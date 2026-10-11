# AGENTS.md

Guidance for AI agents and maintainers working in this repository.

## What this is

`option-calculator` (import name `option_calculator`) — Black-Scholes-Merton
pricing and greeks for European vanilla options in **pure Python**. The pricing
core depends only on the standard library; `matplotlib` is an optional extra for
the plotting layer only.

- **Published on PyPI**: <https://pypi.org/project/option-calculator/>
- **Repository**: <https://github.com/yzoz/python-option-calculator>
- **Default branch**: `master`

## Golden rules

These three are the reason this file exists. Follow them on every change.

1. **Keep `CHANGELOG.md` current.** Every user-visible change gets an entry under
   `## [Unreleased]` in the same commit as the change. See
   [CHANGELOG discipline](#changelog-discipline).
2. **Keep the repo release-ready.** `master` must always be in a state where a
   new `vX.Y.Z` tag builds cleanly and publishes to PyPI without extra edits.
3. **Never let the two version strings drift.** A release is only valid when
   `pyproject.toml` and `src/option_calculator/__init__.py` agree. See
   [Version management](#version-management).

## Repository layout

```
src/option_calculator/
├── bsm.py         # BSM core + greeks (pure stdlib)
├── position.py    # OptionPosition dataclass
├── pricing.py     # portfolio aggregation (greeks, P&L, price grid)
├── plot.py        # optional matplotlib layer (ONLY module importing matplotlib)
├── searching.py   # delta-neutral price search
└── __init__.py    # public API + __version__ (lazy Plot export)
tests/             # pytest suite (mirrors the modules above)
examples/          # runnable demo scripts
.github/workflows/ # ci.yml, release.yml
pyproject.toml     # metadata, deps, ruff/pytest config, version
CHANGELOG.md       # Keep a Changelog
CONTRIBUTING.md    # dev setup + release checklist
AGENTS.md          # this file
README.md          # user-facing docs (mirrored to the PyPI page)
```

## Development setup and checks

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[plot,dev]"

ruff check src tests examples        # lint
ruff format src tests examples       # auto-format
ruff format --check src tests examples
pytest                               # test suite
python -m build && twine check dist/*  # verify the package builds cleanly
```

All of `ruff check`, `ruff format --check` and `pytest` **must pass** before a
change is done. CI (`.github/workflows/ci.yml`) runs exactly these on Python
3.9–3.12.

## Code conventions

- Target **Python 3.9+**. Use `from __future__ import annotations`.
- Style is enforced by **ruff** (rules `E,F,W,I,B,UP,D`, Google docstrings,
  line length 100). The layout is `src/`.
- **Every public class and method needs a Google-style docstring.** Tests and
  `examples/` are exempt from the `D` rules (see per-file ignores in
  `pyproject.toml`).
- **Keep the core dependency-free.** `bsm.py`, `position.py`, `pricing.py` and
  `searching.py` must not import `matplotlib`. Only `plot.py` may, and `Plot`
  is exported lazily from `__init__.py` via `__getattr__`.
- **Composition, not inheritance.** `Pricing` owns a `BSM`; `Plot` and `Search`
  own a `Pricing`. Do not reintroduce the old `BSM ← Pricing ← Plot` chain.
- **Never mutate inputs.** Aggregators take positions as `OptionPosition` or a
  plain mapping and must not write back to them.
- Prefer `TypedDict` over `dict[str, Any]` for structured rows (see
  `SearchRow` in `searching.py`).
- Domain constants live in `bsm.py`: `VEGA_SCALE = 100.0`, `DAYS_PER_YEAR = 365`.
  Reuse them; do not re-declare magic numbers.
- Conventions that must stay documented: `r` defaults to `0.0` (continuous
  compounding; classic zero-rate BS, the futures-style crypto convention).

## Version management

The version is duplicated in **two** files and both must match:

| File | Field |
|------|-------|
| `pyproject.toml` | `version = "X.Y.Z"` |
| `src/option_calculator/__init__.py` | `__version__ = "X.Y.Z"` |

Bump both together, following [Semantic Versioning](https://semver.org).
A `tests/test_package.py` check only asserts `__version__` is truthy — the two
strings are **not** verified against each other, so keep them in sync by hand.

`requires-python` is `>=3.9`. The classifier list and `[project.optional-dependencies]`
extras (`plot`, `dev`) should reflect reality.

## CHANGELOG discipline

`CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

- Work in progress goes under `## [Unreleased]` at the top.
- Use the standard groups in this order: **Added, Changed, Deprecated, Removed,
  Fixed, Security** — only include groups you actually used.
- One bullet per user-visible change, written for users (not "refactored X"
  unless it changes behaviour). Internal-only refactors still count as
  `Changed` if they touch the public API.
- Keep the compare-link block at the bottom in sync:
  `[Unreleased]: .../compare/v<latest>...HEAD` and a link per released tag.
- **At release time**, move the `[Unreleased]` body into a new
  `## [X.Y.Z] - YYYY-MM-DD` section, leave an empty `## [Unreleased]` behind,
  and add the new version's compare link.

> Rule of thumb: if a reviewer would ask "should this be in the changelog?", the
> answer is yes — add it in the same commit as the change.

## Release process

The end-to-end checklist lives in `CONTRIBUTING.md`; this is the short version.

1. Ensure `master` is green in CI and the working tree is clean.
2. Bump the version in **both** files (see above) and fill in `CHANGELOG.md`.
3. Commit: `Release vX.Y.Z`.
4. Tag and push — this triggers the **Release** workflow:
   ```bash
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   git push origin master --tags
   ```
5. `.github/workflows/release.yml` then builds `dist/` and publishes to PyPI
   via **Trusted Publishing** (OIDC, no tokens/secrets). The `publish` job runs
   in the `pypi` environment.
6. (Optional) Create a GitHub Release from the tag and paste the matching
   `CHANGELOG.md` section as its description.

### PyPI publishing notes

- Trusted Publishing is configured as a PyPI *pending publisher* for:
  project `option-calculator`, owner `yzoz`, repo `python-option-calculator`,
  workflow `release.yml`, environment `pypi`. If any of these change, update the
  publisher on PyPI or publishing will fail with an OIDC mismatch.
- `release.yml` also has a `workflow_dispatch` trigger, so the workflow can be
  run manually (Actions → Release → Run workflow) to publish an existing version
  without moving a tag.
- **A version can be uploaded to PyPI only once.** After a successful upload,
  bump the version before publishing again.
- The **PyPI landing page renders `README.md` as of the upload**. Editing the
  README without a new release will *not* update the PyPI page. To refresh it,
  release a new version.
- Trusted Publishing lives in GitHub Actions only — there is no PyPI API token
  in this repo and none should be added.

## Gotchas

- `.gitignore` covers `dist/` and `build/`; never commit build artifacts.
- `theo()` raises `ValueError` for `dType='F'` (a linear future has no premium).
- `T == 0` and `V == 0` are **valid** degenerate inputs, not errors.
- The sdist does not ship `examples/` or `CONTRIBUTING.md`; only
  `src/`, `tests/`, `README.md`, `LICENSE` and `pyproject.toml`. Add a
  `MANIFEST.in` if more needs to ship.
