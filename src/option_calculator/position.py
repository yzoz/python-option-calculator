"""Portfolio position model for the option calculator.

A position is described by an :class:`OptionPosition`. For backward
compatibility the pricing aggregators also accept plain dictionaries with the
same fields.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

OptionType = Literal["C", "P", "F"]

_VALID_TYPES: tuple[str, ...] = ("C", "P", "F")


@dataclass
class OptionPosition:
    """A single position in a portfolio.

    Attributes:
    ----------
    dType:
        ``'C'`` call, ``'P'`` put or ``'F'`` linear future.
    strike:
        Strike price (must be ``> 0`` for options; use ``0`` for futures).
    vola:
        Implied volatility as a fraction (e.g. ``0.45``).
    exp:
        Time to expiry in years.
    quant:
        Signed quantity (positive = long, negative = short).
    price:
        Entry premium / price used for P&L calculations.
    """

    dType: OptionType
    strike: float
    vola: float
    exp: float
    quant: float
    price: float = 0.0

    def __post_init__(self) -> None:
        """Validate the position fields after construction."""
        if self.dType not in _VALID_TYPES:
            raise ValueError(f"dType must be one of {_VALID_TYPES}, got {self.dType!r}")
        if self.exp < 0:
            raise ValueError(f"exp must be >= 0, got {self.exp!r}")
        if self.dType != "F":
            if self.strike <= 0:
                raise ValueError(
                    f"strike must be > 0 for dType={self.dType!r}, got {self.strike!r}"
                )
            if self.vola < 0:
                raise ValueError(f"vola must be >= 0, got {self.vola!r}")
