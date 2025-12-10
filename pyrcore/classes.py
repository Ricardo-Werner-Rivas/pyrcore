#*===============================================================================================================================
#* LEGEND
#*-------------------------------------------------------------------------------------------------------------------------------
#! Missing
#& Missing unimportant
#? Questions
#* Section
#^ Important
# Normal comment
#// Deprecated code
#*===============================================================================================================================

#^ The different types of comments require the "Colorful Comments Refreshed" extension for VSCode to be properly distinguished

#* IMPORTS
# NumPy
import numpy as np
# TypeVar and Generic
from typing import TypeVar,Generic,Iterable
# Class Vector
from .core import Vector
# Combination function
from .functions import c

#* TYPING
# Define new variable type with TypeVar
MT=TypeVar("SupportedTypes")

#* CLASS "matrix"
class matrix(Vector,Generic[MT]):
    #& Missing code comments
    """
    Replicates R matrixes and R `matrix()` function.\n
    Unlike class `Vector`, this class properly creates the object so no auxiliar functions are needed.\n
    ---
    Attributes:
    """
    #* METHODS
    # __init__
    def __init__(
        self,
        data:Vector|Iterable|None=None,nrow:int|None=None,ncol:int|None=None,byrow:bool=False,
        *,
        dimnames:tuple[Iterable[str]|None,Iterable[str]|None]|None=None,
        **attributes
    ):
        """
        Arguments:
            data (`Vector`|`Iterable`|`None`, Optional): *Matrix-like* Python object to convert to an *R-like* matrix.
            nrow (`int`|`None`, Optional): Number of rows to split the data. If not given, it is calculated.
            ncol (`int`|`None`, Optional): Number of colums to split the data. If not given, it is calculated.
            byrow (`bool`, Optional): Wether if the matrix will be built by rows (`True`) or by columns (`False`). `False` by default.
            dimnames (`tuple[Iterable[str]|None,Iterable[str]|None]`|`None`, Optional): Ideally a tuple with the names for the rows (first position)
                and the names for the columns (second position).
                Any two position iterable works fine. Tuple is recommended if you just want to name the columns, so you can pass the following:
                ```
                m=matrix(<data>,<nrow>,2,dimnames=(,["name1","name2"]))
                ```
                If only an iterable of strings is received, it will be passed to the rows.
            **attributes (`dict`, Optional): Stream of keyword arguments defining the matrix R attributes.
                Matrixes support `dim` and `dimnames` attributes, which contains the matrix dimensions.
        """
        if not isinstance(data,Vector):
            data=c(data)
        if not nrow and not ncol:
            nrow=len(data)
            ncol=1
        elif nrow:
            ncol=len(data)//nrow
            if len(data)%nrow>0:ncol+=1
        elif ncol:
            nrow=len(data)//ncol
            if len(data)%ncol>0:nrow+=1
        
        if len(data)<nrow*ncol:
            if data.type in [int,float]:
                data=c(data,[0 for i in range(nrow*ncol-len(data))])
            else:
                data=c(data,[None for i in range(nrow*ncol-len(data))])
        
        #! Implement "byrow"