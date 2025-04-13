# Exotic options pricing project

This project aims to implement risk-neutral pricing for some of the most well-known exotic derivatives using
Monte-Carlo simulations.

## Requirements

This project uses the following python packages

```requirements
pandas>=2.2.3
numpy>=2.2.4
scipy>=1.15.2
yfinance>=0.2.55
```

## Specifications

The implemented call options are:

- Vanilla
- Asian arithmetic mean price
- Asian geometric mean price
- Knock-in
- Knock-out
- Lookback

We use three different Monte-Carlo simulation techniques:

- Naive simulations
- Variance reduction using antithetic variables

All simulations are based on geometric brownian motion modelling for stock prices
```math
dX_t=rXdt+\sigma XdW_t
```
Each time step of a trajectory is computed as follows, with $Z\sim\mathcal{N}(0,1)$ and $\sigma$ the historical volatility
```math
S_t=S_0e^{(r-\frac{1}{2}\sigma^2)t+\sigma\sqrt{t}Z}
```

## Configuration

In the [configuration file](config.ini), the user can modify the project parameters:

- The `option` parameters:
    - `strike_multiplier` is what is used to compute the strike price (by multiplying the initial price)
    - `knock_in_barrier_multiplier` is what is used to compute the knock-in barrier
    - `knock_out_barrier_multiplier` is what is used to compute the knock-out barrier
- The `simulation` parameters:
    - `trading_days` the number of trading days
    - `risk_free_rate` the risk-free rate
    - `use_seed` boolean to indicate if a seed should be used for random generations
    - `seed` the seed value
    - `horizon` option maturity in years
    - `n_trajectories` number of simulated trajectories
    - `n_strata` number of stratas for stratified sampling
    - `antithetic_proportion` proportion of antithetic variables to generate

## Functioning

For each trajectory, the program will compute it's future cash-flow at T $CF_T$.
The value of the option is then computed by discounting the expected cash-flow at the risk-free
rate
```math
C=e^{-rT}\mathbb{E}[CF_T]
```

The results are printed in the console and saved in the data folder under `prices.csv`.

## Sequence diagram

You can find the different sequence diagrams versions here
- [Plant UML file](docs/sequence.puml)
- [PDF file](docs/sequence.pdf)
- [SVG file (displayed belowed)](docs/sequence.svg)

![](docs/sequence.svg)

## Example output

Here is an example output of the program with the user inputing stock ticker `AAPL` (Apple)


```shell
Loading configuration
Fetching data
Enter ticker symbol: AAPL
[*********************100%***********************]  1 of 1 completed

Executing simulations
	Executing Naive Monte-Carlo simulation
	Executing Antithetic variables Monte-Carlo simulation

Pricing options using naive simulation
	Pricing vanilla option
	Pricing asian arithmetic mean price option
	Pricing asian geometric mean price option
	Pricing knock-in barrier option
	Pricing knock-out barrier option
	Pricing lookback option

Pricing options using antithetic simulation
	Pricing vanilla option
	Pricing asian arithmetic mean price option
	Pricing asian geometric mean price option
	Pricing knock-in barrier option
	Pricing knock-out barrier option
	Pricing lookback option

Results:
        Option type Naive simulation Antithetic simulation
1           vanilla            7.127                  5.77
2  asian_arithmetic            2.045                 1.554
3   asian_geometric            1.899                 1.447
4          knock_in            1.045                 0.534
5         knock_out            6.082                 5.236
6          lookback           24.818                24.441

Confidence intervals:
        Option type Naive simulation Antithetic simulation
1           vanilla   [ 7.01,  7.24]        [ 5.67,  5.87]
2  asian_arithmetic   [ 2.00,  2.09]        [ 1.52,  1.59]
3   asian_geometric   [ 1.86,  1.94]        [ 1.41,  1.48]
4          knock_in   [ 0.98,  1.11]        [ 0.48,  0.58]
5         knock_out   [ 5.99,  6.18]        [ 5.15,  5.32]
6          lookback   [24.66, 24.98]        [24.30, 24.59]
```
