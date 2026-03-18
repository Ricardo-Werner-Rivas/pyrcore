# `pyrcore`
[Python]:https://img.shields.io/badge/python-3.14.3-&
[Supported Python]:https://img.shields.io/badge/python->=3.14.3-&?label=CPython
[TestPyPI Version]:https://img.shields.io/badge/dynamic/json?url=https://test.pypi.org/pypi/pyrcore/json&query=$.info.version&label=TestPyPI
[License]:https://img.shields.io/github/license/Ricardo-Werner-Rivas/pyrcore

Python package aiming to create a core of R programming language to optimize time series management.

|About|Information|
|---|---|
|Development Python version|[![Python]](https://www.python.org/downloads/release/python-3143/)|
|Supported Python distributions|[![Supported Python]](https://www.python.org/downloads)|
|Packaging|[![TestPyPI Version]](https://test.pypi.org/project/pyrcore/) [![License]](https://github.com/Ricardo-Werner-Rivas/pyrcore/blob/TestPyPI/LICENSE)|
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
* ~~Support for R matrixes and R `matrix()`~~ function (stable)
* <ins>Support for R `ts` class</ins> (time series)
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