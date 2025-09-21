#!/usr/bin/env python3

"""
    This module is a mem proxy to a target app.
    It allows R/W on memory variables.
    ProcMemProxy implement this proxy.

    The main is aimed to use it as a tool.

    Example : 
    (.venv) nautilus@ubuntu:~/appviewer$ sudo $(which python3) ./procmemproxy.py --read X double
386.17536997795105
(.venv) nautilus@ubuntu:~/appviewer$ sudo $(which python3) ./procmemproxy.py --read Y double
-0.9574334011780304
(.venv) nautilus@ubuntu:~/appviewer$ sudo $(which python3) ./procmemproxy.py --read X int
1954545664
(.venv) nautilus@ubuntu:~/appviewer$ sudo $(which python3) ./procmemproxy.py --read run int
1
(.venv) nautilus@ubuntu:~/appviewer$ sudo $(which python3) ./procmemproxy.py --write run int 0
(.venv) nautilus@ubuntu:~/appviewer$ sudo $(which python3) ./procmemproxy.py --read run int
0

Support OS linux. windows is TBD.

"""
import argparse
import sys
import os
import struct
import psutil
from elftools.elf.elffile import ELFFile

class ProcMemProxy:
    """ Low level Mem proxy to target linux process
        It will attach to target running process, and allow R/W on target variables
        To help defining variables, it can load the elf file to list exposed variables with their type

        :parameter path : absolute path to the binary (that should be executed as a process). 
        :parameter process_name : the process name as listed, if different from the elf. default : not needed.
        :parameter variables variable list name to search for. if empty it will lookup for any exposed variable.

        Two use cases : 
        - inspect mode : only list variables and their address. Process need not be running.
        - R/W mode : the process must be running, and the proxy will attach to it
        Note : the process must not be stripped, and must be compiled with -g option.
        TODO : read/write more types (byte, string)
    """
    def __init__(self, elf_path: str, process_name: str = None, variables: list[str] = None):
        self.elf_path = os.path.realpath(elf_path)
        self.process_name = process_name or os.path.basename(self.elf_path)
        self.variables = variables
        # get variables info from process
        self.symbols = self._get_variable_offsets()

        # Proc mem file will be opened after first use, this Proxy can be use for inspection only
        self.mem_file = None
        self.pid = None
        self.base_addr = None
        self.var_addrs = None


    def get_symbols(self):
        return self.symbols

    def _get_variable_offsets(self):
        with open(self.elf_path, 'rb') as f:
            elf = ELFFile(f)
            symtab = elf.get_section_by_name('.symtab')
            if not symtab:
                raise RuntimeError("No symbol table found.")

            symbols = {}
            for sym in symtab.iter_symbols():
                name = sym.name
                bind = sym['st_info']['bind']
                typ = sym['st_info']['type']

                # Ne garde que les objets globaux visibles de taille > 0
                if typ != 'STT_OBJECT':
                    continue
                if bind not in ('STB_GLOBAL', 'STB_WEAK'):
                    continue
                if not name or name.startswith("__") or name.startswith("_Z"):
                    continue
                if sym['st_size'] == 0:
                    continue
                if name == "_IO_stdin_used":
                    continue
                if self.variables is None or name in self.variables:
                    symbols[name] = {
                        'offset': sym['st_value'],
                        'size': sym['st_size'],
                        'bind': bind,
                        'type': typ
                    }
            return symbols

    def _find_pid_by_name(self):
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                if proc.info['exe'] and os.path.basename(proc.info['exe']) == self.process_name:
                    return proc.pid
            except psutil.AccessDenied:
                continue
        return None

    def _get_base_address(self):
        with open(f"/proc/{self.pid}/maps") as f:
            for line in f:
                if self.elf_path in line:
                    return int(line.split('-')[0], 16)
        raise RuntimeError("Base address not found.")


    def open_mem(self):
        """Open the process memory file if not already open."""
        if self.mem_file is not None:
            return
        self.pid = self._find_pid_by_name()
        if self.pid is None:
            raise RuntimeError("Process not running.")
        self.base_addr = self._get_base_address()
        self.var_addrs = {name: self.base_addr + info['offset'] for name, info in self.symbols.items()}
        self.mem_file = open(f"/proc/{self.pid}/mem", "rb+", buffering=0)

    def read_double(self, varname):
        self.open_mem()
        addr = self.var_addrs[varname]
        self.mem_file.seek(addr)
        return struct.unpack('d', self.mem_file.read(8))[0]

    def write_double(self, varname, value):
        self.open_mem()
        addr = self.var_addrs[varname]
        self.mem_file.seek(addr)
        self.mem_file.write(struct.pack('d', value))

    def read_int(self, varname):
        self.open_mem()
        addr = self.var_addrs[varname]
        self.mem_file.seek(addr)
        return struct.unpack('i', self.mem_file.read(4))[0]

    def write_int(self, varname, value):
        self.open_mem()
        addr = self.var_addrs[varname]
        self.mem_file.seek(addr)
        self.mem_file.write(struct.pack('i', value))

    def close(self):
        if self.mem_file is None:
            return        
        self.mem_file.close()

def main():
    """
    This allow testing the module and cli interface with a process for simple read/write operation
    options are : --listvars : list found variables with adress in a csv fashion
                  --read <variable name> <type> will execute a read according to type
                  --write <variable name> <type> <value> execute a write according to type
    """
    parser = argparse.ArgumentParser(description="Memory proxy for sinusoid process")
    parser.add_argument('--elf', type=str, default="./sinusoid", help="ELF absolut/relative file path")
    parser.add_argument('--proc', type=str, default=None, help="Optional: override process name")
    parser.add_argument('--listvars', action='store_true', help="List found variables and their addresses")
    parser.add_argument('--read', nargs=2, metavar=('VAR', 'TYPE'), help="Read a variable (TYPE = int|double)")
    parser.add_argument('--write', nargs=3, metavar=('VAR', 'TYPE', 'VALUE'), help="Write a variable")

    args = parser.parse_args()
    proxy = None

    try:
        if args.listvars:
            proxy = ProcMemProxy(args.elf, args.proc)
            print("Variable,Address offset(hex),Size,Bind,Type")
            for var, info in proxy.get_symbols().items():
                print(f"{var},{hex(info['offset'])},{info['size']},{info['bind']},{info['type']}")
            return

        elif args.read:
            var, typ = args.read
            proxy = ProcMemProxy(args.elf, args.proc, var)
            if typ == 'int':
                print(proxy.read_int(var))
            elif typ == 'double':
                print(proxy.read_double(var))
            else:
                print("Unknown type. Use 'int' or 'double'.", file=sys.stderr)

        elif args.write:
            var, typ, value = args.write
            proxy = ProcMemProxy(args.elf, args.proc, var)
            if typ == 'int':
                proxy.write_int(var, int(value))
            elif typ == 'double':
                proxy.write_double(var, float(value))
            else:
                print("Unknown type. Use 'int' or 'double'.", file=sys.stderr)
        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

    finally:
        if proxy:
            proxy.close()

if __name__ == "__main__":
    main()
