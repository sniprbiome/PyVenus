import subprocess
import re
import shutil
import os
import pyodbc
import sys
import json
from operator import itemgetter
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape
import pandas as pd

class Resources:
    """Static class with functions to generate python classes from Venus resources
    """         

    def read_layout(layout: str) -> None:
        """Reads in a Venus layout file (*.lay) and converts it to a python class.

        The generated python class is located in /venus_resources/ and will be named the same as original layout file prefixed with __layout__.

        Args:
            layout (str): Relative or absolute path to the layout file
        """        
        # get output directory for resources
        output_directory = os.path.join(sys.path[0], "venus_resources")
        os.makedirs(output_directory, exist_ok=True)

        # make sure we are working with an absolute path
        layout = os.path.abspath(layout)

        # set filenames and paths
        layout_ascii = os.path.join(output_directory, os.path.splitext(os.path.split(layout)[1])[0] + ".txt")
        layout_py = os.path.join(output_directory, "__layout__" + os.path.splitext(os.path.split(layout)[1])[0].lower() + ".py")

        # create a copy of original deck layout
        shutil.copyfile(layout, layout_ascii)

        # convert deck layout from binary to ascii
        process = subprocess.Popen([
            "C:\\Program Files (x86)\\HAMILTON\\Bin\\HxCfgFilConverter.exe",
            "/t",
            layout_ascii],
            stdout=subprocess.PIPE,
            universal_newlines=True)
        process.communicate()

        # read deck layout file
        with open(layout_ascii, 'r') as f:
            content = f.read()
            p = re.compile('Seq.\\d*.Name, "([A-Za-z0-9_]*)",\\n')
            sequences = p.findall(content)

        # setup template environement
        env = Environment(
            loader=PackageLoader('pyVenus', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('deck_layout.py.j2')

        # write python definition to file
        with open(layout_py, 'w') as f:
            f.write(str(template.render(sequences=sequences, layout_file=layout)))

        # cleanup
        os.remove(layout_ascii)

        # generate __init__.py
        Resources.__generate_init()


    def read_liquid_classes(
        include_1ml_channels: bool = True, 
        include_5ml_channels: bool = False, 
        include_96head: bool = True,
        include_384head: bool = False, 
        include_washstations: bool = False,
        database: str = r'C:\Program Files (x86)\HAMILTON\Config\ML_STARLiquids.mdb') -> None:
        """Reads in the default Venus liquid class database and converts it to a python class.

        It is possible to restrict the list of liquid classes to those fitting the system configuration.
        The generated python class is located at /venus_resources/__liquid_classes__.py

        Args:
            include_1ml_channels (bool, optional): Load liquid classes for 1 mL channels. Defaults to True.
            include_5ml_channels (bool, optional): Load liquid classes for 5 mL channels. Defaults to False.
            include_96head (bool, optional): Load liquid classes for the 96 multiprobe head. Defaults to True.
            include_384head (bool, optional): Load liquid classes for the 384 multiprobe head. Defaults to False.
            include_washstations (bool, optional): Load liquid classes for the wash stations. Defaults to False.
            database (str, optional): Path to a non-standard liquid class database file. Defaults to r'C:\Program Files (x86)\HAMILTON\Config\ML_STARLiquids.mdb'.
        """        

        # get output directory for resources
        output_directory = os.path.join(sys.path[0], "venus_resources")
        os.makedirs(output_directory, exist_ok=True)

        # set filenames and paths
        database_py = os.path.join(output_directory, "__liquid_classes__.py")

        # connect to Access DB with liquid classes
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + database + ';')
        cursor = conn.cursor()
        cursor.execute('select * from LiquidClass')

        # generate list with appropriate device IDs
        selected_devices = []
        if include_1ml_channels: selected_devices.append(1)
        if include_5ml_channels: selected_devices.append(7)
        if include_96head: selected_devices.append(2)
        if include_384head: selected_devices.append(8)
        if include_washstations: selected_devices.extend([9, 3, 5, 6, 4])

        # gather all liquid classes
        liquid_classes = []
        for row in cursor.fetchall():
            select = False

            # select only the liquid classes for the appropriate devices
            devices = [int(i) for i in row[4].split(';')]
            if any(item in devices for item in selected_devices):
                select = True
            # deselect old tip types
            if row[8] in [6, 7, 8]: select = False
            # deselect weird standard tip types
            if row[1] in ['a', 'abc', 'abcd', '1']: select = False
            # deselect old dispense modes
            if row[7] in [0, 1]: select = False

            # process this row?
            if select:
                liquid_classes.append(row[1])

        # setup template environement
        env = Environment(
            loader=PackageLoader('pyVenus', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('liquid_classes.py.j2')

        # write python definition to file
        with open(database_py, 'w') as f:
            f.write(str(template.render(liquid_classes=liquid_classes)))

        # generate __init__.py
        Resources.__generate_init()


    def read_submethods(directory: str = "") -> None:
        """Reads in all the submethod files at the specified folder and converts them to python classes.

        An empty string for the directory parameter (default) loads from /smt/

        All python classes are generated in venus_resources/ and are given the same name as the original smt file, prefixed with __smt__

        Args:
            directory (str, optional): The path to directory with smt files. Defaults to "".
        """        

        # set default directory with SMTs
        if directory == "":
            directory = os.path.join(sys.path[0], "smt")

        # get output directory for resources
        output_directory = os.path.join(sys.path[0], "venus_resources")
        os.makedirs(output_directory, exist_ok=True)

        # loop over all submethod libraries
        pathlist = Path(directory).rglob('*.hsi')
        submethods = []
        for path in pathlist:
            # ignore temp files
            if path.stem.startswith("~"):
                continue

            # read file content
            file = str(path.resolve())
            with open(file, 'r') as f:
                content = f.read()

            # get comments of submethod and its parameters
            smt_definition = Resources.__parse_hxcfg(os.path.join(path.parent, path.stem + ".smt"))


            # setup regex expressions
            pattern_function = re.compile(r"\/\/ {{{ \d+ \"([\w\d_]+)\" \"Begin\"\nfunction \1\( ([\w\d\s&,\[\]]*) \)\s(\w+)\s{\n\/\/ }} \"\"\n[\w\d\s;\[\]\n]*\/\/ {{ \d+ \"\1\" \"InitLocals\"\n([\w\s\d\(\)&,\[\]{}\/\";=\.]*?)\n?\/\/ }} \"\"")
            pattern_parameter = re.compile(r"(\w+)\s(&?)\s?([\w\d&]+)([\[\]]*)[,]*")
            pattern_defaultvalue = re.compile(r"\{\{default:(.*?)\}\}(.*)")

            # find all functions in file
            match_functions = pattern_function.finditer(content)

            # extract information for each function
            functions = []
            for f in match_functions:
                # find all function parameters
                match_parameters = pattern_parameter.finditer(f.group(2))
                parameters = []

                # extract comments from SMT definition
                submethod_comment, parameter_comments = Resources.__get_comments(smt_definition, f.group(1))

                # extract information for each parameter
                for p in match_parameters:
                    # direction: in, out, in_out
                    if p.group(3) in f.group(4):
                        direction = "out"
                    elif p.group(2) == "&":
                        direction = "in_out"
                    else:
                        direction = "in"

                    # is this an array (e.g. array of variables, array of sequences
                    is_array = p.group(4) == "[]"

                    # define datatype in HSL and python
                    hsl_type = p.group(1)
                    if hsl_type == "variable" and is_array:
                        py_type = "Array"
                    else:
                        py_type = hsl_type.capitalize()

                    # define how the parameter is passed to the HSL function
                    # variable: variable is pushed to HSL and then the name of the variable is passed to function
                    # value: the value is directly passed to the function
                    if py_type == "Variable" and direction == "in":
                        pass_mode = "value"
                    else:
                        pass_mode = "variable"

                    # get comment for this parameter
                    comment = parameter_comments[parameter_comments.parameter.eq(p.group(3))]['comment'].values[0]

                    # is a default value set?
                    default_value = None
                    match = pattern_defaultvalue.match(comment)
                    if match:
                        default_value = match.group(1)
                        comment = match.group(2)
                        
                    # add to list of parameters
                    parameters.append({
                        "name": p.group(3),
                        "hsl_type": hsl_type,
                        "py_type": py_type,
                        "is_array": is_array,
                        "direction": direction,
                        "pass_mode": pass_mode,
                        "comment": comment,
                        "default_value": default_value
                    })

                    # throw an error on currently unsupported data types
                    if parameters[-1]["hsl_type"] == "sequence" and parameters[-1]["is_array"]:
                        raise Exception("Arrays of sequences are currently not yet supported!")
                    if parameters[-1]["hsl_type"] in ["file", "timer", "event", "object", "resource"]:
                        raise Exception("HSL datatype '" + parameters[-1]["hsl_type"] + "' is not yet supported!")
                    if parameters[-1]["hsl_type"] != "variable" and parameters[-1]["default_value"] is not None:
                        raise Exception("Default values are currently only supported for variables!")
                    if parameters[-1]["direction"] != "in" and parameters[-1]["default_value"] is not None:
                        raise Exception("Default values are currently only supported for input variables!")

                # sort so all parameters with default values are listed at the end
                parameters = [e for e in parameters if e['default_value'] is not None] + [e for e in parameters if e['default_value'] is None]               

                # add to list of functions
                functions.append({
                    "name": f.group(1),
                    "hasReturn": f.group(3) == "variable",
                    "parameters": parameters,
                    "comment": submethod_comment
                })

            #add to list of SMT files
            submethods.append({
                "name": path.stem,
                "file": os.path.splitext(file)[0] + ".hs_",
                "functions": functions
            })

        # setup template environement
        env = Environment(
            loader=PackageLoader('pyVenus', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('submethods.py.j2')

        # write python definition to file
        for smt in submethods:
            with open(os.path.join(output_directory,"__smt__" + smt['name'] + ".py").lower(), 'w') as f:
                f.write(str(template.render(submethods=[smt])))

        # generate __init__.py
        Resources.__generate_init()

    def __parse_hxcfg(file):
        # get output directory for resources
        output_directory = os.path.join(sys.path[0], "venus_resources")
        os.makedirs(output_directory, exist_ok=True)

        # make a copy of the file
        file_ascii = os.path.join(output_directory, os.path.splitext(os.path.split(file)[1])[0] + ".txt")
        shutil.copy(file, file_ascii)

        # convert .smt from binary to ascii
        process = subprocess.Popen([
            "C:\\Program Files (x86)\\HAMILTON\\Bin\\HxCfgFilConverter.exe",
            "/t",
            file_ascii],
            stdout=subprocess.PIPE,
            universal_newlines=True)
        process.communicate()

        # read file content
        with open(file_ascii, 'r',) as f:
            content = f.read()

        os.remove(file_ascii)
        
        pattern_blocks = re.compile("DataDef,HxPars,3,(\w+),\n\[\n([\s\S]*?)\"\)\"\n\];")
        pattern_line = re.compile("\"([\(\)]?)(.*)\",")

        match_blocks = pattern_blocks.finditer(content)

        json_string = "{\n"
        value_line = False
        for b in match_blocks:
            json_string += f"\"{b.group(1)}\": {{\n"

            for l in b.group(2).splitlines():
                if l == "":
                    continue

                match_line = pattern_line.match(l)
                
                if value_line:
                    json_string += f"\"{match_line.group(2)}\",\n"
                    value_line = False
                    continue

                if match_line.group(1) == "(":
                    json_string += f"\"{match_line.group(2)}\": {{ \n"
                    continue

                if match_line.group(1) == ")":
                    json_string = json_string.rstrip(",\n")
                    json_string += f"\n}},\n"
                    continue
                
                json_string += f"\"{match_line.group(2)}\": "
                value_line = True
            json_string = json_string.rstrip(",\n")
            json_string += f"}},\n"
        json_string = json_string.rstrip(",\n")
        json_string += f"}}"

        return json.loads(json_string)

    def __get_comments(smt_definition, submethod):
        df = pd.DataFrame.from_dict(smt_definition['HxMetEd_Submethods']['-533725162'], orient="index")
        df = df[df['1-533725161'] == submethod]
        submethod_comment = df['1-533725170'].values[0]

        parameter_comments = pd.DataFrame()
        df = pd.DataFrame.from_dict(df['-533725169'].values[0], orient="index")
        if not df.empty:
            parameter_comments = df.rename(columns={"1-533725167":"comment", "1-533725168":"parameter"})[["parameter", "comment"]].sort_index()
        
        return submethod_comment, parameter_comments

    def __generate_init():
        # get output directory for resources
        output_directory = os.path.join(sys.path[0], "venus_resources")

        # loop over all submethod libraries
        init_code = ""
        pathlist = Path(output_directory).rglob('*.py')
        for path in pathlist:
            if path.stem == "__liquid_classes__":
                init_code += f"from .{path.stem} import LiquidClasses\n" 

            if "__layout__" in path.stem:
                layout_name = path.stem.replace("__layout__", "")
                init_code += f"from .{path.stem} import DeckLayout as Layout_{layout_name[0].upper()}{layout_name[1:].lower()} \n"

            if "__smt__" in path.stem:
                smt_name = path.stem.replace("__smt__", "")
                init_code += f"from .{path.stem} import {smt_name[0].upper()}{smt_name[1:].lower()} \n"

        with open(os.path.join(output_directory, "__init__.py"), 'w') as f:
            f.write(init_code)

        