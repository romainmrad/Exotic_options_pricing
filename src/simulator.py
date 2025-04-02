import configparser

import pandas as pd
import numpy as np


def naive_simulation(data: pd.DataFrame, config: configparser.ConfigParser) -> None:
    """
    Naive Monte-Carlo simulation
    :param data: Stock price data
    :param config: Configuration parser object
    """
    print("\tExecuting Naive Monte-Carlo simulation")
    # Loading configuration
    r = config.getfloat("simulation", "risk_free_rate")
    horizon = int(1000 * config.getfloat("simulation", "horizon"))
    trading_days = config.getint("simulation", "trading_days")
    n_trajectories = config.getint("simulation", "n_trajectories")
    if config.getboolean("simulation", "use_seed"):
        np.random.seed(config.getint("simulation", "seed"))
    # Compute volatility and time step
    sigma = data.pct_change().std() * np.sqrt(trading_days)
    dt = 1 / trading_days
    S0 = float(data.iloc[-1])
    # Generate random shocks
    Z = np.random.randn(n_trajectories, horizon - 1)
    # Compute Brownian motion increments
    drift = (r - 0.5 * sigma ** 2) * dt
    diffusion = sigma * np.sqrt(dt) * Z
    increments = drift + diffusion
    # Compute price paths
    trajectories = np.zeros((n_trajectories, horizon))
    trajectories[:, 0] = S0
    trajectories[:, 1:] = S0 * np.exp(np.cumsum(increments, axis=1))
    # Save to CSV
    pd.DataFrame(trajectories.T).to_csv("data/simulations/naive.csv", index=False,
                                        header=[f'trajectory_{i}' for i in range(n_trajectories)])


def antithetic_simulation(config: configparser.ConfigParser) -> None:
    """
    Monte-Carlo simulation using antithetic data
    :param config: Configuration parser object
    """
    print("\tExecuting Antithetic variables Monte-Carlo simulation")
    # Load configuration
    proportion = config.getfloat("simulation", "antithetic_proportion")
    seed = None
    if config.getboolean("simulation", "use_seed"):
        seed = config.getint("simulation", "seed")
    # Load data
    data = pd.read_csv("data/simulations/naive.csv")
    # Sample columns based on proportion
    sampled_data = data.sample(
        n=int(data.shape[1] * proportion),
        axis=1,
        random_state=seed
    )
    # Compute antithetic paths
    S0 = sampled_data.iloc[0].to_numpy()  # Initial prices (first row)
    antithetic_values = 2 * S0 - sampled_data.to_numpy()
    # Create a new DataFrame with antithetic trajectories
    antithetic_data = pd.DataFrame(
        antithetic_values,
        columns=[f'antithetic_{col}' for col in sampled_data.columns]
    )
    # Concatenate and save
    result = pd.concat([sampled_data, antithetic_data], axis=1)
    result.to_csv("data/simulations/antithetic.csv", index=False)


def stratified_sampling_simulation(data: pd.DataFrame, config: configparser.ConfigParser) -> None:
    """
    Monte-Carlo simulation using stratified sampling
    :param data: Stock price data
    :param config: Configuration parser object
    """
    print("\tExecuting Stratified Sampling Monte-Carlo simulation")
    # Loading configuration
    r = config.getfloat("simulation", "risk_free_rate")
    horizon = int(1000 * config.getfloat("simulation", "horizon"))
    trading_days = config.getint("simulation", "trading_days")
    n_trajectories = config.getint("simulation", "n_trajectories")
    n_strata = config.getint("simulation", "n_strata")
    if config.getboolean("simulation", "use_seed"):
        np.random.seed(config.getint("simulation", "seed"))
    # Compute volatility and time step
    sigma = data.pct_change().std() * np.sqrt(trading_days)
    dt = 1 / trading_days
    S0 = float(data.iloc[-1])
    # Stratified sampling: divide the range of S0 into n_strata intervals
    strata_limits = np.linspace(S0 * 0.8, S0 * 1.2, n_strata + 1)
    # Generate random shocks
    Z = np.random.randn(n_trajectories, horizon - 1)
    # Compute Brownian motion increments
    drift = (r - 0.5 * sigma ** 2) * dt
    diffusion = sigma * np.sqrt(dt) * Z
    increments = drift + diffusion
    # Compute price paths
    trajectories = np.zeros((n_trajectories, horizon))
    # Stratified sampling: assign each trajectory to a stratum
    for i in range(n_trajectories):
        # Determine the stratum for the current trajectory
        stratum = np.digitize(S0, strata_limits) - 1
        # Generate trajectory based on the assigned stratum
        S0_stratum = np.random.uniform(strata_limits[stratum], strata_limits[stratum + 1])
        trajectories[i, 0] = S0_stratum
        trajectories[i, 1:] = S0_stratum * np.exp(np.cumsum(increments[i], axis=0))
    # Save to CSV
    pd.DataFrame(trajectories.T).to_csv("data/simulations/stratified.csv", index=False,
                                        header=[f'trajectory_{i}' for i in range(n_trajectories)])


def run_simulations(data: pd.DataFrame, config: configparser.ConfigParser) -> None:
    """
    Run simulations
    :param data: Stock price data
    :param config: Configuration parser object
    """
    print("\nExecuting simulations")
    naive_simulation(data, config)
    antithetic_simulation(config)
    stratified_sampling_simulation(data, config)
