from pathlib import Path
import subprocess, os, shutil, platform
import config

TEMPLATE_DIR_PATH = Path(__file__, "..", "..", "templates").resolve()

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
    print("Done!\n")

def load_config():
    print("Loading config...")

    if not os.path.exists("global-profile.yaml"):
        if platform.system() == "Windows":
            system_profile = "windows-global.yaml"
        else:
            system_profile = "linux-global.yaml"

        shutil.copy2(Path(TEMPLATE_DIR_PATH, system_profile).resolve(), Path(__file__, "..", "..", "global-profile.yaml").resolve())

    print("Done!\n")
    return config.Config()

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

    config_dir = global_config.read("profile-directory")

    if not os.listdir(config_dir):
        if platform.system() == "Windows":
            system_profile = "windows.yaml"
        else:
            system_profile = "linux.yaml"

        print(Path(TEMPLATE_DIR_PATH, system_profile))
        print(Path(config_dir, "profile.yaml"))

        shutil.copy2(Path(TEMPLATE_DIR_PATH, system_profile), Path(config_dir, "profile.yaml"))
    print("Done!\n")

if __name__ == "__main__":
   run()