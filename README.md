# DeepPricing

![GitHub Repo](https://img.shields.io/badge/github-repo-blue?logo=github)
![GitHub repo size](https://img.shields.io/github/repo-size/wolfno/DeepPricing)
![GitHub contributors](https://img.shields.io/github/contributors/wolfno/DeepPricing)
![License](https://img.shields.io/github/license/wolfno/DeepPricing)

DeepPricing is a Neural Network tool that predicts stock prices from option data. <br> </br>

<img src="./github/nn.png">

By analyzing price data of a stock's financial derivatives, this tool calculates the price of the underlying stock. <br> </br>

## Prerequisites

In general, **you don't need to install anything**. Just click on **main.ipynb**.

If you would like to run the script yourself, ensure you have met the following requirements:
* You have installed Python 3.10 or higher.
* You are using Anaconda for Python package management.
* Currently, only Linux is supported if you want to export data such as CSV or PNG files. <br> </br>

## Installing DeepPricing

To install DeepPricing, follow these steps:

```
git clone https://github.com/wolfno/DeepPricing.git
```

To load the conda environment:

```
conda env create -f environment.yml
conda activate deeppricing
```

## Mathematical Models

View an explanation of the models [here](./src/README.md). <br> </br>

## Contributors

Thanks to the following people who have contributed to this project:

* [@scottydocs](https://github.com/scottydocs) for the README template. 📖
* [@alexlenail](https://github.com/alexlenail/NN-SVG) for the template of the Neural Network visualization. 🎨 <br> </br>

## License

This project uses the GNU GPL-3.0 license.
