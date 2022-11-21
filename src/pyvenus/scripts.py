import sys
import os
import shutil
from argparse import ArgumentParser
from importlib.metadata import version

def pyvenus_main():
    parser = ArgumentParser()
    parser.add_argument("-v", "--version", action="store_true")

    args = parser.parse_args()

    if args.version:
        print(version("pyvenus"))
        sys.exit()

def pyvenus_setup():
    parser = ArgumentParser()
    parser.add_argument("--example-method", dest="example_method", action="store_true")

    args = parser.parse_args()

    if args.example_method:
        dir = "example_method"
    else:
        dir = "default"

    if dir is not None:
        shutil.copytree(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), "setup_files", dir),
            os.getcwd()
        )
