from import_util import safe_import

json = safe_import("pyjson5")

GLOBAL_CONFIG_PATH = "global_config.json"

class Config:
    config = {}

    def __init__(self):
        try:
            self.load(GLOBAL_CONFIG_PATH)
        except:
            self.load(os.path.join("../", GLOBAL_CONFIG_PATH))

    def load(self, config_path):
        with open(config_path) as config_file:
            self.config.update(json.load(config_file))

    def read(self, key):
        if key in self.config:
            return self.config[key]
        else:
            print(f"Could not read config: '{key}'")
            return None