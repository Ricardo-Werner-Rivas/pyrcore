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

#^ The different types of comments require the "Colorful Comments Refreshed" extension for VSCode to be properly distinguished

#* IMPORTS
# Class Vector
from .core import Vector,VT
# NumPy
import numpy as np
# Iterable
from typing import Iterable

#* COMBINATION FUNCTION (c(), for vector creation)
def c(*data:VT|list|tuple|np.ndarray,**named_data:VT)->Vector[VT]:
    #& Missing comments for code
    """
    Creates an *R-like* atomic vector. The returned object is a `Vector` instance.\n
    ---
    Arguments:
        *data (`Any`): Stream of unnamed values for the vector, resulting in a tuple of values.
            Values can be of any type.
        **named_data (`dict[str,Any]`): Stream of named values for the vector. They are passed as keyword arguments.
            Values can be of any type. Arguments' names will be the names for the vector.
    ---
    Returns:
        Vector: *R-like* atomic vector.
    """
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
        while any((isinstance(value,Iterable) for value in data)):
            for value in data:
                data_list.extend(tuple(value.values()) if isinstance(value,dict) else value) if isinstance(value,Iterable) else data_list.append(value)
            data=tuple(data_list)
            data_list.clear()
        del data_list
        for value in data:
            #// # Initialize data_type
            #// data_type=None
            #// # If data is in NumPy scalar types
            #// if isinstance(value,np.generic):
            #//     # Put its Python equivalent in a list
            #//     value=[value.item()]
            #// # Else, if value is a NumPy array
            #// elif isinstance(value,np.ndarray):
            #//     # Try listing
            #//     try:
            #//         # List its values in Python built-in types
            #//         value=[item.item() if isinstance(item,np.generic) else item for item in value]
            #//     # If array is 0-dimensional
            #//     except TypeError:
            #//         # Put its Python equivalent in a list
            #//         value=[value.item()]
            #//     # General exception
            #//     except Exception as excep:
            #//         raise type(excep)(
            #//             "A fatal error has occured. Please report this in our issues page: {}\
            #//             \n\nPlease include, along with the error type, the following message in your report:\n\"{}\""\
            #//             .format("https://github.com/Ricardo-Werner-Rivas/pyrcore/issues",excep)
            #//         ) from None
            #// # Else, if value is a dictionary
            #// elif isinstance(value,dict):
            #//     # Take its values
            #//     value=list(value.values())
            # If value is an R-like vector (class Vector)
            if isinstance(value,Vector):
                # Store its attributes
                for k,v in value.attributes.items():
                    attributes.setdefault(k,v)
                if "names" not in attributes:
                    attributes["names"]=names
            #//     # List its values
            #//     value=[item for item in value._data]
            #// elif not isinstance(value,(list,tuple)):
            #//     try:
            #//         value=list(value) if type(value)!=str else [value]
            #//     except TypeError:
            #//         value=[value]
            #// data_list.extend(value)
            #// try:
            #//     Vector(data)
            #// except TypeError:
            #//     data_type=str(type(value[0])) if "'list'" in str(type(value)) else str(type(value))
            #//     data_type=data_type[data_type.find("'")+1:data_type.rfind("'")]
            #//     raise TypeError(f"Data type \"{data_type}\" not supported for atomic vectors") from None
            #// except Exception as excep:
            #//     raise type(excep)(
            #//             "A fatal error has occured. Please report this in our issues page: {}\
            #//             \n\nPlease include, along with the error type, the following message in your report:\n\"{}\""\
            #//             .format("https://github.com/Ricardo-Werner-Rivas/pyrcore/issues",excep)
            #//         ) from None
        return Vector(data,**attributes)