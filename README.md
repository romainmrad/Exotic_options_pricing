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
- Variance reduction using stratified sampling

All simulations are based on geometric brownian motion modelling for stock prices
```math
dX_t=rXdt+\sigma XdW_t
```
Each time step of a trajectory is computed as follows, with $Z\sim\mathcal{N}(0,1)$
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
	Executing Stratified Sampling Monte-Carlo simulation

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

Pricing options using stratified simulation
	Pricing vanilla option
	Pricing asian arithmetic mean price option
	Pricing asian geometric mean price option
	Pricing knock-in barrier option
	Pricing knock-out barrier option
	Pricing lookback option

Results:
        Option type Naive simulation Antithetic simulation Stratified simulation
1           Vanilla             7.58                  6.17                  7.77
2  Asian arithmetic             2.07                  1.56                  2.17
3   Asian geometric             1.92                  1.45                  2.02
4          Knock-in             6.93                  5.33                  7.13
5         Knock-out             6.63                  5.74                  6.76
6          Lookback            27.19                 26.81                 27.74
```
