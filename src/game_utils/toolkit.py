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
    path = os.getcwd()
    zip_export_path = os.path.join(path, f"{MODULE}.zip")

    # download the game_utils package
    subprocess.run(["wget", URL, "-qO", zip_export_path], check=True)

    # extract the download, and copy the module package here
    with zipfile.ZipFile(zip_export_path, "r") as zip_file:
        zip_file.extractall(path)
        shutil.move(src=os.path.join(path, MODULE_IMPORT, "src", MODULE), dst=path)

        # delete job files
        os.remove(zip_export_path)
        shutil.rmtree(os.path.join(path, MODULE_IMPORT))

    print("install complete")


def copy_demo_project():
    shutil.copy(os.path.join(os.path.dirname(__file__), "demo.py"), os.curdir)
    src = os.path.join(os.path.dirname(__file__), ".config")
    dst = os.path.join(os.getcwd(), ".config")
    if os.path.isdir(src):
        if os.path.exists(dst):
            # merge: copy contents into existing .config
            for root, dirs, files in os.walk(src):
                rel = os.path.relpath(root, src)
                target_root = os.path.join(dst, rel) if rel != "." else dst
                os.makedirs(target_root, exist_ok=True)
                for f in files:
                    shutil.copy2(os.path.join(root, f), os.path.join(target_root, f))
        else:
            shutil.copytree(src, dst)


if __name__ == "__main__":
    if len(sys.argv) == 2 and "--install" in sys.argv:
        install_package()

    if len(sys.argv) == 2 and "--sample-project" in sys.argv:
        copy_demo_project()

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
