import os, time, sys
import backup_servers
from pathlib import Path

sys.path.append(os.path.abspath(Path(__file__, "..", "..")))
from utils import config, logger

def run(global_config, logger):
   logger.write("Starting autobackups...")
   logger.indent()

   profile_dir = global_config.read("profile-directory")
   log_dir = global_config.read("log-directory")

   for profile_name in os.listdir(profile_dir):
      profile_path = os.path.join(str(profile_dir), profile_name)

      if not os.path.isfile(profile_path):
         continue

      profile = config.Config(profile_path)
      log_path = os.path.join(log_dir, global_config.name + "-logs.txt")
      logger.open_sublog(log_path)
      logger.indent()

      autobackup(profile, logger)

      logger.unindent()
      logger.close_sublog()


def autobackup(config, logger):
   logger.write("Autobackup: " + config.name)

   logger.indent()
   server_dir = config.read("server-directory")
   backup_dir = config.read("backup-directory")

   if not os.path.exists(server_dir):
      logger.write("Could not find server directory! (" + str(server_dir) + ")")
      logger.unindent()
      return

   last_backup = last_modified(backup_dir)
   last_server_run = last_modified(server_dir)

   if last_backup > last_server_run:
      logger.write("Backup is up to date, no action needed!")
      logger.unindent()
      return

   if time.time() < last_backup + config.read("backup-frequency-secs"):
      logger.write("Backup is recent, no action needed!")
      logger.unindent()
      return

   backup_servers.backup_server(config, logger)


def last_modified(dir):
   last_modified_time = -1

   for root, dirs, files in os.walk(dir):

      for file in files:
         file_path = os.path.join(root, file)

         last_modified_time = max(last_modified_time, os.path.getmtime(file_path))

   return last_modified_time

if __name__ == "__main__":
   global_config = config.Config()
   global_logger = logger.Logger(os.path.join(global_config.read("log-directory"), "global-logs.txt"))

   run(global_config, global_logger)

   global_logger.close()
