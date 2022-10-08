from pyVenus import Connection, Variable, Array, Sequence, Device


class Pipetting:
    def __init__(self, con: Connection):
        self.__con = con
        self.__con.execute(definitions=r'#include "C:\Program Files (x86)\HAMILTON\pyVenus\smt\Pipetting.hs_"')

    def transfer_buffer(self, star_device: Device, source: Sequence, target: Sequence, tips: Sequence, volume, number_of_transfers: Variable):
        """
        Python function generated from submethod 'transfer_buffer' in 'Pipetting.smt'
        Transfers buffer from a trough to all positions in the dispense sequence (target sequence is limiting)
Method uses 1000 uL filter tips
Tips are reused for all transfers and then discarded
            :param star_device: Device (in_out) - star_device object
            :param source: Sequence (in) - Sequence for aspiration (trough)
            :param target: Sequence (in_out) - Sequence for dispense (e.g. plate)
            :param tips: Sequence (in_out) - Sequence of tips (1000 uL filtered)
            :param volume: Variable (in) - Volume to transfer to each position
            :param number_of_transfers: Variable (out) - The number of transfers that were carried out
        """

        # push all variables that are passed into the submethod
        
        source.push()
        target.push()
        tips.push()
        
        number_of_transfers.push()
        

        # generate the parameter string for the HSL function call
        parameter_string = ""
        
        parameter_string += star_device.name
        
        
        parameter_string += ", " + source.name
        
        
        parameter_string += ", " + target.name
        
        
        parameter_string += ", " + tips.name
        
        if isinstance(volume, Variable):
            value = volume.value
        else:
            value = volume
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        
        parameter_string += ", " + number_of_transfers.name
        # call the HSL function
        self.__con.execute("PIPETTING::transfer_buffer(" + parameter_string + ");")

        # pull all variables there were returned by the submethod
        source.pull()
        
        target.pull()
        
        tips.pull()
        
        number_of_transfers.pull()
        
    