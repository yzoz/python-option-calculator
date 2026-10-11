# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-10-11

### Added
- First packaged release: Black-Scholes-Merton core, portfolio aggregation,
  plotting layer and delta-neutral search.
- Packaged the project as an installable `src/`-layout package (`option_calculator`)
  with `pyproject.toml`, optional `[plot]` (matplotlib) and `[dev]` extras.
- `OptionPosition` dataclass with field validation.
- Optional continuously compounded risk-free rate `r` across the pricing engine.
- Input validation with clear `ValueError` messages for all pricing methods.
- Test suite (`pytest`) and GitHub Actions CI (Python 3.9–3.12, ruff + pytest).
- `ruff` linting/formatting configuration.
- Documentation: expanded README, `CONTRIBUTING.md`, `CHANGELOG.md`, `docs/`.

### Changed
- Replaced the `BSM → Pricing → Plot` inheritance chain with composition.
- `Pricing` aggregators no longer mutate the input positions; an explicit `exp`
  argument overrides positions and `exp = 0` is honoured.
- `Search.searchDelta` now returns a list of results instead of printing, and
  compares deltas with a tolerance.
- Deduplicated portfolio aggregation into a single `_aggregate` helper.
- Vega/Theta scaling and day-count constants are now named (`VEGA_SCALE`,
  `DAYS_PER_YEAR`).

### Fixed
- Consistent `dType` handling across all methods (unknown types now raise instead
  of silently producing wrong results).
- Correct discounted intrinsic value for expired / zero-volatility options.

[Unreleased]: https://github.com/yzoz/python-option-calculator/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yzoz/python-option-calculator/releases/tag/v0.1.0
