"""Tests for portfolio aggregation (``option_calculator.pricing``)."""

import copy

import pytest

from option_calculator import OptionPosition, Pricing


@pytest.fixture
def pricing():
    return Pricing()


@pytest.fixture
def exp():
    return 30 / 365


@pytest.fixture
def portfolio(exp):
    return [
        {"dType": "F", "price": 20000, "quant": 1, "strike": 0, "vola": 0, "exp": exp},
        {"dType": "C", "price": 500, "quant": 1, "strike": 25000, "vola": 0.75, "exp": exp},
        {"dType": "P", "price": 100, "quant": 1, "strike": 15000, "vola": 0.75, "exp": exp},
        {"dType": "P", "price": 25, "quant": -1, "strike": 10000, "vola": 1.5, "exp": exp},
    ]


def test_aggregate_smoke(pricing, portfolio, exp):
    f = 21000
    assert pricing.deltaFull(f, portfolio, exp) == pytest.approx(1.2199, abs=1e-3)
    assert pricing.vegaFull(f, portfolio, exp) == pytest.approx(21.031, abs=1e-2)
    assert pricing.thetaFull(f, portfolio, exp) == pytest.approx(-21.719, abs=1e-2)
    assert pricing.gammaFull(f, portfolio, exp) == pytest.approx(8.41e-05, abs=1e-6)
    assert pricing.p_l(f, portfolio, exp) == pytest.approx(994.598, abs=1e-2)


def test_inputs_are_not_mutated(pricing, portfolio, exp):
    snapshot = copy.deepcopy(portfolio)
    pricing.deltaFull(21000, portfolio, exp)
    pricing.vegaFull(21000, portfolio, exp)
    pricing.thetaFull(21000, portfolio, exp)
    pricing.gammaFull(21000, portfolio, exp)
    pricing.p_l(21000, portfolio, exp)
    assert portfolio == snapshot


def test_exp_zero_is_honoured(pricing, portfolio):
    # exp=0 must not be silently ignored (old `if exp:` bug).
    with_zero = pricing.deltaFull(21000, portfolio, 0)
    assert with_zero == pytest.approx(1.0)  # only the future contributes


def test_accepts_option_position_objects(pricing, exp):
    positions = [
        OptionPosition("F", 0, 0, exp, 1, 20000),
        OptionPosition("C", 25000, 0.75, exp, 1, 500),
        OptionPosition("P", 15000, 0.75, exp, 1, 100),
        OptionPosition("P", 10000, 1.5, exp, -1, 25),
    ]
    assert pricing.deltaFull(21000, positions, exp) == pytest.approx(1.2199, abs=1e-3)
    assert pricing.p_l(21000, positions, exp) == pytest.approx(994.598, abs=1e-2)


def test_uses_position_exp_when_not_overridden(pricing, exp):
    positions = [OptionPosition("C", 100, 0.2, exp, 1, 0)]
    assert pricing.deltaFull(100, positions) == pytest.approx(
        pricing.bsm.delta(100, 100, 0.2, exp, "C")
    )


def test_r_is_threaded_through(pricing, portfolio, exp):
    zero = pricing.deltaFull(21000, portfolio, exp, r=0.0)
    nonzero = pricing.deltaFull(21000, portfolio, exp, r=0.05)
    assert zero != nonzero


def test_missing_field_reports_position_and_name(pricing):
    with pytest.raises(KeyError) as excinfo:
        pricing.deltaFull(100, [{"dType": "C", "strike": 100}])
    assert "params[0]" in str(excinfo.value)
    assert "vola" in str(excinfo.value)


def test_bad_params_type(pricing):
    with pytest.raises(TypeError):
        pricing.deltaFull(100, "not-a-list")
    with pytest.raises(TypeError):
        pricing.deltaFull(100, [123])


def test_price_range(pricing):
    assert Pricing.price_range(0, 3, 1) == [0, 1, 2, 3]
    with pytest.raises(ValueError):
        Pricing.price_range(0, 3, 0)
