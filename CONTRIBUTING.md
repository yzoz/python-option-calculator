# Contributing

Thanks for your interest in improving the Vanilla Option Calculator.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[plot,dev]"
```

## Before submitting a change

```bash
ruff check src tests examples   # lint
ruff format src tests examples  # auto-format
pytest                          # run the test suite
```

All three must pass. CI runs the same checks across Python 3.9–3.12.

## Guidelines

- Keep the pricing **core** (`bsm.py`, `pricing.py`, `position.py`, `searching.py`)
  free of external dependencies; only `plot.py` may import `matplotlib`.
- Add or update tests for any behavioural change.
- Update `CHANGELOG.md` under `## [Unreleased]`.
- Follow Semantic Versioning for user-visible changes.

## Release checklist

1. Ensure `master` is green in CI and the working tree is clean.
2. Update the version in `pyproject.toml` and `src/option_calculator/__init__.py`.
3. Move the `## [Unreleased]` entries in `CHANGELOG.md` into a new version section
   with the release date, and add the compare links.
4. Commit: `Release vX.Y.Z`.
5. Tag and push:
   ```bash
   git tag vX.Y.Z
   git push origin master --tags
   ```
6. (Optional) Build and publish: `python -m build` then `twine upload dist/*`.
