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
    print("Type '__HELP__' for more information")

    exit_shell = False

    while not exit_shell:
        try:
            src = input(f"\n{Colors.bright_black('>')} ")
        except KeyboardInterrupt:
            print("^C\nKeyboard Interrupt (to exit, type '__QUIT__')")
            continue

        if src == "__DOCS__":
            continue  # TODO: OPEN WEB DOCS

        if src == "__HELP__":
            print(
                """
__DOCS__         open documentation in your web browser
__INFO__         display version and platform information
__LICENSE__      display license
__HELP__         display this help text
__QUIT__         quit shell"""
            )
            continue

        if src == "__LICENSE__":
            if txt := get_license():
                print(f"\n{txt}")
            continue

        if src == "__QUIT__":
            exit_shell = True
            continue

        if src == "__INFO__":
            print(f"\n{release_info_str}")
            continue

        node, error = run(src)

        if error:
            print(error.generate_error_text())
            continue

        print(node)


if __name__ == "__main__":
    shell()
