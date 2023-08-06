# Brad

![gh-actions](https://github.com/tcbegley/brad/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/tcbegley/brad/branch/main/graph/badge.svg?token=aJUDsDeu1t)](https://codecov.io/gh/tcbegley/brad)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/brad)
![PyPI - License](https://img.shields.io/pypi/l/brad)


Brad is a Python package for Bootstrap, permutation tests and other resampling
functions.

## Development

You can install `brad` and its dependencies from source from the root of this
repo with

```sh
python -m pip install .
```

Tests and linters are run with [`nox`][nox]. Install with

```sh
python -m pip install nox
```

You can then run one of the pre-configured nox "sessions" with

```sh
nox -s lint
```

The available sessions are:
- `lint`: run source code linters (`black`, `flake8`, `isort`, `mypy`)
- `test`: run test suite with PyTest. Will try to run on Python 3.7, 3.8 and
3.9.
- `test-3.x`: run tests for only Python 3.x (replace x with 7, 8, or 9)
- `format`: format source code with `black` and `isort`.

Running only the command

```sh
nox
```

will run `lint` and `test` by default (so in particular `nox` will not format
the source code unless explicitly told to do so).

[nox]: https://nox.thea.codes
