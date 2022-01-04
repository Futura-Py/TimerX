# CONFIG
import json

def loadConfig():
    with open('config.json') as config_file:
        config = json.load(config_file)
    return config

def setConfig(config):
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file)

def createConfig():
    with open('config.json', 'w') as config_file:
        json.dump({"theme": "Light", "notify": False, "ontop": False, "transperency": 1.0, "sound": True}, config_file)