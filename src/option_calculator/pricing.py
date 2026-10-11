"""Portfolio-level aggregation of Black-Scholes-Merton greeks and P&L.

Design notes
------------
* The class owns a :class:`~option_calculator.bsm.BSM` instance (composition)
  rather than inheriting from it. This keeps the pricing logic reusable and
  testable and avoids a deep inheritance chain.
* Positions may be :class:`~option_calculator.position.OptionPosition` instances
  or plain mappings with the same fields (backward compatibility).
* Inputs are never mutated: the effective expiry is a local value, not written
  back into the position. An explicit ``exp`` argument overrides the position's
  own ``exp``; ``exp = 0`` is honoured (checked with ``is not None``).
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Any, Callable, Union

from .bsm import BSM
from .position import OptionPosition

PositionLike = Union[OptionPosition, Mapping[str, Any]]

_REQUIRED_FIELDS = ("dType", "strike", "vola", "quant")


class Pricing:
    """Aggregate greeks and P&L across a portfolio of positions."""

    def __init__(self, bsm: BSM | None = None) -> None:
        """Store the calculator used for per-option pricing."""
        self.bsm = bsm if bsm is not None else BSM()

    # ------------------------------------------------------------------ #
    # Price grid helper
    # ------------------------------------------------------------------ #
    @staticmethod
    def price_range(price_min: float, price_max: float, step: float) -> list[float]:
        """Return the inclusive price grid from ``price_min`` to ``price_max``."""
        if step <= 0:
            raise ValueError(f"step must be > 0, got {step!r}")
        prices = []
        price = price_min
        while price <= price_max:
            prices.append(price)
            price += step
        return prices

    # ------------------------------------------------------------------ #
    # Position access helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _field(position: PositionLike, name: str) -> Any:
        """Read a field from an :class:`OptionPosition` or a mapping."""
        if isinstance(position, OptionPosition):
            return getattr(position, name)
        if isinstance(position, Mapping):
            return position[name]
        raise TypeError(
            f"position must be an OptionPosition or mapping, got {type(position).__name__}"
        )

    @classmethod
    def _validate_params(cls, params: Iterable[PositionLike]) -> None:
        """Ensure every position has the required fields, with context in errors."""
        if isinstance(params, (str, bytes)) or not isinstance(params, Iterable):
            raise TypeError(f"params must be an iterable of positions, got {type(params).__name__}")
        for index, position in enumerate(params):
            if not isinstance(position, (OptionPosition, Mapping)):
                raise TypeError(
                    f"params[{index}] must be an OptionPosition or mapping, "
                    f"got {type(position).__name__}"
                )
            if isinstance(position, Mapping):
                for field in _REQUIRED_FIELDS:
                    if field not in position:
                        raise KeyError(f"params[{index}] is missing required field {field!r}")

    @classmethod
    def _resolve_exp(cls, position: PositionLike, exp: float | None) -> float:
        """Return the effective expiry without mutating the position."""
        if exp is not None:
            return exp
        if isinstance(position, OptionPosition):
            return position.exp
        if "exp" in position:
            return position["exp"]
        raise KeyError("position is missing required field 'exp'")

    # ------------------------------------------------------------------ #
    # Aggregation
    # ------------------------------------------------------------------ #
    def _aggregate(
        self,
        fPrice: float,
        params: Iterable[PositionLike],
        exp: float | None,
        greek_fn: Callable[[float, PositionLike, float, float], float],
        r: float = 0.0,
    ) -> float:
        """Sum ``quant * greek_fn(fPrice, position, exp, r)`` over ``params``.

        ``greek_fn`` is responsible for returning ``0.0`` for positions it does
        not apply to (e.g. futures for the option-only greeks).
        """
        self._validate_params(params)
        total = 0.0
        for position in params:
            effective_exp = self._resolve_exp(position, exp)
            total += self._field(position, "quant") * greek_fn(fPrice, position, effective_exp, r)
        return total

    def _option_greek(
        self,
        method: Callable[..., float],
        fPrice: float,
        position: PositionLike,
        effective_exp: float,
        r: float,
    ) -> float:
        """Apply an option-only greek, returning 0 for futures (``'F'``)."""
        if self._field(position, "dType") == "F":
            return 0.0
        return method(
            fPrice,
            self._field(position, "strike"),
            self._field(position, "vola"),
            effective_exp,
            r=r,
        )

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def deltaFull(
        self,
        fPrice: float,
        params: Sequence[PositionLike],
        exp: float | None = None,
        r: float = 0.0,
    ) -> float:
        """Net delta of the portfolio (futures contribute their quantity)."""

        def greek(fPrice, position, effective_exp, r):
            return self.bsm.delta(
                fPrice,
                self._field(position, "strike"),
                self._field(position, "vola"),
                effective_exp,
                self._field(position, "dType"),
                r,
            )

        return self._aggregate(fPrice, params, exp, greek, r)

    def vegaFull(
        self,
        fPrice: float,
        params: Sequence[PositionLike],
        exp: float | None = None,
        r: float = 0.0,
    ) -> float:
        """Net vega of the portfolio (futures have no vega)."""
        return self._aggregate(
            fPrice,
            params,
            exp,
            lambda f, p, e, rr: self._option_greek(self.bsm.vega, f, p, e, rr),
            r,
        )

    def thetaFull(
        self,
        fPrice: float,
        params: Sequence[PositionLike],
        exp: float | None = None,
        r: float = 0.0,
    ) -> float:
        """Net theta of the portfolio (futures have no theta)."""

        def greek(f, p, e, rr):
            if self._field(p, "dType") == "F":
                return 0.0
            return self.bsm.theta(
                f,
                self._field(p, "strike"),
                self._field(p, "vola"),
                e,
                self._field(p, "dType"),
                rr,
            )

        return self._aggregate(fPrice, params, exp, greek, r)

    def gammaFull(
        self,
        fPrice: float,
        params: Sequence[PositionLike],
        exp: float | None = None,
        r: float = 0.0,
    ) -> float:
        """Net gamma of the portfolio (futures have no gamma)."""
        return self._aggregate(
            fPrice,
            params,
            exp,
            lambda f, p, e, rr: self._option_greek(self.bsm.gamma, f, p, e, rr),
            r,
        )

    def p_l(
        self,
        fPrice: float,
        params: Sequence[PositionLike],
        exp: float | None = None,
        r: float = 0.0,
    ) -> float:
        """Mark-to-market P&L of the portfolio for a given underlying price."""

        def per_position(fPrice, position, effective_exp, rr):
            if self._field(position, "dType") == "F":
                return fPrice - self._field(position, "price")
            theo = round(
                self.bsm.theo(
                    fPrice,
                    self._field(position, "strike"),
                    self._field(position, "vola"),
                    effective_exp,
                    self._field(position, "dType"),
                    rr,
                ),
                3,
            )
            return theo - self._field(position, "price")

        return self._aggregate(fPrice, params, exp, per_position, r)
