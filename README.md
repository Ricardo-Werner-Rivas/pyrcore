# `pyrcore`
Python package aiming to create a core of R programming language to optimize time series management.
## Supported Python distributions
* [CPython](https://www.python.org/downloads)

This project is created and tested using the [3.13.11 CPython team distribution](https://www.python.org/downloads/release/python-31311/).
## Installation
You can install the latest development version of the `pyrcore` package from **TestPyPI** like so:
```powershell
pip install -i https://test.pypi.org/simple/ pyrcore --no-deps
```
## Current features
* Support for R atomic vectors
* Support for combination function `c()`
## Intended features
* ~~Support for R atomic vectors~~ (stable)
* ~~Support for combination function `c()`~~ (stable)
* ~~Support for R matrixes and R `matrix()` function~~ (functional)
* Support for R `ts` class (time series)
* Support for R `mts` class (multivariate time series)
* Support for R `ts()` function
## Dependency policy
This project aims to be as package independent as possible.

At the moment, this project depends on `numpy` for core functionalities and `pandas` for optional ones.

This project will **NOT** depend on `pandas` for <ins>**core functionalities**</ins>.
## Contribution
This project is part of my <ins>Final Degree Project</ins> (in spanish: *Trabajo de Fin de Grado* or *TFG*), so I won't be accepting contributions to this repository until the project is finished and defended.
However, no rule forbids me to learn from other people, so I'll be reading pull requests from forked repositories, but I will code any changes myself. I will not incorporate any changes that I don't understand.

Once the project is defended, contributions will be open. To contribute, fork this repository and clone it locally.

There are two branches:
* **PyPI**: the main branch, for releases.
* **TestPyPI**: for pre-releases or development versions.

Pull requests from TestPyPI to PyPI will only be done by the owner when a new release is ready.