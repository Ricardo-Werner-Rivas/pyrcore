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
#¡ Inherited
#*===============================================================================================================================

#^ The different types of comments require the "Colorful Comments Refreshed" extension for VSCode to be properly distinguished

#* IMPORTS
# NumPy
import numpy as np
# TypeVar and Generic (typing)
from typing import TypeVar,Generic
# Class "Vector"
from .core import RObject

#* TYPING
# Define new variable types with TypeVar
VT=TypeVar("VectorDataTypes")

#* CLASS "Vector"
# Create vector class with Generic
class Vector(RObject,Generic[VT]):
    #& Missing code comments
    """
    Replicates R atomic vectors.\n
    This class can be imported for documentation purposes. For vector creation you'll want to use the combination function (`c()`).\n
    ---
    Attributes:
        data (`numpy.array`, Hidden): A *NumPy* array storing all the data in its native Python type (not forced to `numpy` types).
            Attribute `data` is not multi-type, exactly as R atomic vectors.
        attributes (`dict`, Hidden): Dictionary storing the R vector attribute `"names"` and metada introduced by the user.
        type (`str`, Hidden): String with the type of the elements of the vector.
    ---
    \n## Methods
        :attr: *`MethodType`*
        Gets or sets the value of an attribute
        :structure: *`MethodType`*
        Changes the dictionary of attributes and returns the object (`Vector`)
    ---
    \n## Properties
    1. **type**: *`MethodType`*
        * **Getter**: Gets the hidden attribute `type`.
        * **Setter**: Changes the type of the values in the vector.
        * **No deleter**.
    2. **names**: *`MethodType`*
        * **Getter**: Gets the names of the vector values.
        * **Setter**: Changes the names of the vector values. Receives an iterable with the new names.
        * **No deleter**.
    3. **attributes**: *`MethodType`*
        * **Getter**: Gets the hidden attribute `attributes`.
        * **No setter**.
        * **No deleter**.
    """
    #* METHODS
    # __init__
    def __init__(self,data:list,**attributes):
        """
        Arguments:
            data (`list`): Object containing the value/s for the vector.
                For vector creation, combination function (`c()`) is recommended.
            **attributes (`dict`, Optional): Stream of keyword arguments containing the attributes for the vector.
                Atomic vectors only support attribute "names" and metadata introduced by the user.
        """
        self._data=np.array(
            [
                value.item()
                if isinstance(value,np.generic)
                else value
                for value in data
            ]
        ) if isinstance(data,np.ndarray) else np.array(data)
        if None in self._data:
            self._data=np.array([value for value in self._data[self._data!=None]])
        self._attributes=attributes or {"names":None}
        if self._attributes["names"] and len(self._attributes["names"])!=len(self._data):
            raise IndexError("List of names has different length than the data.")
        if self._data.dtype=="object":
            raise TypeError("Multi-type atomic vector not supported. For this purpose, use lists or tuples")
        self._type=str(self._data.dtype)
        if "int" in self.type:
            self._type=int
        elif "float" in self.type:
            self._type=float
        elif isinstance(self._data[0],np.str_):
            self._type=str
        else:
            self._type=eval(self._type[self._type.find("'")+1:self._type.rfind("'")])
        self._data=np.array([value.item() for value in self._data],dtype=object)
    # Get/set attribute
    def attr(self,attribute:str,value=None):
        if value is None:
            return super().attr(attribute,value)
        elif attribute=="names" and len(value)!=len(self._data):
            raise ValueError("Number of names should be equal to number of values")
        else:
            self._attributes[attribute]=value
    # Update attributes
    def structure(self,atts:dict[str,]|None=None,**attributes):
        """
        Updates attributes dictionary. Similar to R `structure` function.
        Returns the `Vector` object.\n
        ---
        Arguments:
            atts (`dict[str|Any]`|`None`, Optional): Dictionary with the attributes changes.
            **attributes (Optional): Stream of attributes manually introduced.
        Both cannot be introduced at the same time.\n
        ---
        Returns:
            Vector: Returns the `Vector` instance with the updated attributes.
        """
        super().structure(atts,**attributes)
        if self._attributes["names"] and len(self._attributes["names"])!=len(self._data):
            raise IndexError("List of names has different length than the data.")
        return self
    
    #* PROPERTIES
    # Type
    #¡ Getter was inherited
    # Setter
    @RObject.type.setter
    def type(self,new_type:"type|str"):
        super().type=new_type
        self._data=np.array([self._type(value) for value in self._data],dtype=object)
    #^ No deleter
    
    # Names
    @property
    # Getter
    def names(self)->list[str]|None:
        return self._attributes["names"]
    # Setter
    @names.setter
    def names(self,names:"list[str]|tuple[str]|Vector[str]|None"):
        self._attributes["names"]=names
    #^ No deleter
    
    #¡ Inherited "attributes" property
    
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
            if value.type in [int,float] and self.type in [int,float]:
                return Vector(self._data+value._data,**self.attributes)
            elif value.type==str and self.type==str:
                return Vector(self._data+value._data,**self.attributes)
            else:
                raise TypeError("Addition only available for vectors and values of matching supported types")
        elif isinstance(value,(int,float,np.number)) and self.type in [int,float]:
            return Vector(self._data+value,**self.attributes)
        elif isinstance(value,(str,np.str_)) and self.type==str:
            return Vector(self._data+value,**self.attributes)
        else:
            raise TypeError("Addition only available for vectors and values of matching supported types")
    # Difference
    def __sub__(self,value):
        if isinstance(value,Vector):
            if value.type in [int,float] and self.type in [int,float]:
                return Vector(self._data-value._data,**self.attributes)
            else:
                raise TypeError("Difference not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and self.type in [int,float]:
            return Vector(self._data-value,**self.attributes)
        else:
            raise TypeError("Difference not supported for non-numerical values")
    # Product
    def __mul__(self,value):
        if isinstance(value,Vector):
            if value.type in [int,float] and self.type in [int,float]:
                return Vector(self._data*value._data,**self.attributes)
            else:
                raise TypeError("Multiplication not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and self.type in [int,float]:
            return Vector(self._data*value,**self.attributes)
        else:
            raise TypeError("Multiplication not supported for non-numerical values")
    # Fraction
    def __truediv__(self,value):
        if isinstance(value,Vector):
            if value.type in [int,float] and self.type in [int,float]:
                return Vector(self._data/value._data,**self.attributes)
            else:
                raise TypeError("Fraction not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and self.type in [int,float]:
            return Vector(self._data/value,**self.attributes)
        else:
            raise TypeError("Fraction not supported for non-numerical values")
    # Floor division (integer result)
    def __floordiv__(self,value):
        if isinstance(value,Vector):
            if value.type in [int,float] and self.type in [int,float]:
                return Vector(self._data//value._data,**self.attributes)
            else:
                raise TypeError("Integer division not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and self.type in [int,float]:
            return Vector(self._data//value,**self.attributes)
        else:
            raise TypeError("Integer division not supported for non-numerical values")
    # Module
    def __mod__(self,value):
        if isinstance(value,Vector):
            if value.type in [int,float] and self.type in [int,float]:
                return Vector(self._data%value._data,**self.attributes)
            else:
                raise TypeError("Module operation is not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and self.type in [int,float]:
            return Vector(self._data%value,**self.attributes)
        else:
            raise TypeError("Module operation is not supported for non-numerical values")
    # Divmod
    def __divmod__(self,value):
        return self//value,self%value
    # Power
    def __pow__(self,value):
        if isinstance(value,Vector):
            if value.type in [int,float] and self.type in [int,float]:
                return Vector(self._data**value._data,**self.attributes)
            else:
                raise TypeError("Power operation is not supported for non-numerical values")
        elif isinstance(value,(int,float,np.number)) and self.type in [int,float]:
            return Vector(self._data**value,**self.attributes)
        else:
            raise TypeError("Power operation is not supported for non-numerical values")
    
    #* REFLEXED ARITHMETIC OPERATIONS
    # Addition
    def __radd__(self,value):
        return self+value
    # Difference
    def __rsub__(self,value):
        return (self-value)*-1
    # Product
    def __rmul__(self,value):
        return self*value
    # Fraction
    def __rtruediv__(self,value):
        return self/value**-1
    # Integer division
    def __rfloordiv__(self,value):
        return self//value**-1
    # Module
    def __rmod__(self,value):
        if isinstance(value,(int,float,np.number)) and self.type in [int,float]:
            return Vector(value%self._data,**self.attributes)
        else:
            raise TypeError("Module operation is not supported for non-numerical values")
    # Divmod
    def __rdivmod__(self,value):
        return value//self,value%self
    # Power
    def __rpow__(self,value):
        if isinstance(value,(int,float,np.number)) and self.type in [int,float]:
            return Vector(value**self._data,**self.attributes)
        else:
            raise TypeError("Power operation is not supported for non-numerical values")
    
    #* UNARY METHODS
    # Negative
    def __neg__(self):
        if self.type in [int,float]:
            return Vector(-self._data,**self.attributes)
        else:
            raise TypeError(f"Negative unary method only available for numeric vectors, not {self.type} type vectors")
    # Positive
    def __pos__(self):
        if self.type in [int,float]:
            return Vector(+self._data,**self.attributes)
        else:
            raise TypeError(f"Positive unary method only available for numeric vectors, not {self.type} type vectors")
    # Absolute value
    def __abs__(self):
        if self.type in [int,float]:
            return Vector(abs(self._data),**self.attributes)
        else:
            raise TypeError(f"Absolute value unary method only available for numeric vectors, not {self.type} type vectors")
    
    #* INDEXATION
    # Getter
    def __getitem__(self,index):
        if self.names and isinstance(index,str):
            if index in self.names:
                return self._data[self.names.index(index)]
            else:
                raise IndexError(f"Index \"{index}\" not in vector")
        else:
            return self._data[index]
    # Setter
    def __setitem__(self,index,value):
        if self.names and isinstance(index,str):
            if index in self.names:
                if value==None:
                    data=list(self._data)
                    data.remove(data[self.names.index(index)])
                    self._data=np.array(data)
                    self.names.remove(index)
                else:
                    self._data[self.names.index(index)]=value
            else:
                raise IndexError(f"Index \"{index}\" not in vector")
        elif value==None:
            data=list(self._data)
            data.remove(data[data.index(self._data[index],index)])
            try:
                self._data=np.array([eval(self.type)(value) for value in data],dtype=object)
            except:
                raise TypeError("New elements must respect de vectors typing")
            if self.names:
                self.names.remove(self.names[index])
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
        if self.names:
            return f"c({", ".join(f"{name}={str(value)}" for name,value in dict(zip(self.names,self._data)).items())})"
        else:
            return f"c({", ".join(str(value) for value in self._data)})"
    # HTML representation
    def _repr_html_(self):
        if self.names:
            headers=[f"<th>{name}</th>" for name in self.names]
            values=[f"<td style=\"text-align: center;\">{value}</td>" for value in self._data]
            return f"""
            <table>
                <thead>
                    <tr>
                        {"\n".join(headers)}
                    </tr>
                </thead>
                <tr>
                    {"\n".join(values)}
                </tr>
            </table>
            """
        else:
            return f"<p>{"&emsp;·&emsp;".join(str(value) for value in self._data)}</p>"
    # Printing (__str__ method)
    def __str__(self):
        if self.names:
            return f"{"\n".join(f"{name}: {str(value)}" for name,value in dict(zip(self.names,self._data)).items())}"
        else:
            return f"{"\t".join(str(value) for value in self._data)}"