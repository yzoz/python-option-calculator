from bsm import BSM

calc = BSM()

#Bitcoin example

S = 21000 #Underlying (price now)
K = 30000 #Strike
V = 0.75 #Implied Volatility (1 / 100%)
T = 30 / 365 #Expiration date (days from now / 365)
dT = "C" #Call / Put

print('Theo: ', round(calc.theo(S, K, V, T, dT), 2))
print('Delta: ', round(calc.delta(S, K, V, T, dT), 2))
print('Theta: ', round(calc.theta(S, K, V, T), 2))
print('Vega: ', round(calc.vega(S, K, V, T), 2))
print('Gamma: ', round(calc.gamma(S, K, V, T), 2))