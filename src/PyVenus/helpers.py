import string, math
from typing import Union

class Helpers:
    """Various helper functions for making the method setup easier
    """    
    
    @classmethod
    def numeric_to_alphanumeric(cls, well_number: Union[int, str], plate_type: Union[int, str], sorting_mode: str = "column-by-column", zero_padding: bool = False) -> str:
        """Convert a well number to a alphanumeric well ID (e.g. 1 to A1 / 96 to H12)

        Args:
            well_number (Union[int, str]): Well number to convert
            plate_type (Union[int, str]): Plate type (6,12,24,48,96,384,1536) 
            sorting_mode (str, optional): Mode of traversing the plate ('column-by-column' or 'row-by-row'). Defaults to "column-by-column".
            zero_padding (bool, optional): Pad numeric part with a zero (e.g. A1 to A01). Defaults to False.

        Returns:
            str: Alphanumeric well ID (e.g. A1)
        """    
        well_number = int(well_number)
        rows, cols = cls.__get_plate_dimensions(plate_type)

        if sorting_mode == "column-by-column":
            if zero_padding:
                return string.ascii_uppercase[(well_number - 1) % rows] + '%02d' % (math.ceil(well_number / rows),)
            else:
                return string.ascii_uppercase[(well_number - 1) % rows] + str(math.ceil(well_number / rows))
        elif sorting_mode == "row-by-row":
            if zero_padding:
                return string.ascii_uppercase[(well_number - 1) // cols] + '%02d' % ((well_number - 1) % cols + 1,)
            else:
                return string.ascii_uppercase[(well_number - 1) // cols] + str((well_number - 1) % cols + 1)
        else:
            raise ValueError("Sorting mode has to be either 'column-by-column' or 'row-by-row'")


    @classmethod
    def get_well_map(cls, plate_type: Union[int, str], sorting_mode: str = "column-by-column", zero_padding: bool = False) -> list:
        """Generate a list of alphanumeric well IDs for the specified plate type and sorting (e.g. [A1, B2, etc.])

        Args:
            plate_type (Union[int, str]): Plate type (6,12,24,48,96,384,1536)
            sorting_mode (str, optional): Mode of traversing the plate ('column-by-column' or 'row-by-row'). Defaults to "column-by-column".
            zero_padding (bool, optional): Pad numeric part with a zero (e.g. A1 to A01). Defaults to False.

        Returns:
            list: List of well IDs
        """    
        plate_type = int(plate_type)

        map = []
        for w in range(1, plate_type+1):
            map.append(cls.numeric_to_alphanumeric(w, plate_type, sorting_mode, zero_padding))

        return map

    @staticmethod
    def __get_plate_dimensions(plate_type: int) -> tuple[int, int]:
        """Return the number of rows and column for a specific plate type

        Args:
            plate_type (int): Plate type (6,12,24,48,96,384,1536)

        Returns:
            tuple[int, int]: rows, columns
        """    
        plate_type = int(plate_type)

        if plate_type == 6:
            return 2, 3
        elif plate_type == 12:
            return 3, 4
        elif plate_type == 24:
            return 4, 6
        elif plate_type == 48:
            return 6, 8
        elif plate_type == 96:
            return 8,12
        elif plate_type == 384:
            return 16, 24
        elif plate_type == 1536:
            return 32, 48
        else:
            raise ValueError("Unsupported plate type. Supported: 6, 12, 24, 48, 96, 384, 1536")
