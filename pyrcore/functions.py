#*==============================================================================================================================
#* LEGEND
#*------------------------------------------------------------------------------------------------------------------------------
#! Missing
#& Missing unimportant
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
def c(*data:list,numpy:bool=False,**named_data:dict[str,])->Vector:
    #& Missing comments for code
    #^ REVISE TRANSFORMATION PROCESS TO AVOID DOUBLE APPLICATION
    """
    Creates an atomic vector like in R. The returned object if a `Vector` instance.\n
    ---
    Arguments:
        *data (`list`): Stream of unnamed values for the vector.
        numpy (`bool`, Optional): Tells wether if values in the vector are to be set to native Python types (`False`) or to *NumPy* types (`True`).
                Set to `False` (**Python** types) by default.
        **named_data (`dict[str,Any]`): Stream of named values for the vector. They are passed as keyword arguments.
    ---
    Returns:
        Vector: Atomic vector "R-like".
    """
    # Raise error if both named and unnamed data are given
    if data and named_data:
        raise ValueError("Vector cannot store both named and unnamed data")
    # Return empty vector if no data was introduced
    elif not data and not named_data:
        return Vector()
    # In the rest of cases (*data or **named_data)
    else:
        # Store the names
        names=list(named_data.keys()) if named_data else None # If no names, then store None
        # Prepare the passed data
        data=data or list(named_data.values())
        # Empty list to store the data
        data_list=[]
        # Prepare the data to vectorize it
        for value in data:
            # If data is to be set to Python native types and it is in NumPy types
            if isinstance(value,np.generic) and not numpy:
                # If value is an array
                if isinstance(value,np.ndarray):
                    # List its values in Python native types
                    value=[item.item() for item in value]
                # Else
                else:
                    # Put its Python equivalent in a list
                    value=[value.item()]
            # Else, if value is a dictionary
            elif isinstance(value,dict):
                # Take its values
                value=list(value.values())
            # Else, 
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
                    \"{excep}\"
                    \nThank you for your help."""
                ) from None
        return Vector(data_list,names=names,numpy=numpy)