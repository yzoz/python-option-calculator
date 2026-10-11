"""Vanilla option calculator: Black-Scholes-Merton pricing in pure Python.

The core (``BSM``, ``Pricing``, ``OptionPosition``, ``Search``) depends only on
the standard library. The optional plotting layer (``Plot``) requires
``matplotlib`` and is imported lazily, so ``import option_calculator`` works
without it.

Example:
-------
>>> from option_calculator import BSM
>>> BSM().theo(100, 100, 0.2, 1.0, "C", r=0.0)  # doctest: +SKIP
"""

from __future__ import annotations

from .bsm import BSM, DAYS_PER_YEAR, VEGA_SCALE, OptionType
from .position import OptionPosition
from .pricing import Pricing
from .searching import Search

__all__ = [
    "BSM",
    "Pricing",
    "OptionPosition",
    "Search",
    "Plot",
    "OptionType",
    "DAYS_PER_YEAR",
    "VEGA_SCALE",
]

__version__ = "0.1.0"

_PLOT_ATTRS = {"Plot"}


def __getattr__(name: str):
    """Lazily expose the plotting layer without a hard matplotlib dependency."""
    if name in _PLOT_ATTRS:
        from .plot import Plot

        return Plot
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
