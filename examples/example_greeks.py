from option_calculator import BSM

calc = BSM()

# Bitcoin example

S = 19500  # Underlying (price now)
K = 19000  # Strike
V = 0.45  # Implied Volatility (1 / 100%)
T = 0.55555 / 365  # Expiration date (days from now / 365)
dT = "P"  # Call / Put

print("Theo: ", round(calc.theo(S, K, V, T, dT), 2))
print("Delta: ", round(calc.delta(S, K, V, T, dT), 2))
print("Theta: ", round(calc.theta(S, K, V, T, dT), 2))
print("Vega: ", round(calc.vega(S, K, V, T), 2))
print("Gamma: ", round(calc.gamma(S, K, V, T), 2))
