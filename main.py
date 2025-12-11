"""
Applies Deep Learning to infer stock prices from options data.

This script predicts the price of a generic stock. This is achieved
by feeding a set of options derived from the stock price to a 
Neural Network.

Option prices are computed using the Black-Scholes model, and the price
of the underlying asset is inferred from the options data. Parameters
such as strike price, stock volatility and maturity are relevant for
simulating the option prices, but are not handed over to the model.

The steps performed by the script are as follows:

1.  Generate synthetic stock price data using a drift-diffusion model.

2.  Simulate a range of call and put options based on the generated stock
    price data. Their price is computed using the Black-Scholes-model.

3.  Train a Neural Network to infer the price of the underlying asset
    from the generated options data.

The model is trained on the first 80% of intraday stock price data, and 
the performance is evaluated on the remaining 20%. The model's error is 
measured using the Root Mean Squared Error (RMSE), with a final RMSE
of a few cents.
"""

# Standard library and third-party imports
import numpy as np
import pandas as pd
import tensorflow as tf

# Local imports
from src.asset_classes import Stock, CallOption, PutOption
from src.math_models import stock_path, option_path
from src.decorators import timer


# GOAL: Find the price of a stock by training a Neural Network
# on the data of its call and put options.


# ================================================================
# STEP 1
# Generate synthetic stock prices.
# ================================================================

# Mathematical simulation of a Geometric Brownian Motion
df_stock = stock_path(random_state=55)
t, X = df_stock["time"], df_stock["price"]

# Store data in Stock instance
example_stock = Stock(t, X)

# Uncomment to save data in a CSV file
# example_stock.export(file_name="Stock_Price")

# Create a stock plot
# example_stock.plot(plot_title="Stock Price", plot_save_in_file=True)


# ================================================================
# STEP 2
# Generate the corresponding option paths.
# ================================================================

# Define the possible parameters for the options. For performance
# reasons, it is advised to keep the number of possible combinations low.
K_values = [8, 10, 12]
T_values = [0.5, 0.75]
sigma_values = [0.2, 0.3, 0.5]
option_types = ["call", "put"]

# Create the parameter space and count its members
param_space = [(K, T, sigma, option_type)
                  for K in K_values
                  for T in T_values
                  for sigma in sigma_values
                  for option_type in option_types]

option_dict = {}
option_count = 0

# Creating options from all parameter combinations
for K, T, sigma, option_type in param_space:
    option_count += 1

    # Create the time and price column for the option
    df_option = option_path(example_stock.time_grid,
                            example_stock.price_grid,
                            K, T, sigma,
                            option_type=option_type)

    t, X = df_option["time"], df_option["price"]

    if option_type == "call":
        # Save the result in a CallOption instance
        option_dict[option_count] = CallOption(t, X, T, K, sigma)

        # Uncomment to save result in a CSV file
        # option_dict[option_count].export(file_name=f"Call Option {option_count:03}")

        # Uncomment to save plots in PNG files
        # option_dict[option_count].plot(plot_title=f"Call Option {option_count:03}",
        #                                 plot_save_in_file=True)

    if option_type == "put":
        # Save the result in a PutOption instance
        option_dict[option_count] = PutOption(t, X, T, K, sigma)

        # Uncomment to save result in a CSV file
        # option_dict[option_count].export(file_name=f"Put Option {option_count:03}")

        # Uncomment to save plots in PNG files
        # option_dict[option_count].plot(plot_title=f"Put Option {option_count:03}",
        #                                plot_save_in_file=True)


# ================================================================
# STEP 3
# Create, train and evaluate a Neural Network on the data.
# ================================================================

# Build an adequate DataFrame for this purpose.
df_model = pd.DataFrame({"time": example_stock.time_grid})
for i in range(1, option_count + 1):
    option_prices = option_dict[i].price_grid
    df_model[f"option_{i:03}"] = option_prices
df_model["stock"] = example_stock.price_grid

# Building the model
deep_model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation='relu', input_shape=(option_count,)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)
])

# Splitting into training and test set
X_train, y_train = df_model.iloc[:800, 1:option_count+1], df_model.iloc[:800, -1]
X_test, y_test = df_model.iloc[800:, 1:option_count+1], df_model.iloc[800:, -1]

# Fitting the model to the first 80 % of intraday price data
# Note: Model knows nothing of the option parameters but the price!
deep_model.compile(optimizer='adam', loss='mse')

# Wrap this in a function to measure the time
@timer
def model_fit():
    return deep_model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)
model_fit()

# Measuring the error on the remaining 20 % of the day
loss = deep_model.evaluate(X_test, y_test)
print(f'\nRoot Mean Squared Error on test data: {np.sqrt(loss)}')
