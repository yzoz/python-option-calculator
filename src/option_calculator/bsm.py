"""Black-Scholes-Merton pricing for vanilla options using only the standard library.

Conventions
-----------
* ``S``  underlying / forward price; ``K`` strike; ``V`` implied volatility as a
  fraction (e.g. ``0.45`` for 45%); ``T`` time to expiry in years; ``r``
  continuously compounded risk-free rate (default ``0.0``).
* ``dType`` is one of ``'C'`` (call), ``'P'`` (put) or ``'F'`` (linear future).
* Vega is scaled by ``VEGA_SCALE`` (per 1 percentage point of volatility) and
  Theta is expressed per calendar day (``DAYS_PER_YEAR``).
* All formulas use continuous discounting at ``r``. With the default ``r = 0.0``
  they reduce to the classic zero-rate Black-Scholes formulas, which is the
  convention appropriate for coin-margined / futures-style crypto options.

Degenerate inputs
-----------------
* ``T == 0`` (expired) and ``V == 0`` (deterministic forward) are valid and
  yield the discounted intrinsic value; the corresponding greeks are
  deterministic (Delta = 0 / 1 / -1, Vega/Theta/Gamma = 0).
"""

from __future__ import annotations

import math
from typing import Literal

DAYS_PER_YEAR = 365
VEGA_SCALE = 100.0

OptionType = Literal["C", "P", "F"]
_VANILLA_TYPES: tuple[str, ...] = ("C", "P", "F")


class BSM:
    """Stateless Black-Scholes-Merton calculator for a single vanilla option."""

    # ------------------------------------------------------------------ #
    # Distribution helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def pdf(x: float) -> float:
        """Return the standard normal probability density at ``x``."""
        return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)

    @staticmethod
    def cdf(x: float) -> float:
        """Return the standard normal cumulative distribution at ``x``."""
        return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

    # ------------------------------------------------------------------ #
    # Validation
    # ------------------------------------------------------------------ #
    @staticmethod
    def _check_numbers(S: float, K: float, V: float, T: float) -> None:
        """Validate the numeric inputs shared by every pricing method."""
        if S <= 0:
            raise ValueError(f"S (underlying price) must be > 0, got {S!r}")
        if K <= 0:
            raise ValueError(f"K (strike) must be > 0, got {K!r}")
        if V < 0:
            raise ValueError(f"V (volatility) must be >= 0, got {V!r}")
        if T < 0:
            raise ValueError(f"T (time to expiry) must be >= 0, got {T!r}")

    @staticmethod
    def _check_type(dType: str) -> None:
        """Validate the option type flag."""
        if dType not in _VANILLA_TYPES:
            raise ValueError(f"dType must be one of {_VANILLA_TYPES}, got {dType!r}")

    # ------------------------------------------------------------------ #
    # Core building blocks
    # ------------------------------------------------------------------ #
    def _d1_d2(self, S: float, K: float, V: float, T: float, r: float = 0.0) -> tuple[float, float]:
        """Return ``(d1, d2)`` computed once for the given inputs."""
        variance_term = V * math.sqrt(T)
        d1 = (math.log(S / K) + (r + V * V / 2.0) * T) / variance_term
        return d1, d1 - variance_term

    def d1(self, S: float, K: float, V: float, T: float, r: float = 0.0) -> float:
        """Return the ``d1`` term of the Black-Scholes formula."""
        self._check_numbers(S, K, V, T)
        if T == 0 or V == 0:
            raise ValueError("d1 is undefined when T == 0 or V == 0")
        return self._d1_d2(S, K, V, T, r)[0]

    def d2(self, S: float, K: float, V: float, T: float, r: float = 0.0) -> float:
        """Return the ``d2`` term of the Black-Scholes formula."""
        self._check_numbers(S, K, V, T)
        if T == 0 or V == 0:
            raise ValueError("d2 is undefined when T == 0 or V == 0")
        return self._d1_d2(S, K, V, T, r)[1]

    # ------------------------------------------------------------------ #
    # Theoretical price
    # ------------------------------------------------------------------ #
    def theo(self, S: float, K: float, V: float, T: float, dT: str, r: float = 0.0) -> float:
        """Theoretical (fair) value of a call (``'C'``) or put (``'P'``)."""
        self._check_type(dT)
        if dT == "F":
            raise ValueError("theo() is not defined for futures (dType='F')")
        self._check_numbers(S, K, V, T)

        discounted_strike = K * math.exp(-r * T)
        if T == 0 or V == 0:
            # Deterministic forward value / discounted intrinsic.
            if dT == "C":
                return max(S - discounted_strike, 0.0)
            return max(discounted_strike - S, 0.0)

        d1, d2 = self._d1_d2(S, K, V, T, r)
        if dT == "C":
            return S * self.cdf(d1) - discounted_strike * self.cdf(d2)
        return discounted_strike * self.cdf(-d2) - S * self.cdf(-d1)

    # ------------------------------------------------------------------ #
    # Greeks
    # ------------------------------------------------------------------ #
    def delta(self, S: float, K: float, V: float, T: float, dT: str, r: float = 0.0) -> float:
        """Delta of a call/put, or ``1.0`` per unit for a linear future (``'F'``)."""
        self._check_type(dT)
        if dT == "F":
            return 1.0
        self._check_numbers(S, K, V, T)

        discounted_strike = K * math.exp(-r * T)
        if T == 0 or V == 0:
            if dT == "C":
                return 1.0 if S > discounted_strike else 0.0
            return -1.0 if S < discounted_strike else 0.0

        d1 = self._d1_d2(S, K, V, T, r)[0]
        if dT == "C":
            return self.cdf(d1)
        return self.cdf(d1) - 1.0

    def vega(self, S: float, K: float, V: float, T: float, r: float = 0.0) -> float:
        """Vega per 1 percentage point of implied volatility."""
        self._check_numbers(S, K, V, T)
        if T == 0 or V == 0:
            return 0.0
        d1 = self._d1_d2(S, K, V, T, r)[0]
        return S * math.sqrt(T) * self.pdf(d1) / VEGA_SCALE

    def theta(
        self,
        S: float,
        K: float,
        V: float,
        T: float,
        dType: str = "C",
        r: float = 0.0,
    ) -> float:
        """Theta per calendar day (``DAYS_PER_YEAR``) for a call or put."""
        self._check_type(dType)
        if dType == "F":
            return 0.0
        self._check_numbers(S, K, V, T)
        if T == 0 or V == 0:
            return 0.0

        d1, d2 = self._d1_d2(S, K, V, T, r)
        base = -(S * V * self.pdf(d1)) / (2.0 * math.sqrt(T))
        discounted_strike = K * math.exp(-r * T)
        if dType == "C":
            annual = base - r * discounted_strike * self.cdf(d2)
        else:
            annual = base + r * discounted_strike * self.cdf(-d2)
        return annual / DAYS_PER_YEAR

    def gamma(self, S: float, K: float, V: float, T: float, r: float = 0.0) -> float:
        """Gamma of a vanilla option."""
        self._check_numbers(S, K, V, T)
        if T == 0 or V == 0:
            return 0.0
        d1 = self._d1_d2(S, K, V, T, r)[0]
        return self.pdf(d1) / (S * V * math.sqrt(T))
