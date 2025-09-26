Running tests

This project includes a concurrency unit test for the `ClientLookup` class.

Prerequisites
- Developer: install `uv` locally (we assume developers install it ahead of time). The CI uses the uv curl installer.
- Optionally install uv with pipx for local development:

  python -m pip install --upgrade pip pipx
  python -m pipx ensurepath
  python -m pipx install uv

Run tests (developer)

From the project root (`/path/to/pYSFReflector3`):

  # install project deps into uv-managed venv
  uv install -r requirements.txt

  # run tests inside uv-managed environment
  uv run pytest -q

If you want to reproduce the exact environment recorded in the repository lockfile, use `uv sync` (this will read `uv.lock` and create/update `.venv` accordingly):

  # sync project environment from uv.lock
  uv sync

CI notes

- The GitHub Actions workflow installs `uv` via the upstream curl installer:
  curl -LsSf https://astral.sh/uv/install.sh | sh

- CI then runs `uv install -r requirements.txt` and `uv run pytest -q`.

Notes
- The `YSFReflector` script contains runtime startup code; tests import only the `ClientLookup` class by extracting its source to avoid starting the server. Do not run `YSFReflector` directly while running tests unless you want the server to run.
- The tests are located in `tests/test_clientlookup.py` and are designed to exercise concurrent add/find/remove operations; they assert internal consistency (no stale indices) rather than strict snapshot semantics (concurrent removes are allowed).
