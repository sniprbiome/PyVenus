import os
from . import Connection


class Ml_star:
    def __init__(self, con: Connection, layout_file):
        self.__con = con
        self.__con.execute(definitions=f'device ML_STAR("{layout_file}", "ML_STAR", hslTrue);')
        library = os.path.join(os.path.abspath(os.path.dirname(__file__)), "HSL", "ml_star.hsl")
        self.__con.execute(definitions=f'#include "{library}"')

    def initialize(self):
        self.__con.execute("ml_star::initialize(ML_STAR);")
