import configparser

import pandas as pd
import numpy as np
from scipy.stats import gmean


def compute_vanilla_price(data: pd.DataFrame, config: configparser.ConfigParser) -> float:
    """
    Compute price of a vanilla option
    :param data: Simulated trajectories
    :param config: Configuration parser object
    :return: Price of the option
    """
    print("\tPricing vanilla option")
    # Load configuration
    horizon = config.getfloat('simulation', 'horizon')
    r = config.getfloat("simulation", "risk_free_rate")
    multiplier = config.getfloat("option", "strike_multiplier")
    # Compute price
    strike = data.iloc[0, 0] * multiplier
    final_prices = data.iloc[-1]  # Last price of each trajectory
    payoffs = np.maximum(final_prices - strike, 0)
    return round(np.exp(-r * horizon) * np.mean(payoffs), 2)


# def compute_american_price(data: pd.DataFrame, config: configparser.ConfigParser) -> float:
#     """
#     Compute price of an american option
#     :param data: Simulated trajectories
#     :param config: Configuration parser object
#     :return: Price of the option
#     """
#     # Load configuration
#     horizon = config.getfloat('simulation', 'horizon')
#     r = config.getfloat("simulation", "risk_free_rate")
#     multiplier = config.getfloat("option", "strike_multiplier")
#     minimum_exercise_profit = config.getfloat("option", "minimum_exercise_profit")
#     # Compute price
#     strike = data.iloc[0, 0] * multiplier
#     s = 0
#     N = data.shape[1]
#     for col in data.columns:
#         trajectory = data[col].to_numpy()
#         trajectory = trajectory[trajectory > strike + minimum_exercise_profit]
#         if len(trajectory) > 0:
#             s += trajectory[0] - strike
#     return np.exp(-r * horizon) * s / N


def compute_asian_arithmetic_price(data: pd.DataFrame, config: configparser.ConfigParser) -> float:
    """
    Compute price of an arithmetic-average-price asian option
    :param data: Simulated trajectories
    :param config: Configuration parser object
    :return: Price of the option
    """
    print("\tPricing asian arithmetic mean price option")
    # Load configuration
    horizon = config.getfloat('simulation', 'horizon')
    r = config.getfloat("simulation", "risk_free_rate")
    multiplier = config.getfloat("option", "strike_multiplier")
    # Compute strike price
    strike = data.iloc[0, 0] * multiplier
    # Compute the arithmetic means for all trajectories
    means = data.mean()
    # Compute the payoff for each trajectory and then compute the average
    payoffs = np.maximum(means - strike, 0)
    # Compute discounted price
    return round(np.exp(-r * horizon) * np.mean(payoffs), 2)


def compute_asian_geometric_price(data: pd.DataFrame, config: configparser.ConfigParser) -> float:
    """
    Compute price of a geometric-average-price asian option
    :param data: Simulated trajectories
    :param config: Configuration parser object
    :return: Price of the option
    """
    print("\tPricing asian geometric mean price option")
    # Load configuration
    horizon = config.getfloat('simulation', 'horizon')
    r = config.getfloat("simulation", "risk_free_rate")
    multiplier = config.getfloat("option", "strike_multiplier")
    # Compute strike price
    strike = data.iloc[0, 0] * multiplier
    # Compute geometric means for all trajectories
    geometric_means = np.apply_along_axis(gmean, axis=0, arr=data.values)
    # Compute the payoff for each trajectory
    payoffs = np.maximum(geometric_means - strike, 0)
    # Compute discounted price
    return round(np.exp(-r * horizon) * np.mean(payoffs), 2)


def compute_knock_in_price(data: pd.DataFrame, config: configparser.ConfigParser) -> float:
    """
    Compute price of a knock-in barrier option using optimized operations.
    :param data: Simulated trajectories
    :param config: Configuration parser object
    :return: Price of the option
    """
    print("\tPricing knock-in barrier option")
    # Load configuration
    horizon = config.getfloat('simulation', 'horizon')
    r = config.getfloat("simulation", "risk_free_rate")
    strike_multiplier = config.getfloat("option", "strike_multiplier")
    barrier_multiplier = config.getfloat("option", "knock_in_barrier_multiplier")
    # Compute strike and barrier prices
    strike = data.iloc[0, 0] * strike_multiplier
    barrier = data.iloc[0, 0] * barrier_multiplier
    N = data.shape[1]
    s = 0
    for col in data.columns:
        if any(data[col] > barrier):
            s += max(data[col].iloc[-1] - strike, 0)
    return round(np.exp(-r * horizon) * s / N, 2)


def compute_knock_out_price(data: pd.DataFrame, config: configparser.ConfigParser) -> float:
    """
    Compute price of a knock-in barrier option using optimized operations.
    :param data: Simulated trajectories
    :param config: Configuration parser object
    :return: Price of the option
    """
    print("\tPricing knock-out barrier option")
    # Load configuration
    horizon = config.getfloat('simulation', 'horizon')
    r = config.getfloat("simulation", "risk_free_rate")
    strike_multiplier = config.getfloat("option", "strike_multiplier")
    barrier_multiplier = config.getfloat("option", "knock_out_barrier_multiplier")
    # Compute strike and barrier prices
    strike = data.iloc[0, 0] * strike_multiplier
    barrier = data.iloc[0, 0] * barrier_multiplier
    N = data.shape[1]
    s = 0
    for col in data.columns:
        if all(data[col] < barrier):
            s += max(data[col].iloc[-1] - strike, 0)
    return round(np.exp(-r * horizon) * s / N, 2)


def compute_lookback_price(data: pd.DataFrame, config: configparser.ConfigParser) -> float:
    """
    Compute price of a lookback option
    :param data: Simulated trajectories
    :param config: Configuration parser object
    :return: Price of the option
    """
    print("\tPricing lookback option")
    # Load configuration
    horizon = config.getfloat('simulation', 'horizon')
    r = config.getfloat("simulation", "risk_free_rate")
    # Compute the strike prices (minima of each trajectory)
    strike = data.min(axis=0)  # Vectorized: minimum of each column
    # Compute the final prices (last value of each trajectory)
    final_prices = data.iloc[-1]
    # Compute the payoffs: max(final_price - strike, 0) for each trajectory
    payoffs = np.maximum(final_prices - strike, 0)
    return round(np.exp(-r * horizon) * np.mean(payoffs), 2)


def compute_option_prices(config: configparser.ConfigParser) -> None:
    """
    Compute option prices for each option for each simulation
    :param config: Configuration parser object
    """
    simulation_methods = ["naive", "antithetic", "stratified"]
    for i, method in enumerate(simulation_methods):
        print(f"\nPricing options using {method} simulation")
        df = pd.read_csv(f'./data/simulations/{method}.csv')
        data = {
            "Simulation method": [method],
            "Vanilla": [compute_vanilla_price(df, config)],
            # "American": [compute_american_price(df, config)],
            "Asian arithmetic": [compute_asian_arithmetic_price(df, config)],
            "Asian geometric": [compute_asian_geometric_price(df, config)],
            "Knock-in": [compute_knock_in_price(df, config)],
            "Knock-out": [compute_knock_out_price(df, config)],
            "Lookback": [compute_lookback_price(df, config)]
        }
        if i == 0:
            result = pd.DataFrame(data)
        else:
            result = pd.concat([result, pd.DataFrame(data)])
    result = result.transpose()
    result.reset_index(inplace=True)
    result.drop(index=result.index[0], inplace=True)
    result.columns = ["Option type", "Naive simulation", "Antithetic simulation", "Stratified simulation"]
    print("\nResults:")
    print(str(result))
    result.to_csv('./data/prices.csv')
