import json

try:
    with open("config/config.json", "r") as config_file:
        data = json.load(config_file)
except FileNotFoundError:
    print("Config file not found. Continuing with default settings. To define a config file rename config/config.json.example to config.json and edit the example settings there.")
    data = {}

DATABASE_URI = data.get("database_uri")
