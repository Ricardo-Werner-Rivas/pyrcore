# Imports
import numpy as np
from typing import TypeVar,Generic
# Create vector class with Generic
class Vector(Generic[TypeVar("var")]):
    """
    Replicates R vectors (c())
    
    ---
    Attributes:
        
    """
    #* BASIC METHODS
    # __init__
    def __init__(self,data,**attributes):
        if isinstance(data,dict):
            self._names,data=tuple(data.keys()),list(data.values())
        else:
            self._names=None
        self._data=np.array(data)
        self._attributes=attributes or {}
        self._type=self._data.dtype
        return
    # View attribute
    def attr(self,attribute:str,value=None):
        if value is None:
            return self._attributes[attribute]
        else:
            self._attributes[attribute]=value
        return
    # Show attributes dictionary
    def attributes(self):
        return self._attributes
    # Updating attributes
    def structure(self,**attributes):
        self._attributes.update(attributes)
        return self
    
    #* PROPERTIES
    # Type
    @property
    def type(self):
        return self._type
    
    #* ARITHMETHIC OPERATIONS
    # Addition
    def __add__(self,value):
        if self.type in "int64 float64".split():
            if isinstance(value,Vector):
                if value.type in "int64 float64".split():
                    return Vector(self._data+value._data)
                else:
                    raise TypeError("Arithmethic operations only available for numeric vectors and values")
            else:
                if isinstance(value,(int,float,np.number)):
                    return Vector(self._data+value)
                else:
                    raise TypeError("Arithmethic operations only available for numeric vectors and values")
        else:
            raise TypeError("Arithmethic operations only available for numeric vectors and values")
    # Substraction
    def __sub__(self,value):
        if self.type in "int64 float64".split():
            if isinstance(value,Vector):
                if value.type in "int64 float64".split():
                    return Vector(self._data-value._data)
                else:
                    raise TypeError("Arithmethic operations only available for numeric vectors and values")
            else:
                if isinstance(value,(int,float,np.number)):
                    return Vector(self._data-value)
                else:
                    raise TypeError("Arithmethic operations only available for numeric vectors and values")
        else:
            raise TypeError("Arithmethic operations only available for numeric vectors and values")
    # Product
    def __mul__(self,value):
        if self.type in "int64 float64".split():
            if isinstance(value,Vector):
                if value.type in "int64 float64".split():
                    return Vector(self._data*value._data)
                else:
                    raise TypeError("Arithmethic operations only available for numeric vectors and values")
            else:
                if isinstance(value,(int,float,np.number)):
                    return Vector(self._data*value)
                else:
                    raise TypeError("Arithmethic operations only available for numeric vectors and values")
        else:
            raise TypeError("Arithmethic operations only available for numeric vectors and values")
    # Division
    def __truediv__(self,value):
        if self.type in "int64 float64".split():
            if isinstance(value,Vector):
                if value.type in "int64 float64".split():
                    return Vector(self._data/value._data)
                else:
                    raise TypeError("Arithmethic operations only available for numeric vectors and values")
            else:
                if isinstance(value,(int,float,np.number)):
                    return Vector(self._data/value)
                else:
                    raise TypeError("Arithmethic operations only available for numeric vectors and values")
        else:
            raise TypeError("Arithmethic operations only available for numeric vectors and values")
    
    #* INDEXATION
    # Getter
    def __getitem__(self,index):
        return self._data[index]
    # Setter
    def __setitem__(self,index,value):
        self._data[index]=value
        return
    
    #* LENGTH
    # Length
    def __len__(self):
        return len(self._data)
    
    #* SCREEN
    # Representation
    def __repr__(self):
        return f"c({", ".join(value for value in self._data)})"