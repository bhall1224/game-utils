import os
import shutil

import game_utils.toolkit as toolkit


def test_toolkit():
    toolkit.install_package()
    path = os.path.join(os.path.dirname(os.curdir), "game_utils")
    assert os.path.exists(path)
    assert os.path.exists(os.path.join(path, "game.py"))
    shutil.rmtree(path)
