import subprocess
import sys

import pytest


@pytest.fixture
def game_process():
    game_process = subprocess.Popen([sys.executable, "src/nos/main.py"])
    yield game_process
    game_process.kill()
