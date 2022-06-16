import subprocess
import os
import shutil
import time
import atexit

class Connection:
    def __init__(self, run_environment=r"C:\Program Files (x86)\HAMILTON\Bin\HxRun.exe", start_minimized=False):
        """
        Python function generated from submethod 'Transfer' in 'smtTest.smt'
            :param ML_STAR: Device (in_out)
            :param i_seqSource: Sequence (in)
            :param i_seqTarget: Sequence (in)
            :param i_seqTips: Sequence (in_out)
            :param i_fltVolume: Variable (in)
        """
        
        # setup variables
        self.__command_counter = 1
        self.__path_HSLremote = os.path.join(os.path.abspath(os.path.dirname(__file__)), "HSL", "HSLremote")

        # remove old command files
        path_to = os.path.join(self.__path_HSLremote, "toSystem")
        path_from = os.path.join(self.__path_HSLremote, "fromSystem")
        if os.path.exists(path_to):
            shutil.rmtree(path_to)
        if os.path.exists(path_from):
            shutil.rmtree(path_from)
        os.makedirs(path_to)
        os.makedirs(path_from)

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
            universal_newlines=True,
            startupinfo=info
        )

        # register abort handler that closes the run environment
        atexit.register(self.close)

    def execute(self, HSLcode="", definitions=""):
        current_counter = self.__command_counter
        self.__command_counter += 1

        code = definitions.replace("\\", "\\\\") + "\n"
        code += "function __EvalExpr__()\n{\n"
        code += HSLcode
        code += "\n}"

        with open(os.path.join(self.__path_HSLremote, "toSystem", str(current_counter) + ".hsl"), "w") as f:
            f.write(code)

        return current_counter


    def get_return(self, command_counter, wait_for_return=True):
        file = os.path.join(self.__path_HSLremote, "fromSystem", str(command_counter) + ".json")

        if not os.path.exists(file):
            if wait_for_return:
                while not os.path.exists(file):
                    time.sleep(0.2)
            else:
                return None

        with open(file, "r") as f:
            content = f.read()
        return content


    def close(self):
        self.execute("___SHUTDOWN___ = 1;")
