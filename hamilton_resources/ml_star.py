from pyVenus import Connection, Variable, Array, Sequence, Device


class Ml_star:
    def __init__(self, con: Connection):
        self.__con = con
        self.__con.execute(definitions=r'#include "C:\Program Files (x86)\HAMILTON\pyVenus_test\pyVenus\smt\ml_star.hs_"')

    def Initialize(self, ML_STAR: Device, i_blnAlwaysInitialize=0):
        """
        Python function generated from submethod 'Initialize' in 'ml_star.smt'
        Initialize the Microlab STAR
            :param ML_STAR: Device (in_out) - ML_STAR
            :param i_blnAlwaysInitialize: Variable (in) - Always initialize the device (or only after power cycling)
        """

        # push all variables that are passed into the submethod
        
        
        

        # generate the parameter string for the HSL function call
        parameter_string = ""
        
        parameter_string += ML_STAR.name
        
        if isinstance(i_blnAlwaysInitialize, Variable):
            value = i_blnAlwaysInitialize.value
        else:
            value = i_blnAlwaysInitialize
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        # call the HSL function
        self.__con.execute("ML_STAR::Initialize(" + parameter_string + ");")

        # pull all variables there were returned by the submethod
    