import configparser

import pandas as pd
import yfinance as yf


def load_configuration(config_file: str = "config.ini") -> configparser.ConfigParser:
    """
    Loads configuration from json file
    :param config_file: path to configuration file
    :return: configuration dictionary
    """
    print("Loading configuration")
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def fetch_data(config: configparser.ConfigParser) -> pd.Series or pd.DataFrame:
    """
    Downloads data from yahoo and saves it in a pandas DataFrame
    :return: data frame
    """
    print("Fetching data")
    ticker = config.get("general", "default_ticker")
    if config.getboolean("general", "ask_ticker"):
        ticker = str(input("Enter ticker symbol: "))
    data = yf.download(ticker, period="10y", auto_adjust=True)['Close']
    return pd.Series(
        data=data[ticker].tolist(),
        index=data.index.tolist(),
        name="Price"
    )
