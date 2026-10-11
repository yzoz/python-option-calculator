"""Delta-neutral price search over a range of underlying prices.

Given a target position ``paramD`` and a portfolio ``params``, :class:`Search`
finds the underlying prices at which the target's delta offsets the portfolio
delta (i.e. the combined delta is ~0). All calculations are delegated to a
:class:`~option_calculator.pricing.Pricing` instance.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Union

from .position import OptionPosition
from .pricing import Pricing

PositionLike = Union[OptionPosition, Mapping[str, Any]]


class Search:
    """Search for delta-neutral underlying price levels."""

    def __init__(self, pricing: Pricing | None = None) -> None:
        """Store the pricing engine used for all calculations."""
        self.pricing = pricing if pricing is not None else Pricing()

    def searchDelta(
        self,
        fPrice: float,
        paramD: PositionLike,
        params: Sequence[PositionLike],
        price_range: float = 7500,
        step: float = 0.1,
        eps: float = 1e-4,
        exp: float | None = None,
        r: float = 0.0,
    ) -> list[dict[str, float]]:
        """Return price levels where the target and portfolio deltas cancel out.

        Parameters
        ----------
        fPrice:
            Current underlying price; the search spans ``fPrice ± price_range``.
        paramD:
            The target position whose delta is being offset.
        params:
            The rest of the portfolio.
        price_range:
            Half-width of the scanned price interval.
        step:
            Price increment between samples.
        eps:
            Tolerance used when comparing the two deltas (floats).
        exp:
            Optional expiry override applied to every position; ``None`` means
            each position keeps its own expiry.
        r:
            Risk-free rate passed through to the pricing engine.

        Returns:
        -------
        list[dict]
            One row per distinct matching level, with keys ``price``,
            ``dType``, ``strike``, ``quant``, ``delta``, ``delta_portfolio``,
            ``theo``.
        """
        read = self.pricing._field  # local alias for readability
        d_type = read(paramD, "dType")
        strike = read(paramD, "strike")
        vola = read(paramD, "vola")
        quant = read(paramD, "quant")
        effective_exp = exp if exp is not None else read(paramD, "exp")

        rows: list[dict[str, float]] = []
        for price in Pricing.price_range(fPrice - price_range, fPrice + price_range, step):
            target_delta = (
                self.pricing.bsm.delta(price, strike, vola, effective_exp, d_type, r) * quant
            )
            portfolio_delta = self.pricing.deltaFull(price, params, exp, r)
            if abs(target_delta + portfolio_delta) <= eps:
                if d_type == "F":
                    theo = 0.0
                else:
                    theo = round(
                        self.pricing.bsm.theo(price, strike, vola, effective_exp, d_type, r),
                        3,
                    )
                rows.append(
                    {
                        "price": round(price, 2),
                        "dType": d_type,
                        "strike": strike,
                        "quant": quant,
                        "delta": round(target_delta, 4),
                        "delta_portfolio": round(portfolio_delta, 3),
                        "theo": theo,
                    }
                )

        # Keep only the first level of each run of equal target deltas.
        unique: list[dict[str, float]] = []
        for row in rows:
            if not unique or unique[-1]["delta"] != row["delta"]:
                unique.append(row)
        return unique


if __name__ == "__main__":
    from pprint import pprint

    days = 365
    fPrice = 21000
    exp = 30 / days

    params = [
        {"dType": "F", "price": 20000, "quant": 1, "strike": 0, "vola": 0, "exp": exp},
        {"dType": "C", "price": 500, "quant": 1, "strike": 25000, "vola": 0.75, "exp": exp},
        {"dType": "P", "price": 100, "quant": 1, "strike": 15000, "vola": 0.75, "exp": exp},
        {"dType": "P", "price": 25, "quant": -1, "strike": 10000, "vola": 1.5, "exp": exp},
    ]

    target = {"dType": "F", "price": 0, "quant": -1, "strike": 0, "vola": 0, "exp": exp}
    pprint(Search().searchDelta(fPrice, target, params, price_range=7500, step=0.1))
