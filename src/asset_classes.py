"""
A module for working with financial assets.

This module provides classes for the most common financial
asset types, including stocks, call and put options.

Functions
---------
plot_asset
    Creates a plot with asset data.
export_asset
    Creates a CSV file with the asset data.

Classes
-------
Asset
    A general asset.
Stock
    A stock share, subclass of Asset.
CallOption
    A European call option, subclass of Asset.
PutOption
    A European put option, subclass of Asset.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Specifying line colors for asset types
ASSET_COLOR = {"Asset": "black",
              "Stock": "black",
              "CallOption": "darkblue",
              "PutOption": "deepskyblue"}


def plot_asset(asset,
               plot_title: str = None,
               plot_save_in_file: bool = False) -> None:
    """Creates an exportable plot of an asset.

    Attributes
    ----------
    plot_title : str
        The title of the plot, and the name of the file.
    plot_save_in_file : bool
        Specifies whether to show or save the plot.
    """

    sns.set_theme(style="darkgrid")

    # Color of price line

    # Create a plot
    plt.figure(figsize=(12, 8))

    plot_color = ASSET_COLOR[asset.__class__.__name__]
    plt.plot(asset.time_grid, asset.price_grid,
             color=plot_color, lw=2)

    # Change appearance
    plt.grid(visible=True, linestyle="--", alpha=0.7)
    ax = plt.gca()
    ax.spines["left"].set_color("black")
    ax.spines["bottom"].set_color("black")

    # Labels and title
    plt.xlabel("\nTime", fontsize=14)
    plt.ylabel("Price\n", fontsize=14)

    # Default title
    if not plot_title:
        plot_title = "Asset price data\n"

    # Store in file when specified in function call
    if plot_save_in_file:
        plt.title(label=f"{plot_title}\n", fontsize=16)
        plt.savefig(f"./data/{plot_title.replace(' ', '_')}_plot.png", dpi=300)
        plt.close()
    else:
        plt.show()


def export_asset(asset,
                 file_name : str = None):
    """Export time series data of an asset.

    Attributes
    ----------
    file_name : str
        The first part of the name of the CSV file.
    """

    # Default title is asset type
    if file_name is None:
        file_name = asset.__class__.__name__

    pd.DataFrame({'time': asset.time_grid,
                  'price': asset.price_grid
                 }
                ).to_csv(path_or_buf = f"./data/{file_name.replace(' ', '_')}_data.csv",
                         index=False)



# The general asset and building block for all financial assets.
class Asset:
    """
    A general asset, i.e. a financial instrument.

    An asset contains time series data, i.e. a list of timestamps
    and a corresponding list of prices. It can be plotted and
    exported into a CSV file.


    Attributes
    ----------
    asset_type : str
        The type of the asset.
    time_grid : pd.Series
        List of times at which a price has been observed.
    price_grid : pd.Series
        List of observed prices at each point in time.

    Methods
    -------
    __init__(asset_id, price)
        Initializes an Asset instance.
    __str__()
        Provides a human-readable description of the asset.
    plot()
        Creates a plot of the asset data.
    export(title)
        Saves time and price grid to a CSV file.
    """

    def __init__(self,
                 time_grid: pd.Series,
                 price_grid: pd.Series) -> None:

        self.asset_type = "Asset"
        self.time_grid = time_grid
        self.price_grid = price_grid

    def __str__(self) -> str:
        """Provides a human-readable description of the asset."""
        return f"Asset type: {self.asset_type}"

    def plot(self,
             plot_title=None,
             plot_save_in_file=False):
        plot_asset(self,
                   plot_title=plot_title,
                   plot_save_in_file=plot_save_in_file)

    def export(self,
               file_name=None):
        export_asset(self,
                     file_name=file_name)



# The subclass for stocks.
class Stock(Asset):
    """
    A regular stock share.

    A stock represents a share in a company's equity. It is often
    the underlying asset for a call or a put option.

    Attributes
    ----------
    asset_type : str
        The type of the asset.
    time_grid : pd.Series
        List of times at which a price has been observed.
    price_grid : pd.Series
        List of observed prices at each point in time.

    Methods
    -------
    __init__(asset_id, price)
        Initializes a Stock instance.
    __str__()
        Provides a human-readable description of the stock.
    plot()
        Creates a plot of the asset data.
    export(title)
        Saves time and price grid to a CSV file.
    """

    def __init__(self,
                 time_grid: pd.Series,
                 price_grid: pd.Series) -> None:

        super().__init__(time_grid, price_grid)
        self.asset_type = "Stock"



# The subclass for call options.
class CallOption(Asset):
    """A European call option.

    A European call option gives the buyer a right to buy the
    underlying asset, often a stock, at a certain time for a
    certain price. These parameters are specified whenever a
    CallOption instance is created.

    Attributes
    ----------
        asset_type : str
            The type of the asset.
        time_grid : pd.Series
            List of times at which a price has been observed.
        price_grid : pd.Series
            List of observed prices at each point in time.
        strike : float
            The strike price of the call option, i.e. the price
            for which the underlying asset can be bought at maturity.
        maturity : float
            The time until maturity in years.
        volatility : float
            The volatility of the call option as a decimal.
            Example: 0.25 for a volatility of 25 %.

    Methods
    -------
    __init__(asset_id, price)
        Initializes a CallOption instance.
    __str__()
        Provides a human-readable description of the call option.
    plot()
        Creates a plot of the asset data.
    export(title)
        Saves time and price grid to a CSV file.
    """

    def __init__(self,
                 time_grid: pd.Series,
                 price_grid: pd.Series,
                 maturity: float,
                 strike: float,
                 volatility: float) -> None:

        super().__init__(time_grid, price_grid)
        self.asset_type = "Call Option"
        self.strike = strike
        self.maturity = maturity
        self.volatility = volatility



# The subclass for put options.
class PutOption(Asset):
    """A European put option.

        A European put option gives the buyer a right to sell the
        underlying asset, often a stock, at a certain time for a
        certain price. These parameters are specified whenever a
        PutOption instance is created.

        Attributes
        ----------
            asset_type : str
                The type of the asset.
            time_grid : pd.Series
                List of times at which a price has been observed.
            price_grid : pd.Series
                List of observed prices at each point in time.
            strike : float
                The strike price of the call option, i.e. the price
                for which the underlying asset can be bought at maturity.
            maturity : float
                The time until maturity in years.
            volatility : float
                The volatility of the call option as a decimal.
                Example: 0.25 for a volatility of 25 %.

        Methods
        -------
        __init__(asset_id, price)
            Initializes a CallOption instance.
        __str__()
            Provides a human-readable description of the call option.
        plot()
            Creates a plot of the asset data.
        export(title)
            Saves time and price grid to a CSV file.
        """

    def __init__(self,
                 time_grid: pd.Series,
                 price_grid: pd.Series,
                 maturity: float,
                 strike: float,
                 volatility: float) -> None:

        super().__init__(time_grid, price_grid)
        self.asset_type = "Put Option"
        self.strike = strike
        self.maturity = maturity
        self.volatility = volatility
