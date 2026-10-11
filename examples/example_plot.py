from plot import Plot
import matplotlib.pyplot as plt

plot = Plot()

god = 365
step = 10
deep = 7500

exp = 30 / god
exp2 = 15 / god
exp3 = 5 / god

fPrice = 21000

params = []

dType = 'F'
quant = 1
price = 20000
strike = 0
vola = 0
params.append({'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp})

dType = 'C'
quant = 1
price = 500
strike = 25000
vola = 0.75
params.append({'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp})

dType = 'P'
quant = 1
price = 100
strike = 15000
vola = 0.75
params.append({'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp})

dType = 'P'
quant = -1
price = 25
strike = 10000
vola = 1.5
params.append({'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp})

bePriceS = fPrice - deep
bePriceF = fPrice + deep

plot.plotPL(bePriceS, bePriceF, params, exp, step)
plot.plotPL(bePriceS, bePriceF, params, exp2, step)
plot.plotPL(bePriceS, bePriceF, params, exp3, step)
plt.ylabel("P/L")
plt.xlabel("Price")
plt.title("Option")
plt.grid(True)
plt.legend()
plt.show()

plot.plotDelta(bePriceS, bePriceF, params, exp, step)
plot.plotDelta(bePriceS, bePriceF, params, exp2, step)
plot.plotDelta(bePriceS, bePriceF, params, exp3, step)
plt.xlabel("Price")
plt.title("Option")
plt.grid(True)
plt.legend()
plt.ylabel("Delta")
plt.show()

plot.plotTheta(bePriceS, bePriceF, params, exp, step)
plot.plotTheta(bePriceS, bePriceF, params, exp2, step)
plot.plotTheta(bePriceS, bePriceF, params, exp3, step)
plt.xlabel("Price")
plt.title("Option")
plt.grid(True)
plt.legend()
plt.ylabel("Theta")
plt.show()

plot.plotVega(bePriceS, bePriceF, params, exp, step)
plot.plotVega(bePriceS, bePriceF, params, exp2, step)
plot.plotVega(bePriceS, bePriceF, params, exp3, step)
plt.xlabel("Price")
plt.title("Option")
plt.grid(True)
plt.legend()
plt.ylabel("Vega")
plt.show()

plot.plotGamma(bePriceS, bePriceF, params, exp, step)
plot.plotGamma(bePriceS, bePriceF, params, exp2, step)
plot.plotGamma(bePriceS, bePriceF, params, exp3, step)
plt.xlabel("Price")
plt.title("Option")
plt.grid(True)
plt.legend()
plt.ylabel("Gamma")
plt.show()


print('D:\t', round(plot.deltaFull(fPrice, params, exp), 2))

print('V:\t', round(plot.vegaFull(fPrice, params, exp), 2))

print('T:\t', round(plot.thetaFull(fPrice, params, exp), 2))

print('G:\t', round(plot.gammaFull(fPrice, params, exp), 2))

print('P/L:\t', plot.p_l(fPrice, params, exp))