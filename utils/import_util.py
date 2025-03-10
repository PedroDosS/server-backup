from importlib import import_module, util
import sys, os

sys.path.append(os.path.dirname(__file__))

def safe_import(module_name):
    try:
        return import_module(module_name)
    except ModuleNotFoundError:
        pass

    print(f"Could not load {module_name}. Please run \"python3 ./utils/setup.py\" to install modules, or install it manually.")

    input = prompt("Would you like to run setup.py automatically? [Y/n]")
    if input != "n":
        try:
            return import_module(module_name)
        except ModuleNotFoundError:
            pass

    print(f"Still failed to load {module_name}. Please run it manually.")
    exit(1)



