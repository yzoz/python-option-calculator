import pytest
from bsm import BSM
from plot import Plot  # Import the Plot class

def test_call_option_pricing_positive_value():
    # Basic test to ensure the price of a call option is positive
    model = BSM()
    price = model.theo(S=100, K=90, V=0.2, T=1, dT='C')
    assert price > 0

def test_put_option_pricing_positive_value():
    # Basic test to ensure the price of a put option is positive
    model = BSM()
    price = model.theo(S=90, K=100, V=0.2, T=1, dT='P')
    assert price > 0

def test_call_option_price_higher_volatility():
    # Test to check if higher volatility results in a higher call option price
    model = BSM()
    low_vola_price = model.theo(S=100, K=100, V=0.1, T=1, dT='C')
    high_vola_price = model.theo(S=100, K=100, V=0.3, T=1, dT='C')
    assert high_vola_price > low_vola_price

def test_put_option_price_longer_maturity():
    # Test to check if longer time to maturity results in a higher put option price (in some cases)
    model = BSM()
    short_expiry_price = model.theo(S=100, K=100, V=0.2, T=0.5, dT='P')
    long_expiry_price = model.theo(S=100, K=100, V=0.2, T=1.5, dT='P')
    assert long_expiry_price > short_expiry_price

def test_invalid_option_type_raises_error():
    # Test to ensure an invalid option type raises an error
    model = BSM()
    with pytest.raises(ValueError, match="Tipo de opção inválido"):
        model.theo(S=100, K=100, V=0.2, T=1, dT='X')

def test_plot_pl_runs_without_error_basic_params():
    # Basic test to check if the P/L plotting function runs without error
    plotter = Plot()
    params = [{'dType': 'C', 'price': 1, 'quant': 1, 'strike': 105, 'vola': 0.2, 'exp': 1/365}]
    plotter.plotPL(bePriceS=90, bePriceF=110, params=params, exp=1/365, step=5)