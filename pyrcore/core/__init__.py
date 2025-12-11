"""
Module containing the core of the package.\n
---
## Submodule `core`
Contains the class `RObject`, base class for *R-like* objects.\n
---
## Submodule `vector`
Contains the class `Vector`, which is a subclass of `RObject`.
Vectors are the base of R behaviour, so they are included in the core of the package.
"""
from .core import RObject
from .vector import Vector