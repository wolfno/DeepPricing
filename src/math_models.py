"""
A module containing mathematical models for financial assets.

This module provides models for the stocks and options
as defined in the asset_classes module. It contains a
Black-Scholes model for computing option prices and a
Geometric Brownian motion for simulating stock paths.

Functions
---------
black_scholes_price(S0, X, T, sigma, r)
    Compute the current theoretical price of an option.
stock_path(T, n_steps, x0, mu, sigma, random_state)
    Simulates an intraday course of a stock.
option_path(t_grid, S_grid, K, T, r, sigma, option_type, random_state)
    Simulates the intraday course of an option.

Attributes
----------
RISK_FREE
    The assumed default risk-free interest rate.
"""

import numpy as np
import pandas as pd
from numpy import ndarray, dtype, floating
from scipy.stats import norm


# The risk-free interest rate used by default throughout the models.
# Whenever a function from this module is called without specifying r,
# Python's namespace checks for this parameter in this very module.

# Currently, 2.0 % as per the German 7-year bond (DE000BU22114).
RISK_FREE = 0.02


def black_scholes_price(S0: float,
                        K: float,
                        T: float,
                        sigma: float,
                        option_type: str,
                        r: float = RISK_FREE) -> float | None:
    """
    Compute the theoretical price for a given call option.

    The Black-Scholes model is used to calculate the fair price of an
    option, given the parameters described below. This function returns
    this theoretical value, NOT any actual current value the option
    may have on the market. The nomenclature of the variables is based
    on the mathematical conventions for the model.

    Parameters
    ----------
    S0 : float
        The market price of the underlying stock.
    K : float
        The strike price of the option.
    T : float
        The remaining time until maturity in years.
    sigma : float
        The volatility of the option.
    option_type : str
        "call" or "put", type of the option.
    r : float
        The current annual risk-free interest rate.

    Returns
    -------
    float
        The current Black-Scholes price of the option.
    """

    if option_type == "call":
        d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

    if option_type == "put":
        d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)

    return None


def stock_path(T: float = 1.0,
               n_steps: int = 1000,
               x0: float = 10.0,
               mu: float = 0.01,
               sigma: float = 0.5,
               random_state: int | None = None) -> pd.DataFrame:
    """
    Simulate one realization of the following SDE on [0, T]:
    dXt = mu Xt dt + sigma Xt dWt.

    The Geometric Brownian motion is used here to model the course
    of a general stock during the time [0, T]. The nomenclature
    follows mathematical conventions.


    Parameters
    ----------
    T : float
        Final time, starting from zero.
    n_steps : int
        Number of time steps for discretization.
    x0 : float
        Initial price X[0].
    mu : float
        Drift coefficient.
    sigma : float
        Diffusion (volatility) coefficient.
    random_state : int or None
        Seed for reproducibility.

    Returns
    -------
    t_grid : ndarray
        Discretized time grid.
    X_grid : ndarray
        Simulated path values.
    """

    # Initialize random state for reproducibility
    rng = np.random.default_rng(seed=random_state)

    # Discretize the time frame
    dt = T / n_steps
    t_grid = np.linspace(0.0, T, n_steps + 1)

    # Simulate a Brownian motion with N(0, sqrt(dt)) increments
    dW = rng.normal(loc=0.0, scale=np.sqrt(dt), size=n_steps)

    # X_grid[i] represents the price of the stock at time i
    X_grid = np.zeros(n_steps + 1)
    X_grid[0] = x0

    for i in range(n_steps):
        X_grid[i + 1] = X_grid[i] * np.exp(
            (mu - 0.5 * sigma**2) * dt + sigma * dW[i]
        )

    return pd.DataFrame({"time": t_grid, "price": X_grid})


def option_path(t_grid: pd.Series,
                S_grid: pd.Series,
                K: float,
                T: float,
                sigma: float,
                option_type: str,
                r: float = RISK_FREE) -> pd.DataFrame:
    """
    Simulate one intraday price data of an option.

    The Black-Scholes model is used here to model the course of
    a general option throughout a trading day. The nomenclature
    follows mathematical conventions.


    Parameters
    ----------
    t_grid : pd.Series of dtype float64
        Time grid of the underlying asset.
        Must be of same length as S_grid.
    S_grid : pd.Series of dtype float64
        Price of the underlying asset at times t_grid.
        Must be of same length as t_grid.
    K : float
        The strike price of the option.
    T : float
        Time in years until maturity of the option.
    sigma : float
        Volatility coefficient of the underlying asset.
    option_type : str
        "call" or "put", type of the option.
    r : float
        Assumed risk-free interest rate.

    Returns
    -------
    DataFrame ["time", "price"]
    """

    n = len(t_grid)
    X_grid = np.zeros(n)

    if option_type == "call":
        for i in range(n):
            X_grid[i] = black_scholes_price(
                S_grid[i], K, T, sigma, "call", r)
    elif option_type == "put":
        for i in range(n):
            X_grid[i] = black_scholes_price(
                S_grid[i], K, T, sigma, "put", r)

    return pd.DataFrame({"time": t_grid, "price": X_grid})

