#*==============================================================================================================================
#* LEGEND
#*------------------------------------------------------------------------------------------------------------------------------
#! Missing
#? Questions
#* Section
#^ Important
# Normal comment
#// Alternative or deprecated code
#*==============================================================================================================================

#^ The different types of comments require the "Colorful Comments Refreshed" extension for VSCode to be properly distinguished

#* IMPORTS
# Class Vector
from .core import Vector
# NumPy
import numpy as np

#* FUNCTIONS
# Combination function (c(), for vector creation)
def c(*data:list,**named_data:dict[str,])->Vector:
    """
    Creates an atomic vector like in R. The returned object if a `Vector` instance.\n
    ---
    Arguments:
        *data (`list`): Stream of unnamed values for the vector.
        **named_data (`dict[str,Any]`): Stream of named values for the vector. They are passed as keyword arguments.
    ---
    Returns:
        Vector: Atomic vector "Rlike".
    """
    if data and named_data:
        raise ValueError("Vector cannot store both named and unnamed data")
    elif not data and not named_data:
        return Vector(None)
    else:
        names=list(named_data.keys()) if named_data else None
        data=data or named_data
        data_list=[]
        for value in data:
            if isinstance(value,np.generic):
                if isinstance(value,np.ndarray):
                    value=[item.item() for item in value]
                else:
                    value=[value.item()]
            elif isinstance(value,dict):
                value=list(value.values())
            elif isinstance(value,Vector):
                value=[item for item in value._data]
            elif not isinstance(value,(list,tuple)):
                value=[value]
            data_list.extend(value)
            try:
                Vector(data_list)
            except TypeError:
                data_type=str(type(value))
                data_type=data_type[data_type.find("'")+1:data_type.rfind("'")]
                raise TypeError(f"Data type \"{data_type}\" not supported for atomic vectors") from None
            except Exception as excep:
                raise type(excep)(
                    f"""A fatal error ocurred.
                    Please report this in the issues page: https://github.com/Ricardo-Werner-Rivas/pyrcore/issues
                    
                    Include the following message, raised by the error, in your report:
                    \"{excep}\""""
                ) from None
        return Vector(data_list,names=names)