import argparse

from package.load_module import loadJob
from package.run_module import runJob
from package.IO_module import print_color


def main():
    parser = argparse.ArgumentParser(
        description="Python client for Ivette Computational chemistry and Bioinformatics project"
    )

    # Creating a mutually exclusive group for 'load' and 'run' flags
    group = parser.add_mutually_exclusive_group()

    # Adding 'load' flag with a filename argument
    group.add_argument("--load", help="Load a file", metavar="filename")

    # Adding 'run' flag without any additional argument
    group.add_argument("--run", help="Run the program", action="store_true")

    args = parser.parse_args()

    # Header
    print_color("-" * 40, "32")
    print_color("IVETTE CLI", "32;1")  # 32 is the ANSI code for green, 1 makes it bold
    print_color("by Eduardo bogado (2023)", "34") # 34 blue
    print_color("-" * 40, "34")

    # Accessing the values of the mutually exclusive flags
    if args.load:
        loadJob(args.load)
    elif args.run:
        runJob()
    else:
        runJob()


if __name__ == "__main__":
    main()
