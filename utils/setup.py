from import_util import safe_import
from pathlib import Path
import subprocess
import os
import sys

def run():
    install_dependencies()

    global_config = safe_import("config_loader").Config()

    create_directories(global_config)
    populate_directories(global_config)

def correct_path(path):
    if len(path) == 0:
        print(f"Invalid path.")
    elif path[0] != "/":
        path = "../" + path
    return Path(path).resolve()

def install_dependencies():
    print("Installing dependencies...")
    subprocess.run(["pip3", "install", "--upgrade", "pipreqs"], stdout=subprocess.DEVNULL)
    subprocess.run(["pipreqs", "../", "--ignore", ".venv,__pycache__", "--force"], stdout=subprocess.DEVNULL)
    subprocess.run(["pip3", "install", "--upgrade", "-r", "../requirements.txt"], stdout=subprocess.DEVNULL)
    print("Done!\n")

def create_directories(global_config):
    def mkdir(dir_type, global_config):
        dir_path = correct_path(global_config.read(dir_type))
        Path(dir_path).mkdir(parents=True, exist_ok = True)

    print("Creating directories...")
    mkdir("log_dir", global_config)
    mkdir("backup_dir", global_config)
    mkdir("config_dir", global_config)
    print("Done!\n")

def populate_directories(global_config):
    print("Populating directories...")

    config_dir = correct_path(global_config.read("config_dir"))

    if not os.listdir(config_dir):
        with open(os.path.join(config_dir, "template.json"), "w") as default_config:

            # TODO: There has to be a better way to do this
            default_config.write('{\n    "log_dir": "./logs",\n    "backup_dir": "./backups",\n    "server_dir": "/home/pedro/Downloads/server",\n\n    //23h in seconds\n    "backup_threshold": 82800\n}')

    print("Done!\n")

run()




