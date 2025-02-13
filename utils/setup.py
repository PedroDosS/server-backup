from import_util import safe_import
from pathlib import Path
import subprocess
import os
import sys

print("Installing dependencies...")
with open("/dev/null", "w") as dev_null:
    subprocess.run(["pip3", "install", "--upgrade", "pipreqs"], stdout=dev_null)
    subprocess.run(["pipreqs", "../", "--ignore", ".venv,__pycache__", "--force"], stdout=dev_null)
    subprocess.run(["pip3", "install", "--upgrade", "-r", "../requirements.txt"], stdout=dev_null)
print("Done!\n")


global_config = safe_import("config_loader").Config()

def mkdir(dir_type, config):
    dir_path = config.read(dir_type)

    if len(dir_path) == 0:
        print(f"Invalid directory. Skipping {dir_type}")
    elif dir_path[0] != "/":
        dir_path = "../" + dir_path

    Path(dir_path).mkdir(parents=True, exist_ok = True)


print("Creating directories...")
mkdir("config_dir", global_config)
mkdir("log_dir", global_config)
mkdir("backup_dir", global_config)
print("Done!\n")





