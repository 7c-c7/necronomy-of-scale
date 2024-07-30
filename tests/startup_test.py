import time


def test_startup(game_process):
    """
    Test that the game starts up without crashing.
    """
    time.sleep(2)
    assert game_process.poll() is None  # Check that the game is still running
