from import_util import safe_import
import os

json = safe_import("pyjson5")

GLOBAL_CONFIG_PATH = "global_config.json"

class Config:
    config = {}
    name = ""
    full_name = ""

    def __init__(self, config_path=None):
        try:
            self._load(GLOBAL_CONFIG_PATH)
        except:
            self._load(os.path.join("../", GLOBAL_CONFIG_PATH))

        if config_path is not None:
            self._load(config_path)

    def _load(self, config_path):
        with open(config_path) as config_file:
            data = json.load(config_file)

            for category in data["categories"]:
                for setting in category["settings"]:
                    id = setting["id"]
                    value = setting["value"]

                    self.config[id] = value

        self.full_name = os.path.basename(config_path)
        self.name = os.path.splitext(self.full_name)[0]

    def read(self, key):
        if key in self.config:
            return self.config[key]
        else:
            print(f"Could not read config: '{key}'")
            return None