import os, sys, shutil
from datetime import datetime
from pathlib import Path

sys.path.append(os.path.abspath(Path(__file__, "..", "..")))
from utils import config, logger

def backup_servers(global_config, logger):
   profile_dir = global_config.read("profile-directory")
   log_dir = global_config.read("log-directory")

   for profile_name in os.listdir(profile_dir):
      profile_path = os.path.join(profile_dir, profile_name)

      if not os.path.isfile(profile_path):
         continue

      profile = config.Config(profile_path)

      log_path = os.path.join(log_dir, profile.name + "-logs.txt")
      logger.open_sublog(log_path)

      backup_server(profile, logger)

      logger.close_sublog()


def backup_server(config, logger):
   logger.write("Backing up server...")

   output_name = "Backup_[" + datetime.now().strftime("%Y-%m-%d") + "]"
   output_path = os.path.join(config.read("backup-directory"), config.name, output_name)

   compression_method = config.read("compression-method")
   ext = get_ext(compression_method)

   if os.path.exists(output_path + ext):
      output_name = "Backup_[" + datetime.now().strftime("%Y-%m-%d_%H.%M.%S") + "]"
      output_path = os.path.join(config.read("backup-directory"), config.name, output_name)

   server_directory = config.read("server-directory")

   logger.indent()
   logger.write("Config: " + config.name + ".yaml")
   logger.write("Input: " + str(server_directory))
   logger.write("Output: " + output_path + ext)

   shutil.make_archive(output_path, compression_method, server_directory)

   logger.unindent()
   logger.write("Done!")
   logger.newline()


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
   global_config = config.Config()
   global_logger = logger.Logger(os.path.join(global_config.read("log-directory"), "global-logs.txt"))

   backup_servers(global_config, global_logger)

   global_logger.close()
