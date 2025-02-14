import json

def load_config():
    with open("config/config.json", "r") as file:
        return json.load(file)