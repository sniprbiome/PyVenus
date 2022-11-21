import subprocess
import os
import shutil
import time
import atexit
import json

class Connection:
    """Connection class that starts the Venus run environment and takes care of data exchange to python environment
    """

    __connected = False    

    def __init__(self, run_environment: str = r"C:\Program Files (x86)\HAMILTON\Bin\HxRun.exe", start_minimized: bool = False) -> None:
        """Initialize run environment

        Args:
            run_environment (str, optional): Path to the Venus run environment executable. Defaults to r"C:\Program Files (x86)\HAMILTON\Bin\HxRun.exe".
            start_minimized (bool, optional): Start the window minimized. Defaults to False.
        """        

        
        # setup variables
        self.__command_counter = 1
        self.__path_HSLremote = os.path.join(os.path.abspath(os.path.dirname(__file__)), "HSL")

        # remove old command files
        path_to = os.path.join(self.__path_HSLremote,  "toSystem")
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
        self.__connected = True

        # register abort handler that closes the run environment
        atexit.register(self.close)

    def execute(self, HSLcode: str = "", definitions:str = "") -> str:      
        """Send HSL code and/or variable/object defintions to the Venus environment and execute them

        Args:
            HSLcode (str, optional): HSL code to execute. Defaults to "".
            definitions (str, optional): Variable or object definitions. Defaults to "".
        
        Returns:
            int: Command counter ID for this execution
        """

        self.__guard()
        
        current_counter = self.__command_counter
        self.__command_counter += 1

        code = definitions.replace("\\", "\\\\") + "\n"
        code += "function __EvalExpr__()\n{\n"
        code += HSLcode
        code += "\n}"

        with open(os.path.join(self.__path_HSLremote, "toSystem", str(current_counter) + ".hsl"), "w") as f:
            f.write(code)

        return self.__get_return(current_counter)

    def close(self):
        """Close connection and shut down run environment
        """     
        atexit.unregister(self.close)   
        self.execute("___SHUTDOWN___ = 1;")
        self.__runenvironment.wait()
        self.__connected = False

    def __get_return(self, command_counter: int) -> str:
        """Get the data returned from the Venus environment for a previous execution command based on its command counter ID

        If an HSL error occured an exception is raised in python with the error description from Venus.

        Args:
            command_counter (int): The command counter ID for the execution data should be retrieved for

        Returns:
            str: The returned data (JSON).
        """ 

        self.__guard()

        file = os.path.join(self.__path_HSLremote, "fromSystem", str(command_counter) + ".json")

        while not os.path.exists(file):
            time.sleep(0.2)

        with open(file, "r") as f:
            content = f.read()

        ret = json.loads(content)
        if "___ERROR_ID___" in ret:
            raise Exception(f"{ret['___ERROR_DESCRIPTION___']}, Error code: {ret['___ERROR_ID___']}, Additional data: {*ret['___ERROR_DATA___'],}")
            
        return content

    def __guard(self):
        if not self.__connected:
            raise Exception("Connection to Hamilton run environment is closed. Initialize the connection before executing commands.")
        
        if not self.__runenvironment.poll() is None:
            raise Exception("Connection to Hamilton run environment has aborted unexpectedly. Check the Hamilton log file for details.")

        