Running tests

This project includes a concurrency unit test for the `ClientLookup` class.

Prerequisites
- Use the project's virtualenv Python at `pyenv/bin/python`.
- Install test runner if needed (we use pytest in the venv). To install:

  /Users/dbehnke/development/pYSFReflector3/pyenv/bin/python -m pip install pytest

Run tests

From the project root (`/path/to/pYSFReflector3`):

  /Users/dbehnke/development/pYSFReflector3/pyenv/bin/pytest -q

Notes
- The `YSFReflector` script contains runtime startup code; tests import only the `ClientLookup` class by extracting its source to avoid starting the server. Do not run `YSFReflector` directly while running tests unless you want the server to run.
- The tests are located in `tests/test_clientlookup.py` and are designed to exercise concurrent add/find/remove operations; they assert internal consistency (no stale indices) rather than strict snapshot semantics (concurrent removes are allowed).
