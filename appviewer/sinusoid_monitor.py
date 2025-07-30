import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd

import psutil
import os
import struct
from time import sleep
from threading import Thread
from elftools.elf.elffile import ELFFile

# === Configuration ===
ELF_PATH = "./sinusoid"
VARIABLES = ['X', 'Y', 'A', 'B', 'run']
MAX_POINTS = 500
UPDATE_INTERVAL_MS = 100

# === ELF Symbol resolution ===
def get_variable_offsets(elf_path):
    with open(elf_path, 'rb') as f:
        elf = ELFFile(f)
        symtab = elf.get_section_by_name('.symtab')
        if not symtab:
            raise RuntimeError("No symbol table found.")
        symbols = {}
        for sym in symtab.iter_symbols():
            if sym.name in VARIABLES:
                symbols[sym.name] = sym['st_value']
        return symbols

def find_pid_by_name(name):
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if proc.info['exe'] and os.path.basename(proc.info['exe']) == name:
                return proc.pid
        except psutil.AccessDenied:
            continue
    return None

def get_base_address(pid, elf_path):
    with open(f"/proc/{pid}/maps") as f:
        for line in f:
            if elf_path in line:
                return int(line.split('-')[0], 16)
    raise RuntimeError("Base address not found.")

# === Memory access ===
def read_double(pid, addr):
    with open(f"/proc/{pid}/mem", "rb", buffering=0) as mem:
        mem.seek(addr)
        return struct.unpack('d', mem.read(8))[0]

def write_double(pid, addr, value):
    with open(f"/proc/{pid}/mem", "rb+", buffering=0) as mem:
        mem.seek(addr)
        mem.write(struct.pack('d', value))

def write_int(pid, addr, value):
    with open(f"/proc/{pid}/mem", "rb+", buffering=0) as mem:
        mem.seek(addr)
        mem.write(struct.pack('i', value))

def read_int(pid, addr):
    with open(f"/proc/{pid}/mem", "rb", buffering=0) as mem:
        mem.seek(addr)
        return struct.unpack('i', mem.read(4))[0]

# === Acquisition loop ===
buffer_x, buffer_y = [], []
def start_read_loop(pid, var_addrs):
    global buffer_x, buffer_y
    while True:
        try:
            x = read_double(pid, var_addrs['X'])
            y = read_double(pid, var_addrs['Y'])
            buffer_x.append(x)
            buffer_y.append(y)
            if len(buffer_x) > MAX_POINTS:
                buffer_x = buffer_x[-MAX_POINTS:]
                buffer_y = buffer_y[-MAX_POINTS:]
        except Exception as e:
            print("Read error:", e)
        sleep(0.01)

# === Initialisation du processus ===
symbols = get_variable_offsets(ELF_PATH)
pid = find_pid_by_name("sinusoid")
if pid is None:
    raise RuntimeError("Process not running.")
base_addr = get_base_address(pid, os.path.realpath(ELF_PATH))
var_addrs = {name: base_addr + offset for name, offset in symbols.items()}

thread = Thread(target=start_read_loop, args=(pid, var_addrs), daemon=True)
thread.start()

# === Dash App ===
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H3("🧠 Real-time Process Monitor: Y = cos(aX + B)"),
    dbc.Row([
        dbc.Col(dbc.Label("A:"), width=1),
        dbc.Col(dcc.Slider(id="a-slider", min=0, max=10, step=0.1, value=1.0, marks=None, tooltip={"placement": "bottom"}), width=8),
        dbc.Col(html.Div(id="a-display"), width=3)
    ]),
    dbc.Row([
        dbc.Col(dbc.Label("B:"), width=1),
        dbc.Col(dcc.Slider(id="b-slider", min=-10, max=10, step=0.1, value=0.0, marks=None, tooltip={"placement": "bottom"}), width=8),
        dbc.Col(html.Div(id="b-display"), width=3)
    ]),
    dbc.Row([
        dbc.Button(id='run-button', n_clicks=0, color="primary", children="Pause" if read_int(pid, var_addrs['run']) else "Run"),
    ], className="my-3"),
    dbc.Row([
        dbc.Button("Reset View", id="reset-view-btn", color="secondary", className="mr-2"),
        dbc.Button("Exporter CSV", id="export-csv-btn", color="success"),
        dcc.Download(id="download-data")
    ], className="mb-3"),
    dcc.Graph(id='live-plot'),
    dcc.Interval(id='interval', interval=UPDATE_INTERVAL_MS, n_intervals=0)
], fluid=True)

@app.callback(
    Output("a-display", "children"),
    Input("a-slider", "value")
)
def update_a_display(value):
    write_double(pid, var_addrs['A'], value)
    return f"A = {value:.2f}"

@app.callback(
    Output("b-display", "children"),
    Input("b-slider", "value")
)
def update_b_display(value):
    write_double(pid, var_addrs['B'], value)
    return f"B = {value:.2f}"

@app.callback(
    Output("run-button", "children"),
    Input("run-button", "n_clicks"),
    State("run-button", "children")
)
def toggle_run(n, current_label):
    new_value = 0 if current_label == "Pause" else 1
    write_int(pid, var_addrs['run'], new_value)
    return "Run" if new_value == 0 else "Pause"

@app.callback(
    Output("live-plot", "figure"),
    Input("interval", "n_intervals"),
    State("run-button", "children")
)
def update_plot(n, run_label):
    frozen = (run_label == "Run")  # bouton affiche "Run" ⇒ process est gelé

    if read_int(pid, var_addrs['run']) == 0:
        # Return last frozen graph (no new data)
        return dash.no_update
    
    # Données figées
    fig = go.Figure(
        data=[go.Scatter(x=buffer_x, y=buffer_y, mode='lines+markers')],
        layout=go.Layout(
            xaxis=dict(title="X", fixedrange=frozen),
            yaxis=dict(title="Y", fixedrange=frozen),
            title="Y = cos(aX + B)" + (" (🧊 figé)" if frozen else ""),
            margin=dict(l=40, r=40, t=40, b=40),
        )
    )
    return fig

@app.callback(
    Output("live-plot", "relayoutData"),
    Input("reset-view-btn", "n_clicks"),
    prevent_initial_call=True
)
def reset_view(n_clicks):
    return {}  # Dash interprète ça comme "reset layout"

@app.callback(
    Output("download-data", "data"),
    Input("export-csv-btn", "n_clicks"),
    prevent_initial_call=True
)
def export_csv(n_clicks):
    df = pd.DataFrame({'X': buffer_x, 'Y': buffer_y})
    return dcc.send_data_frame(df.to_csv, "sinusoid_trace.csv", index=False)

if __name__ == "__main__":
    app.run(debug=True)
