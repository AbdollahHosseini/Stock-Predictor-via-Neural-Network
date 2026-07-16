from pathlib import Path
import yaml

def getConfigPath():
    path = Path(__file__).parents[2] / "config/config.yaml"

    configFile = path.resolve()

    return configFile

def getConfig():

    configFile = getConfigPath()

    with open(configFile, 'r') as stream:
        config = yaml.full_load(stream)

    return config


