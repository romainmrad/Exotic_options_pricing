from src.initialiser import fetch_data, load_configuration
from src.simulator import run_simulations
from src.pricer import compute_option_prices
import os

if __name__ == "__main__":
    os.makedirs("data/simulations", exist_ok=True)
    os.makedirs("data/payoffs", exist_ok=True)
    config = load_configuration()
    df = fetch_data(config)
    run_simulations(df, config)
    compute_option_prices(config)
