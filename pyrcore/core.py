# Imports
import numpy as np
from typing import TypeVar,Generic
# Create vector class with Generic
class Vector(Generic[TypeVar("var")]):
    """
    Replicates R atomic vectors (c())
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
    # View attribute
    def attr(self,attribute:str,value=None):
        if value is None:
            return self._attributes[attribute]
        else:
            self._attributes[attribute]=value
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
    # Getter
    def type(self):
        return self._type
    # Names
    @property
    def names(self):
        return self._names
    
    #* ARITHMETIC OPERATIONS
    # Addition
    def __add__(self,value):
        if isinstance(value,Vector):
            if value.type in "int64 float64".split() and self.type in "int64 float64".split():
                return Vector(self._data+value._data)
            elif str(value.type)[:2]=="<U" and str(self.type)[:2]=="<U":
                return Vector(self._data+value._data)
            else:
                raise TypeError("Addition only available for vectors and values of matching supported types")
        elif isinstance(value,(int,float,np.number)) and self.type in "int64 float64".split():
            return Vector(self._data+value)
        elif isinstance(value,str) and str(self.type)[:2]=="<U":
            return Vector(self._data+value)
        else:
            raise TypeError("Addition only available for vectors and values of matching supported types")
    # Substraction
    def __sub__(self,value):
        if isinstance(value,Vector):
            if value.type in "int64 float64".split() and self.type in "int64 float64".split():
                return Vector(self._data-value._data)
            else:
                raise TypeError("Substraction not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and self.type in "int64 float64".split():
            return Vector(self._data-value)
        else:
            raise TypeError("Substraction not supported for non-numerical values")
    # Product
    def __mul__(self,value):
        if isinstance(value,Vector):
            if value.type in "int64 float64".split() and self.type in "int64 float64".split():
                return Vector(self._data*value._data)
            else:
                raise TypeError("Multiplication not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and self.type in "int64 float64".split():
            return Vector(self._data*value)
        else:
            raise TypeError("Multiplication not supported for non-numerical values")
    # Fraction
    def __truediv__(self,value):
        if isinstance(value,Vector):
            if value.type in "int64 float64".split() and self.type in "int64 float64".split():
                return Vector(self._data/value._data)
            else:
                raise TypeError("Fraction not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and self.type in "int64 float64".split():
            return Vector(self._data/value)
        else:
            raise TypeError("Fraction not supported for non-numerical values")
    # Floor division (integer result)
    def __floordiv__(self,value):
        if isinstance(value,Vector):
            if value.type in "int64 float64".split() and self.type in "int64 float64".split():
                return Vector(self._data//value._data)
            else:
                raise TypeError("Integer division not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and self.type in "int64 float64".split():
            return Vector(self._data//value)
        else:
            raise TypeError("Integer division not supported for non-numerical values")
    # Module
    def __mod__(self,value):
        if isinstance(value,Vector):
            if value.type in "int64 float64".split() and self.type in "int64 float64".split():
                return Vector(self._data%value._data)
            else:
                raise TypeError("Module operation is not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and self.type in "int64 float64".split():
            return Vector(self._data%value)
        else:
            raise TypeError("Module operation is not supported for non-numerical values")
    # Power
    def __pow__(self,value):
        if isinstance(value,Vector):
            if value.type in "int64 float64".split() and self.type in "int64 float64".split():
                return Vector(self._data**value._data)
            else:
                raise TypeError("Power operation is not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and self.type in "int64 float64".split():
            return Vector(self._data**value)
        else:
            raise TypeError("Power operation is not supported for non-numerical values")
    
    #* REFLEXED ARITHMETIC OPERATIONS
    # Addition
    def __radd__(self,value):
        if isinstance(value,(int,float,np.number)) and self.type in "int64 float64".split():
            return Vector(value+self._data)
        elif isinstance(value,str) and str(self.type)[:2]=="<U":
            return Vector(value+self._data)
        else:
            raise TypeError("Addition only available for vectors and values of matching supported types")
    # Substraction
    def __rsub__(self,value):
        if isinstance(value,(int,float,np.number)) and self.type in "int64 float64".split():
            return Vector(value-self._data)
        else:
            raise TypeError("Substraction not supported for non-numerical values")
    # Product
    def __rmul__(self,value):
        if isinstance(value,(int,float,np.number)) and self.type in "int64 float64".split():
            return Vector(value*self._data)
        else:
            raise TypeError("Multiplication not supported for non-numerical values")
    # Fraction
    def __rtruediv__(self,value):
        if isinstance(value,(int,float,np.number)) and self.type in "int64 float64".split():
            return Vector(value/self._data)
        else:
            raise TypeError("Fraction not supported for non-numerical values")
    # Integer division
    def __rfloordiv__(self,value):
        if isinstance(value,(int,float,np.number)) and self.type in "int64 float64".split():
            return Vector(value//self._data)
        else:
            raise TypeError("Integer division not supported for non-numerical values")
    # Module
    def __rmod__(self,value):
        if isinstance(value,(int,float,np.number)) and self.type in "int64 float64".split():
            return Vector(value%self._data)
        else:
            raise TypeError("Module operation is not supported for non-numerical values")
    # Power
    def __rpow__(self,value):
        if isinstance(value,(int,float,np.number)) and self.type in "int64 float64".split():
            return Vector(value**self._data)
        else:
            raise TypeError("Power operation is not supported for non-numerical values")
    
    #* UNARY METHODS
    # Negative
    def __neg__(self):
        if self.type in "int64 float64":
            return Vector(-self._data)
        else:
            raise TypeError(f"Negative unary method only available for numeric vectors, not {self.type} type vectors")
    # Positive
    def __pos__(self):
        if self.type in "int64 float64":
            return Vector(+self._data)
        else:
            raise TypeError(f"Positive unary method only available for numeric vectors, not {self.type} type vectors")
    # Absolute value
    def __abs__(self):
        if self.type in "int64 float64":
            return Vector(abs(self._data))
        else:
            raise TypeError(f"Absolute value unary method only available for numeric vectors, not {self.type} type vectors")
    
    #* INDEXATION
    # Getter
    def __getitem__(self,index):
        try:
            return self._data[index]
        except IndexError:
            raise IndexError("Object is 0-dimensional. 0 indexes supported, but 1 were given")
    # Setter
    def __setitem__(self,index,value):
        try:
            self._data[index]=value
        except IndexError:
            raise IndexError("Object is 0-dimensional. 0 indexes supported, but 1 were given")
    
    #* LENGTH
    # Length
    def __len__(self):
        return len(self._data)
    
    #* SCREEN
    # Representation
    def __repr__(self):
        return f"c({", ".join(str(value) for value in self._data)})"
    # Printing (__str__ method)
    def __str__(self):
        return f"{"\t".join(str(value) for value in self._data)}"