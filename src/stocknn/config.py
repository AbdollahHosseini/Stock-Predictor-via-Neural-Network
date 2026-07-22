from pathlib import Path
import yaml

def getConfig():

    path = Path(__file__).parents[2] / "config/config.yaml"

    configFile = path.resolve()

    with open(configFile, 'r') as stream:
        config = yaml.full_load(stream)

    return config
    
def getPath(fileType, ticker):

    root = Path(__file__).parents[2]
    path = root / f"data/{fileType}/{ticker}_data.csv"
    return path.resolve()