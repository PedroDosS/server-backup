from datetime import datetime

class Logger:
   log_file = None
   sublog = None
   indentation = 0
   is_sublogger = False

   def __init__(self, log_file_path, is_sublogger=False):
      self.log_file = open(log_file_path, "a+")
      self.is_sublogger = is_sublogger

   def open_sublog(self, sublog_file_path):
      self.close_sublog()
      self.sublog = Logger(sublog_file_path, is_sublogger=True)

   def close_sublog(self):
      if self.sublog is not None:
         self.sublog.close()

   def indent(self):
      self.indentation += 1

      if self.sublog is not None:
         self.sublog.indent()

   def unindent(self):
      self.indentation -= 1

      if self.sublog is not None:
         self.sublog.unindent()

   def write(self, message):
      if self.sublog is not None:
         self.sublog.write(message)

      if not message == "":
         message = ("  " * self.indentation) +  message
      message = self.__add_date(message)

      if not self.is_sublogger:
         print(message)
      self.log_file.write(message + "\n")

   def warn(self, message):
      if self.sublog is not None:
         self.sublog.write(message)

      message = self.__add_date(message)
      message = f' =============== {message} ==============='

      if not self.is_sublogger:
         print(message)
      self.log_file.write(message)

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