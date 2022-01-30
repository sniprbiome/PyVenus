import subprocess
import os
import shutil
import time


class Connection:
    def __init__(self, run_environment=r"C:\Program Files (x86)\HAMILTON\Bin\HxRun.exe", start_minimized=False):
        # setup variables
        self.__command_counter = 1
        self.__path_HSLremote = os.path.join(os.path.abspath(os.path.dirname(__file__)), "HSL", "HSLremote")

        # remove old command files
        shutil.rmtree(os.path.join(self.__path_HSLremote, "toSystem"), ignore_errors=True)
        shutil.rmtree(os.path.join(self.__path_HSLremote, "fromSystem"), ignore_errors=True)
        os.makedirs(os.path.join(self.__path_HSLremote, "toSystem"))
        os.makedirs(os.path.join(self.__path_HSLremote, "fromSystem"))

        # start Venus runtime environment
        info = subprocess.STARTUPINFO()
        if start_minimized:
            info.dwFlags = subprocess.STARTF_USESHOWWINDOW
            info.wShowWindow = 6
        self.__runenvironment = subprocess.Popen(
            [
                run_environment,
                "-t",
                os.path.join(self.__path_HSLremote, "HSLremote.hsl")
            ],
            stdout=subprocess.PIPE,
            universal_newlines=True,
            startupinfo=info
        )

    def execute(self, HSLcode="", definitions=""):
        current_counter = self.__command_counter
        self.__command_counter += 1

        code = definitions.replace("\\", "\\\\") + "\n"
        code += "function __EvalExpr__()\n{\n"
        code += HSLcode
        code += "\n}"

        with open(os.path.join(self.__path_HSLremote, "toSystem", str(current_counter) + ".hsl"), "w") as f:
            f.write(code)
            f.close()

        return current_counter

    # def add_library(self, library):
    #     library = library.replace("\\", "\\\\")
    #     self.libraries.append(f'#include "{library}"\n')
    #
    # def add_definition(self, code):
    #     self.definitions.append(code)

    # def variable(self, name, value=0):
    #     self.definitions.append(f'variable {name} ({value});\n')
    #
    # def sequence(self, name):
    #     self.definitions.append(f'sequence {name};\n')
    #
    # def array(self, name):
    #     self.definitions.append(f'variable {name}[];\n')

    # def ml_star(self, layout_file):
    #     layout_file = layout_file.replace("\\", "\\\\")
    #     self.definitions.append(f'device ML_STAR("{layout_file}", "ML_STAR", hslTrue);\n')

    # def add_code(self, code):
    #     self.HSLcode.append(code + "\n")
    #
    #

    def get_return(self, command_counter, wait_for_return=True):
        file = os.path.join(self.__path_HSLremote, "fromSystem", str(command_counter) + ".txt")

        if not os.path.exists(file):
            if wait_for_return:
                while not os.path.exists(file):
                    time.sleep(1)
            else:
                return None

        with open(file, "r") as f:
            content = f.read()
            f.close()
        return content

    # def clear(self):
    #     if (
    #         self.libraries.count() > 0 or
    #         self.definitions.count() > 0 or
    #         self.HSLcode.count() > 0
    #     ) and not self.executed:
    #         warnings.warn("Clearing HSL code that has not yet been executed.")
    #
    #     self.libraries = []
    #     self.definitions = []
    #     self.HSLcode = []

    def close(self):
        #self.clear()
        self.execute("___SHUTDOWN___ = 1;")
