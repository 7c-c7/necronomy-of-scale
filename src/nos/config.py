import json
import tomllib
import typing
from abc import ABC
from pathlib import Path

with open("src/settings.toml", "rb") as settings_file:
    SETTINGS = tomllib.load(settings_file)

WINDOW = SETTINGS["window"]

GAME = SETTINGS["game"]

#  TODO: add a Moddable mixin to allow for easy modding of the game by specifying a new entity with a JSON file.


class Moddable(ABC):
    @classmethod
    def from_json(cls, path: Path) -> typing.Self | None:
        try:
            with open(path, "rb") as json_file:
                details = json.load(json_file)
            return type(details["class"], (cls,), details["attributes"])
        except FileNotFoundError:
            raise UserWarning(f"File {path} not found. Will not load modded entity.")
        except KeyError as error:
            raise UserWarning(
                f"File {path} does not contain the required keys.\n"
                f"{error}\n"
                f"Will not load modded entity."
            )
        except json.JSONDecodeError:
            raise UserWarning(
                f"File {path} is not a valid JSON file. Will not load modded entity."
            )
