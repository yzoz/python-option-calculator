import pytest
from bsm import BSM
import matplotlib.pyplot as plt
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

# Supondo que a função plotPL retorna a figura ou os eixos para inspeção (idealmente)
# Se não retornar, podemos apenas verificar se não há erros na execução.

def test_plot_pl_with_single_and_multiple_params():
    # Testando plotagem com um único conjunto de parâmetros
    plotter = Plot()
    params_single = [{'dType': 'C', 'price': 1, 'quant': 1, 'strike': 105, 'vola': 0.2, 'exp': 1/365}]
    try:
        plotter.plotPL(bePriceS=90, bePriceF=110, params=params_single, exp=1/365, step=5)
        plt.close() # Fechando a figura para o próximo teste
        assert True # Se chegou aqui sem erro, consideramos um sucesso básico
    except Exception as e:
        assert False, f"Erro ao plotar com um único parâmetro: {e}"

    # Testando plotagem com múltiplos conjuntos de parâmetros
    params_multiple = [
        {'dType': 'C', 'price': 1, 'quant': 1, 'strike': 105, 'vola': 0.2, 'exp': 1/365},
        {'dType': 'P', 'price': 1, 'quant': 1, 'strike': 95, 'vola': 0.25, 'exp': 30/365}
    ]
    try:
        plotter.plotPL(bePriceS=80, bePriceF=120, params=params_multiple, exp=30/365, step=10)
        plt.close()
        assert True # Se chegou aqui sem erro, consideramos um sucesso básico
    except Exception as e:
        assert False, f"Erro ao plotar com múltiplos parâmetros: {e}"

    # Testando plotagem passando um único elemento da lista params (indexado)
    try:
        plotter.plotPL(bePriceS=80, bePriceF=120, params=[params_multiple[0]], exp=1/365, step=5)
        plt.close()
        assert True # Se chegou aqui sem erro, consideramos um sucesso básico
    except Exception as e:
        assert False, f"Erro ao plotar o primeiro parâmetro individualmente: {e}"

    try:
        plotter.plotPL(bePriceS=80, bePriceF=120, params=[params_multiple[1]], exp=30/365, step=10)
        plt.close()
        assert True # Se chegou aqui sem erro, consideramos um sucesso básico
    except Exception as e:
        assert False, f"Erro ao plotar o segundo parâmetro individualmente: {e}"

# Podemos criar testes similares para plotDelta, plotTheta, plotVega e plotGamma
# adaptando os parâmetros conforme necessário.

def test_plot_delta_with_single_param_indexed():
    plotter = Plot()
    params = [{'dType': 'C', 'price': 1, 'quant': 1, 'strike': 105, 'vola': 0.2, 'exp': 1/365}]
    try:
        plotter.plotDelta(bePriceS=90, bePriceF=110, params=[params[0]], exp=1/365, step=5)
        plt.close()
        assert True
    except Exception as e:
        assert False, f"Erro ao plotar Delta com parâmetro indexado: {e}"