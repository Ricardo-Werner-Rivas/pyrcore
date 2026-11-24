# `pyrcore`
[Python]:https://img.shields.io/badge/python-3.15.2-&
[Supported Python]:https://img.shields.io/badge/python->=3.10-&?label=CPython
[TestPyPI Version]:https://img.shields.io/badge/dynamic/json?url=https://test.pypi.org/pypi/pyrcore/json&query=$.info.version&label=TestPyPI
[License]:https://img.shields.io/github/license/Ricardo-Werner-Rivas/pyrcore

|About|Information|
|---|---|
|Development Python version|[![Python]](https://www.python.org/downloads/release/python-3152/)|
|Supported Python distributions|[![Supported Python]](https://www.python.org/downloads)|
|Packaging|[![TestPyPI Version]](https://test.pypi.org/project/pyrcore/) [![License]](https://github.com/Ricardo-Werner-Rivas/pyrcore/blob/TestPyPI/LICENSE)|
## About the Project
`pyrcore` is a Python package that provides a set of R native objects to simplify coding tasks related to time series analysis in Python.
This simplification easier Python/R learning, a smoother transition between the two languages' usages and improved time-bound data management, as periodic time periods are now managed by the recreation of R `ts` objects using integer atomic vectors instead of `datetime` objects.
## Table of Contents
* [Installation](#installation)
* [Current Features](#current-features)
* [Intended Features](#intended-features)
* [Dependency Policy](#dependency-policy)
* [Contribution](#contribution)
* [Building](#building)
## Installation
You can install the latest development version of the `pyrcore` package from **TestPyPI** like so:
```powershell
pip install -i https://test.pypi.org/simple/ pyrcore --no-deps
```
## Current Features
* Support for R atomic vectors
* Support for combination function `c()` for atomic vectors' creation
* Support for R matrixes and R `matrix()` function
* Support for R `ts` class (`TimeSeries`)
## Intended Features
* ~~Support for R atomic vectors~~ (stable)
* ~~Support for combination function `c()`~~ (stable)
* ~~Support for R matrixes and R `matrix()` function~~ (stable)
* ~~Support for R `ts` class (`TimeSeries`)~~ (stable)
* <ins>Support for R `mts` class (multivariate time-series)</ins> (development)
* Support for R `ts()` function
## Dependency Policy
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
### Building
To build the project you only have to fork this repository and clone your fork.

Each code file starts with a comment legend. For this to be useful, you will need to install the <ins>[Colorful Comments Refreshed](https://marketplace.visualstudio.com/items?itemName=AllemandInstable.colorful-comments-refreshed)</ins> extension for **VSCode** and change the last tag from `todo` to `¡`.
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