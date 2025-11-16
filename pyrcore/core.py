#* LEGEND
#! Missing
#* Section
#^ Important
#// Alternative or deprecated code

#* IMPORTS
import numpy as np
from typing import TypeVar,Generic,Any

#* MAIN CLASS
# Create vector class with Generic
class Vector(Generic[TypeVar("var")]):
    """
    Replicates R atomic vectors
    """
    #* BASIC METHODS
    # __init__
    #^ Provisional
    def __init__(self,data:Any=None,**attributes):
        #! MISSING CORRECT TYPE IMPLEMENTATION
        if isinstance(data,(int,float,str,dict,np.number,np.str_)):
            data=[data]
        elif isinstance(data,(list,np.ndarray)):
            pass
        elif data==None:
            data=[]
        else:
            data=list(data)
        if isinstance(data,np.ndarray):
            self._data=data
        else:
            self._data=np.array(data)
        if None in self._data:
            self._data=np.array([value for value in self._data[self._data!=None]])
        self._attributes=attributes or {}
        if self._data.dtype=="object":
            raise TypeError("Multi-type atomic vector not supported. For this purpose, use lists or tuples")
        self._type=self._data.dtype
    # View attribute
    def attr(self,attribute:str,value=None):
        if value is None:
            return self._attributes[attribute]
        else:
            self._attributes[attribute]=value
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
    # Getter
    def names(self):
        return self._attributes["names"] if "names" in self._attributes else None
    # Attributes
    @property
    # Getter
    def attributes(self):
        return self._attributes
    
    #* COMPARATIVE METHODS
    # Equality
    def __eq__(self,value):
        if isinstance(value,Vector):
            return self._data==value._data
        else:
            return self._data==value
    # Inequality
    def __ne__(self,value):
        if isinstance(value,Vector):
            return self._data!=value._data
        else:
            return self._data!=value
    # Less than
    def __lt__(self,value):
        if isinstance(value,Vector):
            return self._data<value._data
        else:
            return self._data,value
    # Less or equal
    def __le__(self,value):
        if isinstance(value,Vector):
            return self._data<=value._data
        else:
            return self._data<=value
    # Greater than
    def __gt__(self,value):
        if isinstance(value,Vector):
            return self._data>value._data
        else:
            return self._data>value
    # Greater or equal
    def __ge__(self,value):
        if isinstance(value,Vector):
            return self._data>=value._data
        else:
            return self._data>=value
    
    #* ARITHMETIC OPERATIONS
    # Addition
    def __add__(self,value):
        if isinstance(value,Vector):
            if isinstance(value._data[0],np.number) and isinstance(self._data[0],np.number):
                return Vector(self._data+value._data)
            elif isinstance(value._data[0],np.str_) and isinstance(self._data[0],np.str_):
                return Vector(self._data+value._data)
            else:
                raise TypeError("Addition only available for vectors and values of matching supported types")
        elif isinstance(value,(int,float,np.number)) and isinstance(self._data[0],np.number):
            return Vector(self._data+value)
        elif isinstance(value,str) and isinstance(self._data[0],np.str_):
            return Vector(self._data+value)
        else:
            raise TypeError("Addition only available for vectors and values of matching supported types")
    # Difference
    def __sub__(self,value):
        if isinstance(value,Vector):
            if isinstance(value._data[0],np.number) and isinstance(self._data[0],np.number):
                return Vector(self._data-value._data)
            else:
                raise TypeError("Difference not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and isinstance(self._data[0],np.number):
            return Vector(self._data-value)
        else:
            raise TypeError("Difference not supported for non-numerical values")
    # Product
    def __mul__(self,value):
        if isinstance(value,Vector):
            if isinstance(value._data[0],np.number) and isinstance(self._data[0],np.number):
                return Vector(self._data*value._data)
            else:
                raise TypeError("Multiplication not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and isinstance(self._data[0],np.number):
            return Vector(self._data*value)
        else:
            raise TypeError("Multiplication not supported for non-numerical values")
    # Fraction
    def __truediv__(self,value):
        if isinstance(value,Vector):
            if isinstance(value._data[0],np.number) and isinstance(self._data[0],np.number):
                return Vector(self._data/value._data)
            else:
                raise TypeError("Fraction not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and isinstance(self._data[0],np.number):
            return Vector(self._data/value)
        else:
            raise TypeError("Fraction not supported for non-numerical values")
    # Floor division (integer result)
    def __floordiv__(self,value):
        if isinstance(value,Vector):
            if isinstance(value._data[0],np.number) and isinstance(self._data[0],np.number):
                return Vector(self._data//value._data)
            else:
                raise TypeError("Integer division not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and isinstance(self._data[0],np.number):
            return Vector(self._data//value)
        else:
            raise TypeError("Integer division not supported for non-numerical values")
    # Module
    def __mod__(self,value):
        if isinstance(value,Vector):
            if isinstance(value._data[0],np.number) and isinstance(self._data[0],np.number):
                return Vector(self._data%value._data)
            else:
                raise TypeError("Module operation is not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and isinstance(self._data[0],np.number):
            return Vector(self._data%value)
        else:
            raise TypeError("Module operation is not supported for non-numerical values")
    # Divmod
    def __divmod__(self,value):
        return self//value,self%value
    # Power
    def __pow__(self,value):
        if isinstance(value,Vector):
            if isinstance(value._data[0],np.number) and isinstance(self._data[0],np.number):
                return Vector(self._data**value._data)
            else:
                raise TypeError("Power operation is not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and isinstance(self._data[0],np.number):
            return Vector(self._data**value)
        else:
            raise TypeError("Power operation is not supported for non-numerical values")
    
    #* REFLEXED ARITHMETIC OPERATIONS
    # Addition
    def __radd__(self,value):
        if isinstance(value,(int,float,np.number)) and isinstance(self._data[0],np.number):
            return Vector(value+self._data)
        elif isinstance(value,str) and isinstance(self._data[0],np.str_):
            return Vector(value+self._data)
        else:
            raise TypeError("Addition only available for vectors and values of matching supported types")
    # Difference
    def __rsub__(self,value):
        if isinstance(value,(int,float,np.number)) and isinstance(self._data[0],np.number):
            return Vector(value-self._data)
        else:
            raise TypeError("Difference not supported for non-numerical values")
    # Product
    def __rmul__(self,value):
        if isinstance(value,(int,float,np.number)) and isinstance(self._data[0],np.number):
            return Vector(value*self._data)
        else:
            raise TypeError("Multiplication not supported for non-numerical values")
    # Fraction
    def __rtruediv__(self,value):
        if isinstance(value,(int,float,np.number)) and isinstance(self._data[0],np.number):
            return Vector(value/self._data)
        else:
            raise TypeError("Fraction not supported for non-numerical values")
    # Integer division
    def __rfloordiv__(self,value):
        if isinstance(value,(int,float,np.number)) and isinstance(self._data[0],np.number):
            return Vector(value//self._data)
        else:
            raise TypeError("Integer division not supported for non-numerical values")
    # Module
    def __rmod__(self,value):
        if isinstance(value,(int,float,np.number)) and isinstance(self._data[0],np.number):
            return Vector(value%self._data)
        else:
            raise TypeError("Module operation is not supported for non-numerical values")
    # Divmod
    def __divmod__(self,value):
        return value//self,value%self
    # Power
    def __rpow__(self,value):
        if isinstance(value,(int,float,np.number)) and isinstance(self._data[0],np.number):
            return Vector(value**self._data)
        else:
            raise TypeError("Power operation is not supported for non-numerical values")
    
    #* UNARY METHODS
    # Negative
    def __neg__(self):
        if isinstance(self._data[0],np.number):
            return Vector(-self._data)
        else:
            raise TypeError(f"Negative unary method only available for numeric vectors, not {self.type} type vectors")
    # Positive
    def __pos__(self):
        if isinstance(self._data[0],np.number):
            return Vector(+self._data)
        else:
            raise TypeError(f"Positive unary method only available for numeric vectors, not {self.type} type vectors")
    # Absolute value
    def __abs__(self):
        if isinstance(self._data[0],np.number):
            return Vector(abs(self._data))
        else:
            raise TypeError(f"Absolute value unary method only available for numeric vectors, not {self.type} type vectors")
    
    #* INDEXATION
    # Getter
    def __getitem__(self,index):
        #! Missing name implemention as index (using <list>.index(<value>) method)
        return self._data[index]
    # Setter
    def __setitem__(self,index,value):
        if value==None:
            data=list(self._data)
            data.remove(self._data[index])
            self._data=np.array(data)
            #! Missing name removal from "names"
        else:
            self._data[index]=value
    #^ No deleter
    
    #* LENGTH
    # Length
    def __len__(self):
        return len(self._data)
    
    #* SCREEN
    # Representation
    def __repr__(self):
        return f"c({", ".join(str(value) for value in self._data)})"
        #! Missing names implementation
    # HTML representation
    def _repr_html_(self):
        return f"<p>c(<br>{",<br>".join(str(value) for value in self._data)}<br>)</p>"
        #! Missing names implementation
    # Printing (__str__ method)
    def __str__(self):
        if "names" in self.attributes:
            return f"{"\n".join([f"{name}: {str(value)}" for name,value in dict(zip(self.names,self._data)).items()])}"
        else:
            return f"{"\t".join(str(value) for value in self._data)}"