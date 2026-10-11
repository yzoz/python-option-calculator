"""Tests for the plotting layer (headless via the Agg backend)."""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import pytest  # noqa: E402

from option_calculator import Plot  # noqa: E402


@pytest.fixture(autouse=True)
def _clean_figure():
    yield
    plt.close("all")


@pytest.fixture
def params():
    exp = 30 / 365
    return [{"dType": "C", "price": 500, "quant": 1, "strike": 25000, "vola": 0.75, "exp": exp}]


@pytest.mark.parametrize(
    "method",
    ["plotPL", "plotDelta", "plotTheta", "plotVega", "plotGamma"],
)
def test_plot_methods_run(method, params):
    exp = 30 / 365
    plot = Plot()
    getattr(plot, method)(20000, 22000, params, exp, 1000)
    assert plt.gca().get_lines()


def test_delegates_pricing_calls(params):
    exp = 30 / 365
    plot = Plot()
    assert plot.p_l(21000, params, exp) == pytest.approx(plot.pricing.p_l(21000, params, exp))
    assert plot.deltaFull(21000, params, exp) == pytest.approx(
        plot.pricing.deltaFull(21000, params, exp)
    )
