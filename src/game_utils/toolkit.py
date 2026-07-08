#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
import zipfile

MODULE = "game_utils"
MODULE_IMPORT = f"{MODULE}-main"
URL = f"https://gitlab.com/madmadam/games/{MODULE}/-/archive/main/{MODULE_IMPORT}.zip"


def install_package():
    print("installing game-utils package into code base")
    path_ = os.path.curdir

    if os.path.isdir(os.path.join(path_, MODULE)):
        print(f"{MODULE} exists already")
        return

    zip_export_path = os.path.join(path_, f"{MODULE}.zip")

    # download the game_utils package
    subprocess.run(["wget", URL, "-qO", zip_export_path], check=True)

    # extract the download, and copy the module package here
    with zipfile.ZipFile(zip_export_path, "r") as zip_file:
        zip_file.extractall(path_)
        shutil.move(src=os.path.join(path_, MODULE_IMPORT, "src", MODULE), dst=path_)

        # delete job files
        os.remove(zip_export_path)
        shutil.rmtree(os.path.join(path_, MODULE_IMPORT))

    print("install complete")


def copy_demo_project():
    shutil.copy(os.path.join(os.path.dirname(__file__), "demo.py"), os.curdir)


if __name__ == "__main__":
    if len(sys.argv) == 2 and "--install" in sys.argv:
        install_package()

    if len(sys.argv) == 2 and "--sample-project" in sys.argv:
        print(f"copying sample project to {os.path.curdir}")
        copy_demo_project()
        print("copying complete...")

    if len(sys.argv) == 1:
        print("Game Utils Package")
        print("Toolkit usage:")
        help = "\n".join(
            [
                "--install\t\tinstall the library code into the code base",
                "--sample-project\tcopy the demo project and configurations to CWD",
            ]
        )
        print(help)
