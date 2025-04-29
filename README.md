# Vanilla options calculator
## Black-Scholes model in pure Python 
### Without SciPy, NumPy or other external dependencies

# PyOption Pricing & Greeks

This project provides a set of tools in Python for calculating the theoretical price of options using the Black-Scholes-Merton (BSM) model, as well as the main Greeks (Delta, Vega, Theta, and Gamma). Additionally, it offers functionalities to visualize the P&L (Profit and Loss) and the Greeks of an option portfolio under different price scenarios and expiration dates.

## Key Features

* **Option Pricing:** Implementation of the Black-Scholes-Merton model to calculate the theoretical price of call and put options.
* **Greeks Calculation:** Provides functions to calculate option sensitivities:
    * **Delta ($\Delta$):** Measures the sensitivity of the option price to a change in the underlying asset price.
    * **Vega ($\nu$):** Measures the sensitivity of the option price to a change in the implied volatility of the underlying asset.
    * **Theta ($\Theta$):** Measures the sensitivity of the option price to the passage of time (time decay).
    * **Gamma ($\Gamma$):** Measures the rate of change of Delta with respect to a change in the underlying asset price.
* **Portfolio Analysis:** Allows for the analysis of a portfolio composed of multiple options and the underlying asset, calculating the total Greeks and P&L of the portfolio.
* **Graphical Visualization:** Utilizes the `matplotlib` library to generate graphs of:
    * Portfolio P&L as a function of the underlying asset price for different expiration dates.
    * The Greeks (Delta, Theta, Vega, Gamma) of the portfolio as a function of the underlying asset price for different expiration dates.
* **(In Development) Delta Neutral Search:** The `searching.py` module appears to contain in-development functionalities for finding prices where a specific individual option neutralizes the portfolio's Delta.

## How to Use

### Prerequisites

* Python 3.x
* `matplotlib` library

### Installation

1.  Ensure you have Python 3 installed on your system.
2.  Install the `matplotlib` library using pip if you haven't already:
    ```bash
    pip install matplotlib
    ```

### Usage Examples

1.  **Calculating Greeks for an Option:** Run the `exemple_greeks.py` script:
    ```bash
    python exemple_greeks.py
    ```
    This script demonstrates how to instantiate the `BSM` class and calculate the theoretical price, Delta, Theta, Vega, and Gamma for a Bitcoin option with example parameters.

2.  **Visualizing Portfolio P&L and Greeks:** Run the `exemple_plot.py` script:
    ```bash
    python exemple_plot.py
    ```
    This script uses the `Plot` class to generate graphs showing the P&L, Delta, Theta, Vega, and Gamma of an option portfolio defined within the script, across different expiration dates. The legends on the graphs indicate the number of days until expiration.

3.  **(In Development) Delta Neutral Search:** The `searching.py` script contains a `Search` class with a `searchDelta` method. To use it (remember it's under development), you can execute the script and observe the output:
    ```bash
    python searching.py
    ```
    The output displays a table with the underlying asset price, option type, strike price, quantity, individual option Delta, total portfolio Delta, and the theoretical option price, searching for points where the individual option's Delta offsets the total portfolio Delta.

## Project Structure

* `bsm.py`: Contains the implementation of the `BSM` class with methods to calculate the theoretical price (theo), the Greeks (delta, vega, theta, gamma), and the standard normal distribution functions (pdf and cdf).
* `pricing.py`: Extends the `BSM` class and implements methods to calculate the total Greeks (`deltaFull`, `vegaFull`, `thetaFull`, `gammaFull`) and the P&L (`p_l`) of a portfolio of assets and options.
* `plot.py`: Utilizes the `Pricing` class and the `matplotlib` library to generate graphs of the portfolio's P&L and Greeks as a function of the underlying asset price for different expiration dates.
* `exemple_greeks.py`: An example script demonstrating how to use the `BSM` class to calculate the Greeks of a single option.
* `exemple_plot.py`: An example script that uses the `Plot` class to generate graphical visualizations of an option portfolio.
* `searching.py`: A script containing a `Search` class with functionalities under development to assist in finding delta-neutral positions, comparing the delta of an individual option with the total portfolio delta.

## Contributing

Contributions are welcome! Feel free to open issues to report bugs or suggest improvements, and submit pull requests with your implementations.