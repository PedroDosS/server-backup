from utils.import_util import safe_import
import os

Config = safe_import("config_loader").Config
Logger = safe_import("logger").Logger

global_config = Config()
logger = Logger(os.path.join(global_config.read("log_dir"), "global_logs"))

logger.write("test")
logger.close()