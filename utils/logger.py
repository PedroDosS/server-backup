class Logger:
    log_file = None
    indentation = 0

    def __init__(self, log_file_path):
         self.log_file = open(log_file_path, "a+")

    def indent(self):
        self.indentation += 1

    def unindent(self):
        self.indentation -= 1

    def newline(self):
        print("")
        self.log_file.write("\n")

    def write(self, message):
        indented_message = ("  " * self.indentation) +  message

        print(indented_message)
        self.log_file.write(indented_message + "\n")

    def warn(self, message):
        print(f' =============== {message} ===============')
        self.log_file.write(f' =============== {message} ===============')

    def close(self):
        self.log_file.close()