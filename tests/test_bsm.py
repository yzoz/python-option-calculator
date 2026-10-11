"""Tests for the Black-Scholes-Merton core (``option_calculator.bsm``)."""

import math

import pytest

from option_calculator import BSM, DAYS_PER_YEAR, VEGA_SCALE


@pytest.fixture
def bsm():
    return BSM()


# --------------------------------------------------------------------------- #
# Reference values (textbook case: S=K=100, V=0.2, T=1, r=0.05)
# --------------------------------------------------------------------------- #
def test_reference_call_and_put(bsm):
    call = bsm.theo(100, 100, 0.2, 1.0, "C", r=0.05)
    put = bsm.theo(100, 100, 0.2, 1.0, "P", r=0.05)
    assert call == pytest.approx(10.4506, abs=1e-4)
    assert put == pytest.approx(5.5735, abs=1e-4)


def test_reference_greeks(bsm):
    assert bsm.delta(100, 100, 0.2, 1.0, "C", r=0.05) == pytest.approx(0.6368, abs=1e-4)
    assert bsm.delta(100, 100, 0.2, 1.0, "P", r=0.05) == pytest.approx(-0.3632, abs=1e-4)
    assert bsm.gamma(100, 100, 0.2, 1.0, r=0.05) == pytest.approx(0.018762, abs=1e-6)
    assert bsm.vega(100, 100, 0.2, 1.0, r=0.05) == pytest.approx(0.37524, abs=1e-5)


def test_put_call_parity_zero_rate(bsm):
    S, K, V, T = 19500, 19000, 0.45, 30 / 365
    call = bsm.theo(S, K, V, T, "C")
    put = bsm.theo(S, K, V, T, "P")
    assert call - put == pytest.approx(S - K, abs=1e-9)


def test_put_call_parity_with_rate(bsm):
    S, K, V, T, r = 100, 105, 0.3, 2.0, 0.04
    call = bsm.theo(S, K, V, T, "C", r=r)
    put = bsm.theo(S, K, V, T, "P", r=r)
    assert call - put == pytest.approx(S - K * math.exp(-r * T), abs=1e-9)


# --------------------------------------------------------------------------- #
# Analytic properties
# --------------------------------------------------------------------------- #
def test_delta_bounds(bsm):
    for dType in ("C", "P"):
        for S in (50, 100, 150):
            d = bsm.delta(S, 100, 0.3, 1.0, dType)
            assert (-1.0 - 1e-12) <= d <= (1.0 + 1e-12)
    assert bsm.delta(100, 100, 0.3, 1.0, "C") >= 0
    assert bsm.delta(100, 100, 0.3, 1.0, "P") <= 0


def test_vega_and_gamma_positive(bsm):
    assert bsm.vega(100, 100, 0.3, 1.0) > 0
    assert bsm.gamma(100, 100, 0.3, 1.0) > 0


def test_future_delta_is_one(bsm):
    assert bsm.delta(21000, 0, 0, 1.0, "F") == 1.0


# --------------------------------------------------------------------------- #
# Degenerate inputs
# --------------------------------------------------------------------------- #
def test_expired_option_is_intrinsic(bsm):
    assert bsm.theo(100, 90, 0.2, 0.0, "C") == pytest.approx(10.0)
    assert bsm.theo(100, 90, 0.2, 0.0, "P") == pytest.approx(0.0)
    assert bsm.theo(80, 90, 0.2, 0.0, "C") == pytest.approx(0.0)
    assert bsm.theo(80, 90, 0.2, 0.0, "P") == pytest.approx(10.0)


def test_zero_vol_is_deterministic(bsm):
    assert bsm.theo(100, 90, 0.0, 1.0, "C") == pytest.approx(10.0)
    assert bsm.delta(100, 90, 0.0, 1.0, "C") == 1.0
    assert bsm.delta(80, 90, 0.0, 1.0, "C") == 0.0
    assert bsm.vega(100, 90, 0.0, 1.0) == 0.0
    assert bsm.theta(100, 90, 0.0, 1.0) == 0.0
    assert bsm.gamma(100, 90, 0.0, 1.0) == 0.0


def test_expired_discounted_intrinsic(bsm):
    # With r > 0, T == 0 still discounts the strike consistently.
    assert bsm.theo(100, 90, 0.2, 0.0, "C", r=0.05) == pytest.approx(10.0)


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "S,K,V,T", [(-1, 100, 0.2, 1), (100, 0, 0.2, 1), (100, 100, -0.1, 1), (100, 100, 0.2, -1)]
)
def test_invalid_numbers_raise(bsm, S, K, V, T):
    with pytest.raises(ValueError):
        bsm.theo(S, K, V, T, "C")


@pytest.mark.parametrize("dType", ["X", "c", "", None])
def test_invalid_type_raises(bsm, dType):
    with pytest.raises(ValueError):
        bsm.delta(100, 100, 0.2, 1.0, dType)


def test_theo_rejects_future(bsm):
    with pytest.raises(ValueError):
        bsm.theo(100, 100, 0.2, 1.0, "F")


def test_d1_d2_defined_only_with_vol_and_time(bsm):
    with pytest.raises(ValueError):
        bsm.d1(100, 100, 0.2, 0.0)
    with pytest.raises(ValueError):
        bsm.d2(100, 100, 0.0, 1.0)


def test_constants():
    assert DAYS_PER_YEAR == 365
    assert VEGA_SCALE == 100.0
