"""Tests for the delta-neutral price search (``option_calculator.searching``)."""

import pytest

from option_calculator import Search


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


def test_search_returns_rows(portfolio, exp):
    search = Search()
    target = {"dType": "F", "price": 0, "quant": -1, "strike": 0, "vola": 0, "exp": exp}
    rows = search.searchDelta(21000, target, portfolio, price_range=7500, step=0.1)
    assert isinstance(rows, list)
    assert rows, "expected at least one delta-neutral level"
    row = rows[0]
    assert set(row) == {"price", "dType", "strike", "quant", "delta", "delta_portfolio", "theo"}
    # The combined delta is ~0 at the found level.
    assert abs(row["delta"] + row["delta_portfolio"]) <= 1e-3


def test_search_no_match_returns_empty(portfolio, exp):
    search = Search()
    # A target with a huge quantity can never be offset by the portfolio.
    target = {"dType": "F", "price": 0, "quant": -1000, "strike": 0, "vola": 0, "exp": exp}
    rows = search.searchDelta(21000, target, portfolio, price_range=100, step=10)
    assert rows == []
