from pathlib import Path
import yfinance as yf
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


def TickerData():

    config = getConfig()['yfinance']

    print(config['ticker'])



if __name__ == "__main__":
    TickerData()