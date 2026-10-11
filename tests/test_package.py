"""Smoke tests for the public package API."""

import option_calculator


def test_public_api():
    assert option_calculator.__version__
    for name in ("BSM", "Pricing", "OptionPosition", "Search"):
        assert hasattr(option_calculator, name)


def test_canonical_imports():
    from option_calculator import BSM, OptionPosition, Pricing, Search

    assert BSM is option_calculator.BSM
    assert Pricing is option_calculator.Pricing
    assert OptionPosition is option_calculator.OptionPosition
    assert Search is option_calculator.Search
