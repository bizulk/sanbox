#!/usr/bin/env python3
"""
    Real-time process variable visualizer using Dash and sinusoid_memproxy
    Parameters like MAX_POINTS, UPDATE_INTERVAL_MS and read_interval_s are configurable from the frontend.
    Configuration is saved in a JSON file for persistence.
"""

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from threading import Thread
from time import sleep
import json
from pathlib import Path

from sinusoid_memproxy import SinusoidProxy

# === Config persistence ===
CONFIG_FILE = Path("monitor_config.json")
DEFAULT_CONFIG = {
    "max_points": 500,
    "update_interval_ms": 100,
    "read_interval_ms": 10
}

def load_config():
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except:
            return DEFAULT_CONFIG.copy()
    else:
        return DEFAULT_CONFIG.copy()

def save_config(conf):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(conf, f, indent=4)

config = load_config()

# === Init proxy ===
proxy = SinusoidProxy()
buffer_x, buffer_y = [], []

def read_loop():
    global buffer_x, buffer_y
    while True:
        try:
            x, y = proxy.get_XY()
            buffer_x.append(x)
            buffer_y.append(y)

            max_len = config["max_points"]
            if len(buffer_x) > max_len:
                buffer_x = buffer_x[-max_len:]
                buffer_y = buffer_y[-max_len:]
        except Exception as e:
            print(f"[read_loop] Error: {e}")
        sleep(config["read_interval_ms"] / 1000.0)

# === Start background thread ===
thread = Thread(target=read_loop, daemon=True)
thread.start()

# === Dash App ===
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H3("🧠 Real-time Process Monitor: Y = cos(aX + B)"),

    # Parameter controls
    html.H5("🔧 Configuration"),
    dbc.Row([
        dbc.Col(dbc.Label("Graph Update Interval (ms):"), width=3),
        dbc.Col(dcc.Slider(id="update-interval-slider", min=50, max=1000, step=50,
                           value=config["update_interval_ms"],
                           tooltip={"placement": "bottom"}), width=7),
        dbc.Col(html.Div(id="update-interval-display"), width=2),
    ], className="mb-2"),
    dbc.Row([
        dbc.Col(dbc.Label("Graph Max Points:"), width=3),
        dbc.Col(dcc.Slider(id="max-points-slider", min=100, max=2000, step=100,
                           value=config["max_points"],
                           tooltip={"placement": "bottom"}), width=7),
        dbc.Col(html.Div(id="max-points-display"), width=2),
    ], className="mb-2"),
    dbc.Row([
        dbc.Col(dbc.Label("data sampling Interval (ms):"), width=3),
        dbc.Col(dcc.Slider(id="read-interval-slider", min=1, max=100, step=10,
                           value=config["read_interval_ms"],
                           tooltip={"placement": "bottom"}), width=7),
        dbc.Col(html.Div(id="read-interval-display"), width=2),
    ], className="mb-4"),

    html.Hr(),

    # Controls
    dbc.Row([
        dbc.Col(dbc.Label("A:"), width=1),
        dbc.Col(dcc.Slider(id="a-slider", min=0, max=10, step=0.1, value=proxy.get_A(),
                           marks=None, tooltip={"placement": "bottom"}), width=8),
        dbc.Col(html.Div(id="a-display"), width=3)
    ]),
    dbc.Row([
        dbc.Col(dbc.Label("B:"), width=1),
        dbc.Col(dcc.Slider(id="b-slider", min=-10, max=10, step=0.1, value=proxy.get_B(),
                           marks=None, tooltip={"placement": "bottom"}), width=8),
        dbc.Col(html.Div(id="b-display"), width=3)
    ]),
    dbc.Row([
        dbc.Button(id='run-button', n_clicks=0, color="primary",
                   children="Pause" if proxy.get_run() else "Run"),
    ], className="my-3"),
    dbc.Row([
        dbc.Button("Reset View", id="reset-view-btn", color="secondary", className="mr-2"),
        dbc.Button("Exporter CSV", id="export-csv-btn", color="success"),
        dcc.Download(id="download-data")
    ], className="mb-3"),
    dcc.Graph(id='live-plot'),

    # Hidden store for update interval
    dcc.Interval(id='interval', interval=config["update_interval_ms"], n_intervals=0),
], fluid=True)

# === Callbacks ===

@app.callback(Output("a-display", "children"), Input("a-slider", "value"))
def update_a_display(value):
    proxy.set_A(value)
    return f"A = {value:.2f}"

@app.callback(Output("b-display", "children"), Input("b-slider", "value"))
def update_b_display(value):
    proxy.set_B(value)
    return f"B = {value:.2f}"

@app.callback(
    Output("run-button", "children"),
    Input("run-button", "n_clicks"),
    State("run-button", "children")
)
def toggle_run(n_clicks, current_label):
    new_value = current_label == "Run"
    proxy.set_run(new_value)
    return "Pause" if new_value else "Run"

@app.callback(
    Output("live-plot", "figure"),
    Input("interval", "n_intervals"),
    State("run-button", "children")
)
def update_plot(n, run_label):
    frozen = run_label == "Run"
    if not proxy.get_run():
        return dash.no_update

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
    return {}

@app.callback(
    Output("download-data", "data"),
    Input("export-csv-btn", "n_clicks"),
    prevent_initial_call=True
)
def export_csv(n_clicks):
    df = pd.DataFrame({'X': buffer_x, 'Y': buffer_y})
    return dcc.send_data_frame(df.to_csv, "sinusoid_trace.csv", index=False)

@app.callback(
    Output("interval", "interval"),
    Input("update-interval-slider", "value")
)
def update_interval_slider(val):
    config["update_interval_ms"] = val
    save_config(config)
    return val

@app.callback(Output("update-interval-display", "children"), Input("update-interval-slider", "value"))
def show_update_interval(val):
    return f"{val} ms"

@app.callback(Output("max-points-display", "children"), Input("max-points-slider", "value"))
def update_max_points(val):
    config["max_points"] = val
    save_config(config)
    return f"{val} points"

@app.callback(Output("read-interval-display", "children"), Input("read-interval-slider", "value"))
def update_read_interval(val_ms):
    config["read_interval_ms"] = val_ms
    save_config(config)
    return f"{val_ms} ms"

if __name__ == "__main__":
    app.run(debug=True)
