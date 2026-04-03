"""
Provides several R objects and functions.\n
---
## Implemented features
* Class `Vector`: Implementation of R atomic vectors.
* Combination function (`c()`): Implementation of R `c()` function.
## Remaining intended features
* Class `matrix`: Implementation of R matrixes and `matrix()` function.
* Class `TimeSeries`: Implementation of R univariate time series.
* Class `MultiVarTimeSeries`: Implementation of R multivariate time series.
* Function `ts()`: Implementation of R `ts()` function.
"""
from .core import Vector
from .subclasses import matrix
from .functions import c