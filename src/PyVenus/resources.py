import subprocess
import re
import shutil
import os
import pyodbc
import sys
import json
import warnings
from operator import itemgetter
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape
import pandas as pd

class Resources:
    """Static class with functions to generate python classes from Venus resources
    """         

    @classmethod
    def read_layout(cls, layout: str) -> None:
        """Reads in a Venus layout file (*.lay) and converts it to a python class.

        The generated python class is located in /venus_resources/ and will be named the same as original layout file prefixed with __layout__.

        Args:
            layout (str): Relative or absolute path to the layout file
        """        
        # make sure we are working with an absolute path
        layout = os.path.abspath(layout)

        # get path of original layout and for generated files
        layout_path_original = os.path.dirname(layout)
        layout_path_generated = os.path.join(sys.path[0], "venus_resources")
        os.makedirs(layout_path_generated, exist_ok=True)    

        # get the layout name (both original and sanitized)
        layout_name_original = os.path.splitext(os.path.split(layout)[1])[0]
        layout_name_generated = "__layout__" + cls.__sanitize_identifier(layout_name_original.lower().replace(" ","_"))

        # create a copy of original deck layout
        shutil.copyfile(
            os.path.join(layout_path_original, layout_name_original + ".lay"), 
            os.path.join(layout_path_generated, layout_name_generated + ".lay"))
        shutil.copyfile(
            os.path.join(layout_path_original, layout_name_original + ".res"), 
            os.path.join(layout_path_generated, layout_name_generated + ".res"))

        # convert deck layout from binary to ascii
        cls.__convert_to_ascii(os.path.join(layout_path_generated, layout_name_generated + ".lay"))

        # read deck layout file
        with open(os.path.join(layout_path_generated, layout_name_generated + ".lay"), 'r') as f:
            content = f.read()
        
        # extract names of all the deck sequences
        p = re.compile('Seq.\\d*.Name, "([A-Za-z0-9_]*)",\\n')
        sequences = p.findall(content)

        # extract names of all labware items
        p = re.compile('Labware.\\d*.Id, "([A-Za-z0-9_]*)",\\n')
        labware = p.findall(content)

        # setup template environement
        env = Environment(
            loader=PackageLoader('PyVenus', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('deck_layout.py.j2')

        # write python definition to file
        with open(os.path.join(layout_path_generated, layout_name_generated + ".py"), 'w') as f:
            f.write(str(template.render(layout_file=layout, layout_name=layout_name_generated, sequences=sequences, labware=labware)))

        # log output
        print("Generated: " + os.path.join(layout_path_generated, layout_name_generated + ".py"))
        
        # generate __init__.py
        cls.__generate_init()

    @classmethod
    def read_liquid_classes(
        cls,
        include_1ml_channels: bool = True, 
        include_5ml_channels: bool = False, 
        include_96head: bool = True,
        include_384head: bool = False, 
        include_washstations: bool = False,
        include_default: bool = True,
        include_custom: bool = True,
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
            include_default (bool, optional): Load default liquid classes (all LCs that ship with Venus). Defaults to True.
            include_custom (bool, optional): Load user created liquid classes. Defaults to True.
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

        # set allowed liquid class types (default/custom)
        selected_types = []
        if include_default: selected_types.append(1)
        if include_custom: selected_types.append(0)    

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
            # deselect weird standard liquid classes that nobody needs
            if row[1] in ['a', 'abc', 'abcd', '1']: select = False
            # deselect old dispense modes
            if row[7] in [0, 1]: select = False
            # only allow selected type
            if select:
                if row[6] not in selected_types:
                    select = False

            # process this row?
            if select:
                liquid_classes.append(row[1])

        # setup template environement
        env = Environment(
            loader=PackageLoader('PyVenus', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('liquid_classes.py.j2')

        # write python definition to file
        with open(database_py, 'w') as f:
            f.write(str(template.render(liquid_classes=liquid_classes)))

        # log output
        print("Generated: " + database_py)

        # generate __init__.py
        cls.__generate_init()

    @classmethod
    def read_submethods(cls, directory: str = "") -> None:
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
            skip_this_submethod = False
            
            # ignore temp files
            if path.stem.startswith("~"):
                continue

            # make copy of all files in resource folder
            shutil.copy(
                os.path.join(path.parent, path.stem + ".hs_"),
                os.path.join(output_directory, path.stem + ".hs_")
            )
            shutil.copy(
                os.path.join(path.parent, path.stem + ".hsi"),
                os.path.join(output_directory, path.stem + ".hsi")
            )
            shutil.copy(
                os.path.join(path.parent, path.stem + ".smt"),
                os.path.join(output_directory, path.stem + ".smt")
            )
            shutil.copy(
                os.path.join(path.parent, path.stem + ".stp"),
                os.path.join(output_directory, path.stem + ".stp")
            )

            # convert binary files to ascii
            cls.__convert_to_ascii(os.path.join(output_directory, path.stem + ".smt"))
            cls.__convert_to_ascii(os.path.join(output_directory, path.stem + ".stp"))

            # read file content
            file = str(path.resolve())
            with open(file, 'r') as f:
                content = f.read()

            # get comments of submethod and its parameters
            smt_definition = cls.__parse_hxcfg(os.path.join(output_directory, path.stem + ".smt"))

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
                        warnings.warn(f"Error in {path.stem}.smt ({f.group(1)}): Arrays of sequences are currently not yet supported!")
                        skip_this_submethod = True
                        break

                    if parameters[-1]["hsl_type"] in ["file", "timer", "event", "object", "resource"]:
                        warnings.warn(f"Error in {path.stem}.smt ({f.group(1)}): HSL datatype '{parameters[-1]['hsl_type']}' is not yet supported! Submethod is skipped", stacklevel=2)
                        skip_this_submethod = True
                        break
                        
                    if parameters[-1]["hsl_type"] != "variable" and parameters[-1]["default_value"] is not None:
                        warnings.warn(f"Error in {path.stem}.smt ({f.group(1)}): Default values are currently only supported for variables!")
                        skip_this_submethod = True
                        break

                    if parameters[-1]["direction"] != "in" and parameters[-1]["default_value"] is not None:
                        warnings.warn(f"Error in {path.stem}.smt ({f.group(1)}): Default values are currently only supported for input variables!")
                        skip_this_submethod = True
                        break

                # jump to next submethod if error
                if skip_this_submethod:
                    continue
                
                # sort so all parameters with default values are listed at the end
                parameters = [e for e in parameters if e['default_value'] is None] + [e for e in parameters if e['default_value'] is not None]               

                # add to list of functions
                functions.append({
                    "name": f.group(1),
                    "hasReturn": f.group(3) == "variable",
                    "parameters": parameters,
                    "comment": submethod_comment
                })
            
            #add to list of SMT files
            submethods.append({
                "name": Resources.__sanitize_identifier(path.stem.replace(" ", "_")),
                "file": os.path.splitext(file)[0] + ".hs_",
                "functions": functions
            })

        # setup template environement
        env = Environment(
            loader=PackageLoader('PyVenus', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('submethods.py.j2')

        # write python definition to file
        for smt in submethods:
            with open(os.path.join(output_directory,"__smt__" + smt['name'] + ".py").lower(), 'wb') as f:
                output = template.render(submethods=[smt]).encode("utf-8")
                f.write(output)

            print("Generated: " + os.path.join(output_directory,"__smt__" + smt['name'] + ".py").lower())

        # generate __init__.py
        cls.__generate_init()

    @classmethod
    def __parse_hxcfg(cls, file):
        # read file content
        with open(file, 'r',) as f:
            content = f.read()

        # some special characters (e.g. µ) are not converted correctly but left as hex codes.
        content = re.sub(r"\\0x([A-Za-z0-9]{2})", Resources.__hex_converter, content)
        #content = content.encode("utf8").decode("unicode-escape")
        
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

    @staticmethod
    def __get_comments(smt_definition, submethod):
        df = pd.DataFrame.from_dict(smt_definition['HxMetEd_Submethods']['-533725162'], orient="index")
        df = df[df['1-533725161'] == submethod]
        submethod_comment = df['1-533725170'].values[0]

        parameter_comments = pd.DataFrame()
        df = pd.DataFrame.from_dict(df['-533725169'].values[0], orient="index")
        if not df.empty:
            parameter_comments = df.rename(columns={"1-533725167":"comment", "1-533725168":"parameter"})[["parameter", "comment"]].sort_index()
        
        return submethod_comment, parameter_comments

    @staticmethod
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
                init_code += f"from .{path.stem} import {layout_name[0].upper()}{layout_name[1:].lower()} \n"

            if "__smt__" in path.stem:
                smt_name = path.stem.replace("__smt__", "")
                init_code += f"from .{path.stem} import {smt_name[0].upper()}{smt_name[1:].lower()} \n"

        with open(os.path.join(output_directory, "__init__.py"), 'w') as f:
            f.write(init_code)
    
    @staticmethod
    def __hex_converter(match):
        return chr(int(match.group(1), 16))

    @staticmethod
    def __gen_valid_identifier(seq):
        # get an iterator
        itr = iter(seq)
        # pull characters until we get a legal one for first in identifer
        for ch in itr:
            if ch == '_' or ch.isalpha():
                yield ch
                break
        # pull remaining characters and yield legal ones for identifier
        for ch in itr:
            if ch == '_' or ch.isalpha() or ch.isdigit():
                yield ch

    @classmethod
    def __sanitize_identifier(cls, name):
        return ''.join(cls.__gen_valid_identifier(name))

    
    @staticmethod
    def __convert_to_ascii(file):
        process = subprocess.Popen([
            "C:\\Program Files (x86)\\HAMILTON\\Bin\\HxCfgFilConverter.exe",
            "/t",
            file],
            stdout=subprocess.PIPE,
            universal_newlines=True)
        process.communicate()