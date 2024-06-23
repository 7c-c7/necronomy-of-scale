import tomllib

with open("src/settings.toml", "rb") as settings_file:
    SETTINGS = tomllib.load(settings_file)

WINDOW = SETTINGS["window"]
