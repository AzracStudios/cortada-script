import os
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="Cortada Script",
        description="An interpreted programming language written in python",
    )
    parser.add_argument("filename")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print out the tokens and abstract syntax tree along with the result",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="display the version of cortada script",
    )
    args = parser.parse_args()

    if not args.filename:
        print("Filename is required")


if __name__ == "__main__":
    main()
