#!/usr/bin/env python3

import os
import shutil
import subprocess
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


if __name__ == "__main__":
    install_package()
