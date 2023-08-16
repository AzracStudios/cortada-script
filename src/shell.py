import yaml
import platform
from os import path
from color import Colors
import readline  # enables arrow based text navigation

from main import *


def get_release_info() -> dict[str, dict[str, str]] | None:
    try:
        with open(path.abspath("release.yaml"), "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                return print(f"Release info broken: {exc}")
    except:
        return print("Release info not found")


def get_license() -> str | None:
    try:
        with open(path.abspath("LICENSE"), "r") as stream:
            try:
                return "".join(stream.readlines())
            except:
                return print("License broken / corrupted")
    except:
        return print("License not found")


def shell():
    info = get_release_info()
    assert info is not None
    info = info["data"]
    release_info_str = f"Cortada Script {info['version']} ({info['date']} version) on {platform.platform()}"

    print(release_info_str)
    print("Type 'help' for more information")

    exit_shell = False
    debug = False

    while not exit_shell:
        try:
            src = input(f"\n{Colors.bright_black('>')} ")
        except KeyboardInterrupt:
            print("^C\nKeyboard Interrupt (to exit, type 'quit')")
            continue

        if src == "docs":
            continue  # TODO: OPEN WEB DOCS

        if src == "help":
            print(
                """
debug        toggle debug mode to display tokens and ast
docs         open documentation in your web browser
info         display version and platform information
license      display license
help         display this help text
quit         quit shell"""
            )
            continue

        if src == "license":
            if txt := get_license():
                print(f"\n{txt}")
            continue

        if src == "debug":
            debug = not debug
            print(f"debug: {debug}")
            continue

        if src == "quit":
            exit_shell = True
            continue

        if src == "info":
            print(f"\n{release_info_str}")
            continue

        if len(src.replace(" ", "").replace("\t", "")) == 0:
            continue

        val, error = run(src, debug)

        if error:
            print(error.generate_error_text())
            continue

        print(val)


if __name__ == "__main__":
    shell()
