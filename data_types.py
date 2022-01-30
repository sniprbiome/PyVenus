import json
import pandas as pd
from . import Connection


class Variable:
    def __init__(self, con: Connection, name, value=0):
        self.__con = con
        self.__name = name
        self.value = value
        self.__con.execute(definitions=f'variable {self.__name} ({self.value});')

    def __str__(self):
        return str(self.value)

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def push(self):
        value_string = f'"{self.value}"' if isinstance(self.value, str) else str(self.value)
        self.__con.execute(f"{self.__name} = {value_string};")

    def pull(self):
        i = self.__con.execute(f'addJSON_variable(___JSON___, {self.__name}, "{self.__name}");')
        ret = json.loads(self.__con.get_return(i))
        self.value = ret[self.__name]


class Array(list):
    def __init__(self, con: Connection, name, value=None):
        list.__init__([])
        if value is None:
            value = []
        self.extend(value)
        self.__con = con
        self.__name = name
        self.__con.execute(definitions=f'variable {self.__name}[];')
        self.push()

    @property
    def name(self):
        return self.__name

    def push(self):
        code = f"{self.__name}.SetSize(0);\n"
        for item in self.copy():
            value_string = f'"{item}"' if isinstance(item, str) else str(item)
            code += f"{self.__name}.AddAsLast({value_string});\n"
        self.__con.execute(code)

    def pull(self):
        i = self.__con.execute(f'addJSON_array(___JSON___, {self.__name}, "{self.__name}");')
        ret = json.loads(self.__con.get_return(i))
        self.clear()
        self.extend(ret[self.__name])


class Sequence:
    def __init__(self, con, name, copy=None):
        self.__con = con
        self.__name = name
        self.__current = 0
        self.__end = 0

        if isinstance(copy, Sequence):
            do_pull = True
            seq_name = copy.name
        elif copy != "":
            do_pull = True
            seq_name = copy
        else:
            do_pull = False
            seq_name = ""

        if do_pull:
            i = self.__con.execute(f'addJSON_sequence(___JSON___, {seq_name}, "{seq_name}");')
            ret = json.loads(self.__con.get_return(i))
            self.__df = pd.DataFrame(
                {
                    'labware': ret[seq_name]["labware"],
                    'position': ret[seq_name]["position"]
                }
            )
            self.end = ret[seq_name]["end"]
            self.current = ret[seq_name]["current"]
        else:
            self.__df = pd.DataFrame(
                {
                    'labware': [],
                    'position': []
                }
            )
            self.end = 0
            self.current = 0

        self.__con.execute(definitions=f'sequence {self.__name};')
        self.push()

    def __str__(self):
        return f"Current: {self.current}\n" \
            f"End: {self.end}\n" \
            f"{self.__df.__str__()}"

    @property
    def name(self):
        return self.__name

    @property
    def current(self):
        return self.__current

    @current.setter
    def current(self, current):
        if current > self.end or current < 0:
            current = 0
        self.__current = current

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, end):
        if end < 0:
            end = 0
        if end > self.total:
            end = self.total
        self.__end = end

        self.current = self.current

    @property
    def remaining(self):
        if self.current > 0:
            return self.end - (self.current - 1)
        else:
            return 0

    @property
    def total(self):
        return len(self.__df.index)

    def push(self):
        code = f'{{ sequence __temp; {self.__name} = __temp; }}\n'
        for row in self.__df.itertuples():
            code += f'{self.__name}.Add("{row.labware}", "{row.position}");\n'
        code += f'{self.__name}.SetCount({self.end});\n'
        code += f'{self.__name}.SetCurrentPosition({self.current});\n'
        self.__con.execute(code)

    def pull(self):
        i = self.__con.execute(f'addJSON_sequence(___JSON___, {self.__name}, "{self.__name}");')
        ret = json.loads(self.__con.get_return(i))
        self.__df = pd.DataFrame(
            {
                'labware': ret[self.__name]["labware"],
                'position': ret[self.__name]["position"]
            }
        )
        self.end = ret[self.__name]["end"]
        self.current = ret[self.__name]["current"]

    def add(self, labware, position, index=None): # TODO: implement adding at specified index
        old_total = self.total

        self.__df = self.__df.append(
            pd.DataFrame(
                {
                    "labware": [labware] if isinstance(labware, str) else labware,
                    "position": [position] if isinstance(position, str) else position,
                }
            ),
            ignore_index=True
        )

        if self.end == old_total:
            self.end = self.total

        if self.current == 0:
            self.current = 1

    def remove(self, index):
        pass

    def clear(self):
        self.__df = self.__df.iloc[0:0]
        self.current = 0
        self.end = 0


class Device:
    def __init__(self, con: Connection, layout_file, name="ML_STAR"):
        self.__con = con
        self.__name = name
        self.__con.execute(definitions=f'device {name}("{layout_file}", "{name}", hslTrue);')

    @property
    def name(self):
        return self.__name
