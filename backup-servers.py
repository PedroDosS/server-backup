from utils.import_util import safe_import
import os, shutil
from datetime import datetime

Config = safe_import("config_loader").Config
Logger = safe_import("logger").Logger

def run(global_config, logger):
   config_dir = global_config.read("config_dir")
   log_dir = global_config.read("log_dir")

   for config_name in os.listdir(config_dir):
      config_path = os.path.join(config_dir, config_name)
      log_path = os.path.join(log_dir, os.path.splitext(config_name)[0] + "_logs.txt")

      if os.path.isfile(config_path):
         config = Config(config_path)
         logger.open_sublog(log_path)
         logger.write("Backing up server...")

         output_name = "Backup_[" + datetime.now().strftime("%Y-%m-%d") + "]"
         output_path = os.path.join(config.read("backup_dir"), os.path.splitext(config_name)[0], output_name)

         compression_method = config.read("compression_method")
         ext = get_ext(compression_method)

         if os.path.exists(output_path + ext):
            output_name = "Backup_[" + datetime.now().strftime("%Y-%m-%d_%H.%M.%S") + "]"
            output_path = os.path.join(config.read("backup_dir"), os.path.splitext(config_name)[0], output_name)

         server_directory = config.read("server_dir")

         logger.indent()
         logger.write("Config: " + config_name)
         logger.write("Input: " + server_directory)
         logger.write("Output: " + output_path + get_ext(compression_method))

         shutil.make_archive(output_path, compression_method, server_directory)

         logger.unindent()
         logger.write("Done!")
         logger.newline()
         logger.close()

def get_ext(compression_method):
   if compression_method == "zip":
      return ".zip"
   if compression_method == "tar":
      return ".tar"
   if compression_method == "gztar":
      return ".tar.gz"
   if compression_method == "bztar":
      return ".bz2"
   if compression_method == "xztar":
      return ".tar.xz"

   return ".zip"


if __name__ == "__main__":
   global_config = Config()
   global_logger = Logger(os.path.join(global_config.read("log_dir"), "global_logs.txt"))

   run(global_config, global_logger)

   global_logger.close()




