from plot import Plot
import matplotlib.pyplot as plt

# Creates an instance of the Plot class, which inherits pricing functionalities
plot = Plot()

# Defines the number of days in a year (used to convert time for the BSM model)
god = 365
# Defines the price increment to generate points on the graphs
step = 10
# Defines the depth (range) of the price around the current price for the graphs
deep = 7500

# Defines different expiration times in years
exp = 30 / god   # Approximately 30 days
exp2 = 15 / god  # Approximately 15 days
exp3 = 5 / god   # Approximately 5 days

# Defines the current price (spot price) of the underlying asset
fPrice = 21000

# Initializes a list to store the parameters of the positions in the portfolio
params = []

# Adds a position of the underlying asset (F - Future/Forward)
params.append({
    'dType': 'F',       # Type: Future/Forward asset
    'quant': 1,         # Quantity: 1 (long 1 unit)
    'price': 20000,     # Purchase price of the asset
    'strike': 0,        # Strike not applicable for the asset
    'vola': 0,          # Volatility not applicable for the asset
    'exp': exp          # Expiration time (irrelevant for the asset, but needed in the structure)
})

# Adds a long position (buy - 1) of a call option (C - Call)
params.append({
    'dType': 'C',       # Type: Call Option
    'quant': 1,         # Quantity: 1 (long 1 contract)
    'price': 500,       # Premium paid for the option
    'strike': 25000,    # Strike Price
    'vola': 0.75,       # Implied Volatility (75%)
    'exp': exp          # Expiration time
})

# Adds a long position (buy - 1) of a put option (P - Put)
params.append({
    'dType': 'P',       # Type: Put Option
    'quant': 1,         # Quantity: 1 (long 1 contract)
    'price': 100,       # Premium paid for the option
    'strike': 15000,    # Strike Price
    'vola': 0.75,       # Implied Volatility (75%)
    'exp': exp          # Expiration time
})

# Adds a short position (sell - -1) of a put option (P - Put)
params.append({
    'dType': 'P',       # Type: Put Option
    'quant': -1,        # Quantity: -1 (short 1 contract)
    'price': 25,        # Premium received for selling the option
    'strike': 10000,    # Strike Price
    'vola': 1.5,        # Implied Volatility (150%)
    'exp': exp          # Expiration time
})

# Defines the lower and upper price limits for the graphs
bePriceS = fPrice - deep
bePriceF = fPrice + deep

# Plots the Profit/Loss (P/L) of the portfolio for different expiration times
plot.plotPL(bePriceS, bePriceF, params, exp, step)
plot.plotPL(bePriceS, bePriceF, params, exp2, step)
plot.plotPL(bePriceS, bePriceF, params, exp3, step)
plt.ylabel("P/L")
plt.xlabel("Price")
plt.title("Option")
plt.grid(True)
plt.legend()
plt.show()

# Plots the Delta of the portfolio for different expiration times
plot.plotDelta(bePriceS, bePriceF, params, exp, step)
plot.plotDelta(bePriceS, bePriceF, params, exp2, step)
plot.plotDelta(bePriceS, bePriceF, params, exp3, step)
plt.xlabel("Price")
plt.title("Option")
plt.grid(True)
plt.legend()
plt.ylabel("Delta")
plt.show()

# Plots the Theta of the portfolio for different expiration times
plot.plotTheta(bePriceS, bePriceF, params, exp, step)
plot.plotTheta(bePriceS, bePriceF, params, exp2, step)
plot.plotTheta(bePriceS, bePriceF, params, exp3, step)
plt.xlabel("Price")
plt.title("Option")
plt.grid(True)
plt.legend()
plt.ylabel("Theta")
plt.show()

# Plots the Vega of the portfolio for different expiration times
plot.plotVega(bePriceS, bePriceF, params, exp, step)
plot.plotVega(bePriceS, bePriceF, params, exp2, step)
plot.plotVega(bePriceS, bePriceF, params, exp3, step)
plt.xlabel("Price")
plt.title("Option")
plt.grid(True)
plt.legend()
plt.ylabel("Vega")
plt.show()

# Plots the Gamma of the portfolio for different expiration times
plot.plotGamma(bePriceS, bePriceF, params, exp, step)
plot.plotGamma(bePriceS, bePriceF, params, exp2, step)
plot.plotGamma(bePriceS, bePriceF, params, exp3, step)
plt.xlabel("Price")
plt.title("Option")
plt.grid(True)
plt.legend()
plt.ylabel("Gamma")
plt.show()

# Prints the aggregated (Full) values of the Greeks and P/L at the current price
print('Delta:\t', round(plot.deltaFull(fPrice, params, exp), 2))
print('Vega:\t', round(plot.vegaFull(fPrice, params, exp), 2))
print('Theta:\t', round(plot.thetaFull(fPrice, params, exp), 2))
print('Gamma:\t', round(plot.gammaFull(fPrice, params, exp), 2))
print('P/L:\t', plot.p_l(fPrice, params, exp))