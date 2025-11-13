# `pyrcore`
Python package aiming to create a core of R programming language to optimize time series management.
## Supported Python distributions
This project is created and tested using the **CPython** team distribution.
## Installation
You can install the latest development version of the `pyrcore` package from **TestPyPI** like so:
```powershell
pip install -i https://test.pypi.org/simple/ pyrcore --no-deps
```
## Intended features
* Support for R atomic vectors and combination function `c()`
* Support for R matrixes
* Support for R `ts` class (time series)
* Support for R `mts` class (multivariate time series)
* Support for R `ts()` function
## Dependency policy
This project aims to be as package independent as possible.

At the moment, this project depends on `numpy`.

This project will **not** depend on `pandas` for **core functionalities**.
## Contribution
This project is part of my Final Degree Project (in spanish: *Trabajo de Fin de Grado* or *TFG*), so I won't be accepting contributions to this repository until the project is finished and defended.
However, no rule forbids me to learn from other people, so I'll be reading pull requests from forked repositories, but I will code any changes myself.

Once the project is defended, contributions will be open. To contribute, fork this repository and clone it locally.

There are two branches:
* **PyPI**: the main branch, for releases.
* **TestPyPI**: for pre-releases or development versions.

Pull requests from TestPyPI to PyPI will only be done by the owner when a new release is ready.