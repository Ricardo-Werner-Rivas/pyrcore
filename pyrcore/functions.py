#*==============================================================================================================================
#* LEGEND
#*------------------------------------------------------------------------------------------------------------------------------
#! Missing
#& Missing unimportant
#~ Revision notes
#? Questions
#* Section
#^ Important
# Normal comment
#// Deprecated code
#*==============================================================================================================================

#* IMPORTS
# Class Vector
from .core import Vector
# VT type variable
from .core.vector import VT
# NumPy
import numpy as np
# Iterable
from typing import Iterable

#* COMBINATION FUNCTION (c(), for vector creation)
def c(*data:VT|list|tuple|np.ndarray,Rtype:type|str|None=None,**named_data:VT)->Vector[VT]:
    #& Missing comments for code
    """
    Creates an *R-like* atomic vector. The returned object is a `Vector` instance.
    
    Arguments
    ---------
    data : `tuple[Any]`
        Stream of unnamed values for the vector, resulting in a tuple of values.
        Values can be of any type.
    Rtype : `type`|`str`|`None`, Optional
        Type to which the data will be transformed to. Introduce `object` for multitype vectors.
    named_data : `dict[str,Any]`
        Stream of named values for the vector. They are passed as keyword arguments. Values can be of any type.
        Arguments' names will be the names for the vector.
    
    Returns
    -------
    Vector
        *R-like* atomic vector.
    """
    # Control Rtype's type
    if isinstance(Rtype,str):
        Rtype=eval(Rtype)
    # Raise error if both named and unnamed data are given
    if data and named_data:
        raise ValueError("Vector cannot store both named and unnamed data")
    # Return empty vector if no data was introduced
    elif not data and not named_data:
        return Vector([])
    # In the rest of cases (*data or **named_data)
    else:
        # Store the names
        names=list(named_data.keys()) if named_data else None # If no names, then store None
        # Create an "attributes" variable
        attributes:dict[str,]={"names":names}
        # Prepare the passed data
        data=data or list(named_data.values())
        # Empty list to store the data
        data_list=[]
        # Prepare the data to vectorize it
        while (lambda:any(isinstance(value,Iterable) and not isinstance(value,str) for value in data))():
            for value in data:
                if isinstance(value,str):
                    data_list.append(value)
                    continue
                data_list.extend(tuple(value.values()) if isinstance(value,dict) else value) if isinstance(value,Iterable) else data_list.append(value)
            data=tuple(data_list)
            data_list.clear()
        del data_list
        for value in data:
            # If value is an R-like vector (class Vector)
            if isinstance(value,Vector):
                # Store its attributes
                for k,v in value.attributes.items():
                    attributes.setdefault(k,v)
                if "names" not in attributes:
                    attributes["names"]=names
        return Vector(data,Rtype=Rtype,**attributes)