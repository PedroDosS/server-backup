from utils.import_util import safe_import
import os, time

Config = safe_import("config_loader").Config
Logger = safe_import("logger").Logger
backup_server = safe_import("backup_servers").backup_server

def run(global_config, logger):
   logger.write("Starting autobackups...")
   logger.indent()

   config_dir = global_config.read("config_dir")
   log_dir = global_config.read("log_dir")


   for config_name in os.listdir(config_dir):
      config_path = os.path.join(config_dir, config_name)

      if not os.path.isfile(config_path):
         continue

      config = Config(config_path)
      log_path = os.path.join(log_dir, global_config.name + "_logs.txt")
      logger.open_sublog(log_path)
      logger.indent()

      autobackup(config, logger)

      logger.unindent()
      logger.close_sublog()


def autobackup(config, logger):
   logger.write("Autobackup: " + config.name)

   logger.indent()
   server_dir = config.read("server_dir")
   backup_dir = config.read("backup_dir")

   if not os.path.exists(server_dir):
      logger.write("Could not find server directory!")
      logger.unindent()
      return

   last_backup = last_modified(backup_dir)
   last_server_run = last_modified(server_dir)

   if last_backup > last_server_run:
      logger.write("Backup is up to date, no action needed!")
      logger.unindent()
      return

   if time.time() < last_backup + config.read("backup_threshold"):
      logger.write("Backup is recent, no action needed!")
      logger.unindent()
      return

   backup_server(config, logger)


def last_modified(dir):
   last_modified_time = -1

   for root, dirs, files in os.walk(dir):

      for file in files:
         file_path = os.path.join(root, file)

         last_modified_time = max(last_modified_time, os.path.getmtime(file_path))

   return last_modified_time

if __name__ == "__main__":
   global_config = Config()
   global_logger = Logger(os.path.join(global_config.read("log_dir"), "global_logs.txt"))

   run(global_config, global_logger)

   global_logger.close()
