import pytest
from bsm import BSM

def test_call_option_positive_price():
    # Test for positive call option price
    model = BSM()
    price = model.theo(S=100, K=90, V=0.2, T=1, dT='C')
    assert price > 0

def test_put_option_positive_price():
    # Test for positive put option price
    model = BSM()
    price = model.theo(S=90, K=100, V=0.2, T=1, dT='P')
    assert price > 0

def test_call_price_increases_with_volatility():
    # Test call price sensitivity to volatility
    model = BSM()
    low_vola = model.theo(S=100, K=100, V=0.1, T=1, dT='C')
    high_vola = model.theo(S=100, K=100, V=0.3, T=1, dT='C')
    assert high_vola > low_vola

def test_put_price_decreases_with_spot_price():
    # Test put price sensitivity to spot price
    model = BSM()
    high_spot = model.theo(S=110, K=100, V=0.2, T=1, dT='P')
    low_spot = model.theo(S=90, K=100, V=0.2, T=1, dT='P')
    assert low_spot > high_spot

def test_invalid_option_type_raises_value_error():
    # Test handling of invalid option type
    model = BSM()
    with pytest.raises(ValueError, match="Tipo de opção inválido"):
        model.theo(S=100, K=100, V=0.2, T=1, dT='X')

def test_negative_spot_price_raises_value_error():
    # Test handling of negative spot price
    model = BSM()
    with pytest.raises(ValueError, match="Preço à vista não pode ser negativo"):
        model.theo(-100, 100, 0.2, 1, 'C')