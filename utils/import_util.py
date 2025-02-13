from importlib import import_module, util

def safe_import(module_name):
    try:
        return import_module(module_name)
    except ModuleNotFoundError:
        print(f"Could not load {module_name}. Please run setup.py to install modules, or install it manually.")
        exit(1)

