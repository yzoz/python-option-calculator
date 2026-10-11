<img align="right" src="https://img.shields.io/badge/python-3.9%2B-blue" alt="Python 3.9+">

# Vanilla Option Calculator

[![PyPI](https://img.shields.io/pypi/v/option-calculator.svg)](https://pypi.org/project/option-calculator/)
[![PyPI - Python versions](https://img.shields.io/pypi/pyversions/option-calculator.svg)](https://pypi.org/project/option-calculator/)
[![CI](https://github.com/yzoz/python-option-calculator/actions/workflows/ci.yml/badge.svg)](https://github.com/yzoz/python-option-calculator/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/yzoz/python-option-calculator/blob/master/LICENSE)

**Black-Scholes-Merton** pricing and greeks for vanilla options, written in **pure
Python** — no NumPy, no SciPy, no other numerical dependencies. The only external
dependency is `matplotlib`, and only for the optional plotting layer.

Available on **PyPI**: [`option-calculator`](https://pypi.org/project/option-calculator/).

- Theoretical price and greeks: **Theo, Delta, Theta, Vega, Gamma**
- Portfolio aggregation and mark-to-market **P&L** across many positions
- Price-grid **visualisation** (P&L / Delta / Theta / Vega / Gamma)
- Delta-neutral price **search**
- Optional risk-free rate `r` (defaults to `0`, the rates-free crypto convention)

## Installation

From **PyPI**:

```bash
pip install option-calculator            # core only (standard library)
pip install "option-calculator[plot]"    # + matplotlib for the plotting layer
```

From source:

```bash
pip install .            # core only (standard library)
pip install ".[plot]"    # + matplotlib for the plotting layer
pip install ".[dev]"     # + pytest and ruff for development
```

Or, for development, install in editable mode:

```bash
pip install -e ".[plot,dev]"
```

## Quick start

### Price and greeks of a single option

```python
from option_calculator import BSM

calc = BSM()

S = 19500          # underlying price
K = 19000          # strike
V = 0.45           # implied volatility as a fraction (45%)
T = 30 / 365       # time to expiry in years
dType = "P"        # 'C' call, 'P' put, 'F' future

print("Theo: ", round(calc.theo(S, K, V, T, dType), 2))
print("Delta:", round(calc.delta(S, K, V, T, dType), 2))
print("Theta:", round(calc.theta(S, K, V, T, dType), 2))
print("Vega: ", round(calc.vega(S, K, V, T), 2))
print("Gamma:", round(calc.gamma(S, K, V, T), 2))
```

See `examples/example_greeks.py`.

### Portfolio aggregation and plotting

```python
from option_calculator import Plot

plot = Plot()
exp = 30 / 365
params = [
    {"dType": "F", "price": 20000, "quant": 1,  "strike": 0,     "vola": 0,    "exp": exp},
    {"dType": "C", "price": 500,   "quant": 1,  "strike": 25000, "vola": 0.75, "exp": exp},
    {"dType": "P", "price": 100,   "quant": 1,  "strike": 15000, "vola": 0.75, "exp": exp},
]

plot.plotPL(13500, 28500, params, exp, step=10)

print("Delta:", plot.deltaFull(21000, params, exp))
print("P&L:  ", plot.p_l(21000, params, exp))
```

See `examples/example_plot.py`.

## Position format

A position is either an `OptionPosition` dataclass or a plain dictionary with the
same fields:

| Field    | Meaning                                                |
|----------|--------------------------------------------------------|
| `dType`  | `'C'` call, `'P'` put, `'F'` linear future             |
| `strike` | strike price (`> 0` for options; use `0` for futures)  |
| `vola`   | implied volatility as a fraction (e.g. `0.45`)         |
| `exp`    | time to expiry in years                                |
| `quant`  | signed quantity (positive = long, negative = short)    |
| `price`  | entry premium / price, used for P&L                     |

```python
from option_calculator import OptionPosition, Pricing

pricing = Pricing()
positions = [OptionPosition("C", 25000, 0.75, 30 / 365, quant=1, price=500)]
print(pricing.deltaFull(21000, positions))
```

Passing a positional `exp` to the aggregators **overrides** every position's expiry
(and `exp=0` is honoured). Inputs are never mutated.

## Conventions and limitations

- **Rate**: `r` is a continuously compounded risk-free rate and defaults to `0.0`.
  With `r = 0` the formulas reduce to the classic zero-rate Black-Scholes, the
  convention used for coin-margined / futures-style crypto options. Pass `r=` to
  use the discounted model.
- **Vega** is scaled per 1 percentage point of volatility (`VEGA_SCALE = 100`).
- **Theta** is expressed per calendar day (`DAYS_PER_YEAR = 365`).
- **Degenerate inputs**: `T = 0` (expired) and `V = 0` are valid and yield the
  discounted intrinsic value with deterministic greeks; other invalid inputs
  (`S ≤ 0`, `K ≤ 0`, `V < 0`, `T < 0`, unknown `dType`) raise `ValueError`.
- Only European vanilla options are supported. No dividends, no American exercise,
  no volatility smile.

## Project layout

```
src/option_calculator/
├── bsm.py         # Black-Scholes-Merton core (pure stdlib)
├── position.py    # OptionPosition dataclass
├── pricing.py     # portfolio aggregation (greeks, P&L, price grid)
├── plot.py        # optional matplotlib layer
└── searching.py   # delta-neutral price search
examples/          # runnable demo scripts
tests/             # pytest suite
```

## Development

```bash
pip install -e ".[plot,dev]"
ruff check src tests examples   # lint
ruff format --check src tests examples # formatting
pytest                          # tests
```

## Changelog and releases

See [CHANGELOG.md](CHANGELOG.md). Releases follow [Semantic Versioning](https://semver.org/);
see [CONTRIBUTING.md](CONTRIBUTING.md) for the release checklist.

## License

[MIT](LICENSE) © 2017 yzoz
