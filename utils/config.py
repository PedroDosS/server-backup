import os
from yaml import load, Loader
   
GLOBAL_CONFIG_PATH = "global-config.yaml"

class Config:
    config = {}
    name = ""
    full_name = ""

    def __init__(self, profile_path=None):
        # load global backup profile first
        try:
            self._load(GLOBAL_CONFIG_PATH)
        except:
            self._load(os.path.join("../", GLOBAL_CONFIG_PATH))

        # then, load individual backup profile
        if profile_path is not None:
            self._load(profile_path)

    def _load(self, config_path):
        with open(config_path) as config_file:
            config = load(config_file, Loader)

            # Resolve directory paths to be absolute
            if 'server-directory' in config:
                config['server-directory'] = os.path.abspath(config['server-directory'])
            config['log-directory'] = os.path.abspath(config['log-directory'])
            config['profile-directory'] = os.path.abspath(config['profile-directory'])
            config['backup-directory'] = os.path.abspath(config['backup-directory'])

            self.config = config
            
        self.full_name = os.path.basename(config_path)
        self.name = os.path.splitext(self.full_name)[0]

    def read(self, key):
        if key in self.config:
            return self.config[key]
        else:
            print(f"Could not read config: '{key}'")
            return None