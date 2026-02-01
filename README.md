# `pyrcore`
[Python]:https://img.shields.io/badge/python-3.13.11-&
[Supported Python]:https://img.shields.io/badge/python->=3.13.11-&
[Version]:https://img.shields.io/pypi/v/pyrcore
[License]:https://img.shields.io/github/license/Ricardo-Werner-Rivas/pyrcore

Python package aiming to create a core of R programming language to optimize time series management.

|About|Information|
|---|---|
|Development Python version|[![Python]](https://www.python.org/downloads/release/python-31311/)|
|Supported Python versions|![Supported Python]|
|Packaging|[![Version]](https://pypi.org/project/pyrcore/) ![License]|
## Supported Python distributions
* [CPython](https://www.python.org/downloads)

This project is created and tested using the [3.13.11 CPython team distribution](https://www.python.org/downloads/release/python-31311/).
## Installation
You can install the `pyrcore` package from **PyPI** like so:
```powershell
pip install pyrcore
```
## Current features
|Feature|PyPI|TestPyPI|Status|
|-------|----|--------|------|
|R atomic vectors|❌|✅|**Stable**|
|Combination function `c()`|❌|✅|**Stable**|
|R matrixes and `matrix()` function|❌|❌|Development|
|R `ts` class|❌|❌||
|R `mts` class|❌|❌||
|`ts()` function|❌|❌||
## Intended features
* Support for R atomic vectors
* Support for combination function `c()`
* Support for R matrixes
* Support for `matrix()` R function
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
### Branch merging
To merge branches properly with PyPI branch in your cloned repository, you will need to have the `.gitattributes` file in the PyPI branch and execute the following commands, while in repo directory, in your **PowerShell**:
```powershell
git config merge.keepPyPIFiles.name "Keep README.md and setup.cfg from PyPI branch on merge"
git config merge.keepPyPIFiles.driver "bash -c 'cp $(git rev-parse --show-toplevel)/$3 $2'"
```
This way, `README.md` and `setup.cfg` files will not be overwritten in the PyPI branch.
### Building
To build the project you only have to fork this repository and clone your fork.

Each code file starts with a comment legend. For this to be useful, you will need to install the <ins>"Colorful Comments Refreshed"</ins> extension for **VSCode** and change the last tag from `todo` to `¡`.
<details>
<summary>The final configuration of the extension (in user's <code>settings.json</code>) is the following:</summary>

```json
{
    "colorful-comments-refreshed.tags": [
        {
            "tag": "!",
            "color": "#FF2D00",
            "strikethrough": false,
            "backgroundColor": "transparent"
        },
        {
            "tag": "?",
            "color": "#0076FF",
            "strikethrough": false,
            "backgroundColor": "transparent"
        },
        {
            "tag": "//",
            "color": "#474747",
            "strikethrough": true,
            "backgroundColor": "transparent"
        },
        {
            "tag": "^",
            "color": "#EAF622",
            "strikethrough": false,
            "backgroundColor": "transparent"
        },
        {
            "tag": "*",
            "color": "#28FF00",
            "strikethrough": false,
            "backgroundColor": "transparent"
        },
        {
            "tag": "&",
            "color": "#FF06A0",
            "strikethrough": false,
            "backgroundColor": "transparent"
        },
        {
            "tag": "~",
            "color": "#BE00FF",
            "strikethrough": false,
            "backgroundColor": "transparent"
        },
        {
            "tag": "¡",
            "color": "#FF8C00",
            "strikethrough": false,
            "backgroundColor": "transparent"
        }
    ]
}
```
</details>
