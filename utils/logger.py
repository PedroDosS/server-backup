from datetime import datetime

class Logger:
   log_file = None
   sublog = None
   indentation = 0

   def __init__(self, log_file_path):
      self.log_file = open(log_file_path, "a+")

   def open_sublog(self, sublog_file_path):
      self.close_sublog()
      self.sublog = open(sublog_file_path, "a+")

   def close_sublog(self):
      if self.sublog is not None:
         self.sublog.close()

   def indent(self):
      self.indentation += 1

   def unindent(self):
      self.indentation -= 1

   def write(self, message):
      if not message == "":
         message = ("   " * self.indentation) +  message
      message = self.__add_date(message)

      print(message)
      self.log_file.write(message + "\n")

      if self.sublog is not None:
         self.sublog.write(message + "\n")

   def warn(self, message):
      message = self.__add_date(message)

      print(f' =============== {message} ===============')
      self.log_file.write(f' =============== {message} ===============')

      if self.sublog is not None:
         self.sublog.write(message + "\n")

   def newline(self):
      self.write("")

   def close(self):
      self.log_file.close()

      if self.sublog is not None:
         self.sublog.close()

   def __add_date(self, message):
      date = "[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"

      if message == "":
         return date
      return date + "  " + message