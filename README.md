# `pyrcore`
Python package aiming to create a core of R programming language to optimize time series management.
## Supported Python distributions
* [CPython](https://www.python.org/downloads)

This project is created and tested using the [3.13.9 **CPython** team distribution](https://www.python.org/downloads/release/python-3139).
## Instalation
You can install the `pyrcore` package from **PyPI** like so:
```powershell
pip install pyrcore
```
## Intended features
* Support for R atomic vectors and combination function `c()`
* Support for R matrixes
* Support for R `ts` class (time series)
* Support for R `mts` class (multivariate time series)
* Support for R `ts()` function
## Dependency policy
This project aims to be as package independent as possible.

At the moment, this project depends on `numpy` for core functionalities and `pandas` for optional ones.

This project will **not** depend on `pandas` for **core functionalities**.
## Contribution
This project is part of my Final Degree Project (in spanish: *Trabajo de Fin de Grado* or *TFG*), so I won't be accepting contributions to this repository until the project is finished and defended.
However, no rule forbids me to learn from other people, so I'll be reading pull requests from forked repositories, but I will code any changes myself.

Once the project is defended, contributions will be open. To contribute, fork this repository and clone it locally.

There are two branches:
* **PyPI**: the main branch, for releases.
* **TestPyPI**: for pre-releases or development versions.

Pull requests from TestPyPI to PyPI will only be done by the owner when a new release is ready.
### Branch merging
To merge branches properly with PyPI branch in your cloned repository, you will need to have the `.gitattributes` file in the PyPI branch and execute the following commands, while in repo directory, in your PowerShell:
```powershell
git config merge.keepPyPIFiles.name "Keep README.md and setup.cfg from PyPI branch on merge"
git config merge.keepPyPIFiles.driver "bash -c 'cp $(git rev-parse --show-toplevel)/$3 $2'"
```
Or in your git bash terminal:
```bash
git config merge.keepPyPIFiles.name "Keep README.md and setup.cfg from PyPI branch on merge"
git config merge.keepPyPIFiles.driver "bash -c 'cp $(git rev-parse --show-toplevel)/$3 $2'"
```
This way, `README.md` and `setup.cfg` files will not be overwritten in the PyPI branch.