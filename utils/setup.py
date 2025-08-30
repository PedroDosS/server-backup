from import_util import safe_import
from pathlib import Path
import subprocess, os, shutil, platform

def run():
    install_dependencies()
    global_config = load_config()
    create_directories(global_config)
    populate_directories(global_config)

def install_dependencies():
    print("Installing dependencies...")
    subprocess.run(["pip3", "install", "--upgrade", "pipreqs"])#, stdout=subprocess.DEVNULL)
    subprocess.run(["pipreqs", "--ignore", ".venv,__pycache__", "--force"])#, stdout=subprocess.DEVNULL)
    subprocess.run(["pip3", "install", "--upgrade", "-r", "requirements.txt"])#, stdout=subprocess.DEVNULL)
    subprocess.run(["pip3", "install", "--upgrade", "pyjson5"])#, stdout=subprocess.DEVNULL)
    print("Done!\n")

def load_config():
    print("Loading config...")

    if not os.path.exists("global-profile.yaml"):
        if platform.system() == "Windows":
            config_name = "windows-global.yaml"
        else:
            config_name = "linux-global.yaml"

        shutil.copy2(os.path.join("templates", config_name), os.path.join("global-profile.yaml"))

    print("Done!\n")
    return safe_import("config_loader").Config()

def create_directories(global_config):
    def mkdir(dir_type, global_config):
        dir_path = global_config.read(dir_type)
        Path(dir_path).mkdir(parents=True, exist_ok = True)

    print("Creating directories...")
    mkdir("log-directory", global_config)
    mkdir("backup-directory", global_config)
    mkdir("profile-directory", global_config)
    print("Done!\n")

def populate_directories(global_config):
    print("Populating directories...")

    config_dir = global_config.read("config_dir")
    template_dir = "templates"

    if not os.listdir(config_dir):
        if platform.system() == "Windows":
            config_name = "windows.yaml"
        else:
            config_name = "linux.yaml"

        shutil.copy2(os.path.join("templates", config_name), os.path.join(config_dir, "config1.yaml"))


    print("Done!\n")

if __name__ == "__main__":
   run()