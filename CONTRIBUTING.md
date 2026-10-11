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
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   git push origin master --tags
   ```
6. Pushing a `v*` tag triggers the **Release** workflow
   (`.github/workflows/release.yml`), which builds the distributions and
   publishes them to PyPI via [Trusted Publishing](https://docs.pypi.org/trusted-publishers/).
7. (Optional) Create a GitHub Release from the tag and paste the matching
   `CHANGELOG.md` section as the description.

### PyPI publishing

Publishing uses Trusted Publishing (OIDC) — no API tokens or repository
secrets are required. One-time setup:

1. Register the project on PyPI and add a **pending publisher** at
   <https://pypi.org/manage/account/publishing/> matching:
   - PyPI Project Name: `option-calculator`
   - Owner: `yzoz`
   - Repository name: `python-option-calculator`
   - Workflow name: `release.yml`
   - Environment name: `pypi`
2. Push a `v*` tag (step 5 above). The `publish` job runs in the `pypi`
   environment and uploads `dist/` via `pypa/gh-action-pypi-publish`.

To publish an existing version (for example after workflow-only changes)
without moving a tag, run the workflow manually:

```bash
gh workflow run release.yml        # or: Actions → Release → Run workflow
```

> A version can only be uploaded to PyPI once. After a successful upload,
> bump the version before publishing again.

### Manual build (local check)

```bash
python -m build          # produces dist/*.whl and dist/*.tar.gz
twine check dist/*       # validate metadata before publishing
```
