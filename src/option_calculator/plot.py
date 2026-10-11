"""Visualisation layer for option portfolios.

This module is a thin presentation wrapper: it owns a
:class:`~option_calculator.pricing.Pricing` instance (composition) and delegates
all calculations to it. ``matplotlib`` is imported only here, so the pricing
core can be used without a plotting dependency.

Usage::

    from option_calculator import Plot

    plot = Plot()
    plot.plotPL(price_min, price_max, params, exp, step)
"""

from __future__ import annotations

import matplotlib.pyplot as plt

from .bsm import DAYS_PER_YEAR
from .pricing import Pricing


class Plot:
    """Build P&L and greek curves and hand them to matplotlib."""

    def __init__(self, pricing: Pricing | None = None) -> None:
        """Store the pricing engine whose results are plotted."""
        self.pricing = pricing if pricing is not None else Pricing()

    def __getattr__(self, name: str):
        """Delegate pricing/aggregation calls to the owned :class:`Pricing`."""
        return getattr(self.pricing, name)

    # ------------------------------------------------------------------ #
    # Curve builders
    # ------------------------------------------------------------------ #
    def _curve(self, price_min, price_max, step, evaluate):
        """Return ``(prices, values)`` sampled over ``[price_min, price_max]``."""
        prices = Pricing.price_range(price_min, price_max, step)
        return prices, [evaluate(price) for price in prices]

    def _plot(self, price_min, price_max, params, exp, step, evaluate):
        prices, values = self._curve(price_min, price_max, step, evaluate)
        plt.plot(prices, values, label=int(exp * DAYS_PER_YEAR))

    def plotPL(self, price_min, price_max, params, exp, step):
        """Plot the portfolio P&L curve."""
        self._plot(
            price_min,
            price_max,
            params,
            exp,
            step,
            lambda price: self.pricing.p_l(price, params, exp),
        )

    def plotDelta(self, price_min, price_max, params, exp, step):
        """Plot the portfolio delta curve."""
        self._plot(
            price_min,
            price_max,
            params,
            exp,
            step,
            lambda price: self.pricing.deltaFull(price, params, exp),
        )

    def plotTheta(self, price_min, price_max, params, exp, step):
        """Plot the portfolio theta curve."""
        self._plot(
            price_min,
            price_max,
            params,
            exp,
            step,
            lambda price: self.pricing.thetaFull(price, params, exp),
        )

    def plotVega(self, price_min, price_max, params, exp, step):
        """Plot the portfolio vega curve."""
        self._plot(
            price_min,
            price_max,
            params,
            exp,
            step,
            lambda price: self.pricing.vegaFull(price, params, exp),
        )

    def plotGamma(self, price_min, price_max, params, exp, step):
        """Plot the portfolio gamma curve."""
        self._plot(
            price_min,
            price_max,
            params,
            exp,
            step,
            lambda price: self.pricing.gammaFull(price, params, exp),
        )
