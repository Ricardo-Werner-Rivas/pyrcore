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
# Iterable and TYPE_CHECKING
from typing import Iterable,TYPE_CHECKING

# Annotations' classes imports
if TYPE_CHECKING:
    from .subclasses import TimeSeries

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
    if Rtype and isinstance(Rtype,str):
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

#* AUTOCORRELATION FUNCTIONS
# Simple AutoCorrelation Function (ACF)
def acf(ts:TimeSeries,lag:int)->dict[int,]:
    mean=sum(ts)/len(ts)
    result=tuple()
    for k in range(lag+1):
        result=(*result,sum(tuple((ts[i]-mean)*(ts[i-k]) if i>=k else 0 for i in range(len(ts))))/sum(tuple((ts[i]-mean)**2 for i in range(len(ts)))))
    return dict(zip(tuple(range(lag+1)),(1,*result)))

# Partial AutoCorrelation Function (PACF)
def pacf(ts:TimeSeries,lag:int)->dict[tuple[int],]:
    p=acf(ts,lag)
    result:dict[tuple[int],]={}
    for k in range(1,lag+1):
        if k==1:
            result[(1,1)]=p[1]
        else:
            result[(k,k)]=(p[k]-sum(tuple(result[(k-1,j)]*p[k-j] for j in range(1,k))))/(1-sum(tuple(result[(k-1,j)]*p[j] for j in range(1,k))))
            for j in range(1,k):
                result[(k,j)]=result[(k-1,j)]-result[(k,k)]*result[(k-1,k-j)]
    return dict(zip(sorted(tuple(result.keys())),tuple(result[k] for k in sorted(tuple(result.keys())))))