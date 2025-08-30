import os
from pathlib import Path
from yaml import load, Loader
   
GLOBAL_CONFIG_PATH = Path(os.path.join(os.path.abspath(__file__), "..", "..", "global-profile.yaml")).resolve()

class Config:
    config = {}
    name = ""
    full_name = ""

    def __init__(self, profile_path=None):
        # load global backup profile first
        self._load(GLOBAL_CONFIG_PATH)

        # then, load individual backup profile
        if profile_path is not None:
            self._load(profile_path)

    def _load(self, config_path):
        with open(config_path) as config_file:
            config = load(config_file, Loader)

            # Resolve directory paths to be absolute
            if 'server-directory' in config:
                config['server-directory'] = Path(__file__, "..", "..", config['server-directory']).resolve()
            config['log-directory'] = Path(__file__, "..", "..", config['log-directory']).resolve()
            config['profile-directory'] = Path(__file__, "..", "..",config['profile-directory']).resolve()
            config['backup-directory'] = Path(__file__, "..", "..", config['backup-directory']).resolve()

            self.config = config
            
        self.full_name = os.path.basename(config_path)
        self.name = os.path.splitext(self.full_name)[0]

    def read(self, key):
        if key in self.config:
            return self.config[key]
        else:
            print(f"Could not read config: '{key}'")
            return None