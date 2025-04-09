import configparser

import pandas as pd
import numpy as np
from scipy.stats import gmean


def empirical_variance(
    arr: np.ndarray,
    mean: float
) -> float:
    """
    Computes the empirical variance
    :param arr: the array
    :param mean: the mean of the array
    :return: the empirical variance
    """
    return sum((mean - e) ** 2 for e in arr) / (len(arr) - 1)


def confidence_interval(
    mean: float,
    sigma2: float,
    n: int
) -> str:
    """
    Computes the confidence interval
    :param mean: mean of the array
    :param sigma2: variance of the array
    :param n: size of the array
    :return: confidence interval
    """
    if sigma2 == 0:
        lb, ub = mean, mean
    else:
        lb = mean - np.sqrt(sigma2 / n)
        ub = mean + np.sqrt(sigma2 / n)
    return f'[{lb:>5.2f}, {ub:>5.2f}]'


def format_output_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Formats the output
    :param df: dataframe
    :return: Formatted dataframe
    """
    formatted_df = df.transpose()
    formatted_df.reset_index(inplace=True)
    formatted_df.drop(index=formatted_df.index[0], inplace=True)
    formatted_df.columns = ["Option type", "Naive simulation", "Antithetic simulation"]
    return formatted_df


def compute_vanilla_price(
    data: pd.DataFrame,
    config: configparser.ConfigParser,
    method: str
) -> float:
    """
    Compute price of a vanilla option
    :param data: Simulated trajectories
    :param config: Configuration parser object
    :param method: Simulation method
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
    payoffs = np.exp(-r * horizon) * np.maximum(final_prices - strike, 0)
    np.save(f"./data/payoffs/{method}_vanilla.npy", payoffs)
    return round(np.mean(payoffs), 3)


def compute_asian_arithmetic_price(
    data: pd.DataFrame,
    config: configparser.ConfigParser,
    method: str
) -> float:
    """
    Compute price of an arithmetic-average-price asian option
    :param data: Simulated trajectories
    :param config: Configuration parser object
    :param method: Simulation method
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
    payoffs = np.exp(-r * horizon) * np.maximum(means - strike, 0)
    np.save(f"./data/payoffs/{method}_asian_arithmetic.npy", payoffs)
    # Compute discounted price
    return round(np.mean(payoffs), 3)


def compute_asian_geometric_price(
    data: pd.DataFrame,
    config: configparser.ConfigParser,
    method: str
) -> float:
    """
    Compute price of a geometric-average-price asian option
    :param data: Simulated trajectories
    :param config: Configuration parser object
    :param method: Simulation method
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
    payoffs = np.exp(-r * horizon) * np.maximum(geometric_means - strike, 0)
    np.save(f"./data/payoffs/{method}_asian_geometric.npy", payoffs)
    # Compute discounted price
    return round(np.mean(payoffs), 3)


def compute_knock_in_price(
    data: pd.DataFrame,
    config: configparser.ConfigParser,
    method: str
) -> float:
    """
    Compute price of a knock-in barrier option using optimized operations.
    :param data: Simulated trajectories
    :param config: Configuration parser object
    :param method: Simulation method
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
    payoffs = []
    for col in data.columns:
        if any(data[col] > barrier):
            payoffs.append(np.exp(-r * horizon) * max(data[col].iloc[-1] - strike, 0))
    np.save(f"./data/payoffs/{method}_knock_in.npy", np.array(payoffs))
    return round(np.mean(payoffs), 3)


def compute_knock_out_price(
    data: pd.DataFrame,
    config: configparser.ConfigParser,
    method: str
) -> float:
    """
    Compute price of a knock-in barrier option using optimized operations.
    :param data: Simulated trajectories
    :param config: Configuration parser object
    :param method: Simulation method
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
    payoffs = []
    for col in data.columns:
        if all(data[col] < barrier):
            payoffs.append(np.exp(-r * horizon) * max(data[col].iloc[-1] - strike, 0))
    np.save(f"./data/payoffs/{method}_knock_out.npy", np.array(payoffs))
    return round(np.mean(payoffs), 3)


def compute_lookback_price(
    data: pd.DataFrame,
    config: configparser.ConfigParser,
    method: str
) -> float:
    """
    Compute price of a lookback option
    :param data: Simulated trajectories
    :param config: Configuration parser object
    :param method: Simulation method
    :return: Price of the option
    """
    print("\tPricing lookback option")
    # Load configuration
    horizon = config.getfloat('simulation', 'horizon')
    r = config.getfloat("simulation", "risk_free_rate")
    # Compute the strike prices (minima of each trajectory)
    strike = data.min(axis=0)
    # Compute the final prices (last value of each trajectory)
    final_prices = data.iloc[-1]
    # Compute the payoffs
    payoffs = np.exp(-r * horizon) * np.maximum(final_prices - strike, 0)
    np.save(f"./data/payoffs/{method}_lookback.npy", payoffs)
    return round(np.mean(payoffs), 3)


def compute_option_prices(config: configparser.ConfigParser) -> None:
    """
    Compute option prices for each option for each simulation
    :param config: Configuration parser object
    """
    simulation_methods = ["naive", "antithetic"]
    options = {
        "vanilla": compute_vanilla_price,
        "asian_arithmetic": compute_asian_arithmetic_price,
        "asian_geometric": compute_asian_geometric_price,
        "knock_in": compute_knock_in_price,
        "knock_out": compute_knock_out_price,
        "lookback": compute_lookback_price
    }
    for i, method in enumerate(simulation_methods):
        print(f"\nPricing options using {method} simulation")
        df = pd.read_csv(f'./data/simulations/{method}.csv')
        price_data = {"Simulation method": [method]}
        conf_int_data = {"Simulation method": [method]}
        for option_type in options.keys():
            price = options[option_type](df, config, method)
            price_data[option_type] = [price]
            payoffs = np.load(f"./data/payoffs/{method}_{option_type}.npy")
            conf_int_data[option_type] = [
                confidence_interval(
                    mean=price,
                    sigma2=empirical_variance(
                        arr=payoffs,
                        mean=price),
                    n=len(payoffs)
                )
            ]
        if i == 0:
            price_result = pd.DataFrame(price_data)
            conf_int_result = pd.DataFrame(conf_int_data)
        else:
            price_result = pd.concat([price_result, pd.DataFrame(price_data)])
            conf_int_result = pd.concat([conf_int_result, pd.DataFrame(conf_int_data)])
    price_result = format_output_df(price_result)
    conf_int_result = format_output_df(conf_int_result)
    print("\nResults:")
    print(str(price_result))
    print("\nConfidence intervals:")
    print(str(conf_int_result))
    price_result.to_csv('./data/prices.csv')
    conf_int_result.to_csv('./data/conf_int.csv')
