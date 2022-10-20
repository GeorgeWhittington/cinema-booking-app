import json

with open("config/config.json", "r") as config_file:
    data = json.load(config_file)

DATABASE_URI = data.get("database_uri")
