#!/usr/bin/env python3

"""
    This module is a mem proxy to the sinusoid APP based on the generic proc.
    run standalone it allows R/W on memory variables (for testing purpose), and demonstrate how to use it

    example : 
(.venv) nautilus@ubuntu:~/dev/tmp/sanbox/appviewer$ sudo $(which python3) ./sinusoid_memproxy.py --elf ./sinusoid --read B
0.0
(.venv) nautilus@ubuntu:~/dev/tmp/sanbox/appviewer$ sudo $(which python3) ./sinusoid_memproxy.py --elf ./sinusoid --write A 0
Variable 'a' not known. Should be in: ['X', 'Y', 'A', 'B', 'run']
(.venv) nautilus@ubuntu:~/dev/tmp/sanbox/appviewer$ sudo $(which python3) ./sinusoid_memproxy.py --elf ./sinusoid --write A 0
A set to 0
(.venv) nautilus@ubuntu:~/dev/tmp/sanbox/appviewer$ sudo $(which python3) ./sinusoid_memproxy.py --elf ./sinusoid --read A
0.0
(.venv) nautilus@ubuntu:~/dev/tmp/sanbox/appviewer$ sudo $(which python3) ./sinusoid_memproxy.py --elf ./sinusoid --read XY
(8783.06179690361, 1.0)
(.venv) nautilus@ubuntu:~/dev/tmp/sanbox/appviewer$ sudo $(which python3) ./sinusoid_memproxy.py --elf ./sinusoid --read XY
(8785.188358783722, 1.0)

"""
import argparse
import sys
import procmemproxy as mp

class SinusoidProxy:
    def __init__(self, elf_path="./sinusoid"):
        self.VARIABLES = ['X', 'Y', 'A', 'B', 'run']
        self.proxy = mp.ProcMemProxy(elf_path, variables=self.VARIABLES)

    def get_variables(self):
        return self.proxy.get_symbols().items()

    def get_XY(self):
        x = self.proxy.read_double('X')
        y = self.proxy.read_double('Y')
        return x, y

    def get_A(self): return self.proxy.read_double('A')
    def set_A(self, value: float): self.proxy.write_double('A', value)
    def get_B(self): return self.proxy.read_double('B')
    def set_B(self, value: float): self.proxy.write_double('B', value)
    def get_run(self): return self.proxy.read_int('run') != 0
    def set_run(self, state: bool): self.proxy.write_int('run', int(state))
    def close(self): self.proxy.close()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--elf', type=str, default="./sinusoid", help="ELF absolute/relative file path")
    parser.add_argument('--proc', type=str, default=None, help="Optional: override process name")
    parser.add_argument('--read', nargs=1, metavar='VAR', help="Read a variable (A, B, run, XY)")
    parser.add_argument('--write', nargs=2, metavar=('VAR', 'VALUE'), help="Write a variable (A, B, run)")

    args = parser.parse_args()
    proxy = None

    try:
        proxy = SinusoidProxy(args.elf)
        if args.read:
            var = args.read[0]
            if var not in [v for v in proxy.VARIABLES] and var != "XY" :
                print(f"Variable '{var}' not known. Should be in: {proxy.VARIABLES} or 'XY'", file=sys.stderr)
                return
            if var == "xy":
                print(proxy.get_XY())
            else:
                method_name = f"get_{var}"
                if hasattr(proxy, method_name):
                    print(getattr(proxy, method_name)())
                else:
                    print(f"Read method for '{var}' not implemented.", file=sys.stderr)
        elif args.write:
            var, value = args.write
            if var not in [v for v in proxy.VARIABLES]:
                print(f"Variable '{var}' not known. Should be in: {proxy.VARIABLES}", file=sys.stderr)
                return
            method_name = f"set_{var}"
            if hasattr(proxy, method_name):
                cast = float if var in ['a', 'b'] else int
                getattr(proxy, method_name)(cast(value))
                print(f"{var} set to {value}")
            else:
                print(f"Write method for '{var}' not implemented.", file=sys.stderr)
        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

    finally:
        if proxy:
            proxy.close()

if __name__ == "__main__":
    main()
