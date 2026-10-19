# Contributing to youtube-analytics

Thanks for considering a contribution. Issues, discussions and PRs are all
welcome.

## Getting set up

Python 3.9 or newer with Tkinter (on Debian or Ubuntu: `sudo apt-get install python3-tk`). `pip install -r requirements.txt`, then `python app.py`.

## Running the checks

`pip install -r requirements-test.txt` then `pytest -q tests`. The tests cover `analytics.py` and need no display. CI runs them on every PR.

## Ground rules

- Open an issue or discussion before large changes, so effort isn't wasted.
- Keep PRs focused: one change per PR.
- New behavior needs a test where the repo has a test suite.
- CI must pass before merge.

## Licensing

By contributing you agree your contributions are licensed under the repo's
MIT license.
