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
# TypeVar, Generic and Iterable
from typing import TypeVar,Generic,Iterable
# Class RObject
from .core import RObject,Vector
# Combination function
from .functions import c

#* TYPING
# Define new variable types with TypeVar
MT=TypeVar("MatrixDataTypes") # For matrixes

#* CLASS "matrix"
class matrix(RObject,Generic[MT]):
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
        data:Vector[int|float]|Iterable|None=None,nrow:int|None=None,ncol:int|None=None,byrow:bool=False,
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
            elif data.type==bool:
                data=c(data,[False for i in range(nrow*ncol-len(data))])
            else:
                data=c(data,[None for i in range(nrow*ncol-len(data))])
        elif len(data)>nrow*ncol:
            data=data[:nrow*ncol]
        
        data_type=data._type
        data=data._data.reshape((nrow,ncol),order="C" if byrow else "F")
        super().__init__(data,**attributes)
        self._type=data_type
        self._attributes["dim"]=(nrow,ncol)
        if dimnames:
            self._attributes["dimnames"]=(
                list(dimnames[0]) if dimnames[0] else None,
                list(dimnames[1]) if dimnames[1] else None
            )
        else:
            self._attributes.setdefault("dimnames",(None,None))
    
    # Get/set attribute
    def attr(self,attribute:str,value=None):
        if value is None:
            super().attr(attribute,value)
        elif attribute=="dimnames" and any((len(value[0])>self.nrow,len(value[1])>self.ncol)):
            raise ValueError(f"{"Row" if len(value[0])>self.nrow else "Column"} names iterable can't be larger than {"row" if len(value[0])>self.nrow else "column"}'s length")
        else:
            self._attributes[attribute]=value
    
    # Structure
    def structure(self,atts:dict[str,]|None=None,**attributes):
        super().structure(atts,**attributes)
        if len(self.attributes["dimnames"][0])>self.nrow or len(self.attributes["dimnames"][1])>self.ncol:
            raise IndexError(f"{"Row" if len(self.attributes["dimnames"][0])>self.nrow else "Column"} names iterable can't be larger than {"row" if len(self.attributes["dimnames"][0])>self.nrow else "column"}'s length")
    
    #* PROPERTIES
    # Number of rows
    @property
    # Getter
    def nrow(self)->int:
        return self.attributes["dim"][0]
    #^ No setter
    #^ No deleter
    
    # Number of columns
    @property
    # Getter
    def ncol(self)->int:
        return self.attributes["dim"][1]
    #^ No setter
    #^ No deleter
    
    # Dimensions
    @property
    # Getter
    def dim(self)->tuple[int,int]:
        return self.attributes["dim"]
    #^ No setter
    #^ No deleter
    
    # Names of rows and columns (dimnames)
    @property
    # Getter
    def dimnames(self)->tuple[Iterable[str],Iterable[str]]:
        return self.attributes["dimnames"]
    #^ No setter
    #^ No deleter
    
    # Names of rows
    @property
    # Getter
    def rownames(self)->Vector[str]:
        return c(self.dimnames[0])
    # Setter
    @rownames.setter
    def rownames(self,names:Iterable[str]|None):
        self._attributes["dimnames"][0]=names
    #^ No deleter
    
    # Names of columns
    @property
    # Getter
    def colnames(self)->Vector[str]:
        return c(self._attributes["dimnames"][1])
    # Setter
    @colnames.setter
    def colnames(self,names:Iterable[str]|None):
        self._attributes["dimnames"][1]=names
    #^ No deleter
    
    #¡ Inherited "attributes" property
    
    # Type
    #¡ Getter was inherited
    # Setter
    @RObject.type.setter
    def type(self,new_type:"type|str"):
        super().type=new_type
        self._data=np.array([self._type(value) for value in self._data.ravel()]).reshape(self.nrow,self.ncol)
    #^ No deleter
    
    #* COMPARATIVE DUNDER METHODS
    # Equality
    def __eq__(self,value):
        return self._data==value._data if isinstance(value,matrix) else self._data==value
    
    # Inequality
    def __ne__(self,value):
        return self._data!=value._data if isinstance(value,matrix) else self._data!=value
    
    # Less than
    def __lt__(self,value):
        return self._data<value._data if isinstance(value,matrix) else self._data<value
    
    # Less or equal
    def __le__(self,value):
        return self._data<=value._data if isinstance(value,matrix) else self._data<=value
    
    # Greater than
    def __gt__(self,value):
        return self._data>value._data if isinstance(value,matrix) else self._data>value
    
    # Greater or equal
    def __ge__(self,value):
        return self._data>=value._data if isinstance(value,matrix) else self._data>=value
    
    #* ARITHMETIC OPERATIONS DUNDER METHODS
    # Addition
    def __add__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix(c((self._data+value._data).flatten()),self.nrow,self.ncol,True,attributes=self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(c(self._data.flatten()+value._data),self.nrow,self.ncol,True,attributes=self.attributes)
            else:
                result=self._data.copy()
                pos=0
                end=False
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        try:
                            result[i,j]+=value[pos]
                        except IndexError:
                            end=True
                            break
                        pos+=1
                    if end:
                        break
                return matrix(c(result.flatten()),self.nrow,self.ncol,True,attributes=self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(c(self._data.flatten()+value),self.nrow,self.ncol,True,attributes=self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Difference
    def __sub__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix(c((self._data-value._data).flatten()),self.nrow,self.ncol,True,attributes=self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(c(self._data.flatten()-value._data),self.nrow,self.ncol,True,attributes=self.attributes)
            else:
                result=self._data.copy()
                pos=0
                end=False
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        try:
                            result[i,j]-=value[pos]
                        except IndexError:
                            end=True
                            break
                        pos+=1
                    if end:
                        break
                return matrix(c(result.flatten()),self.nrow,self.ncol,True,attributes=self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(c(self._data.flatten()-value),self.nrow,self.ncol,True,attributes=self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Product
    def __mul__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix(c((self._data*value._data).flatten()),self.nrow,self.ncol,True,attributes=self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(c(self._data.flatten()*value._data),self.nrow,self.ncol,True,attributes=self.attributes)
            else:
                result=self._data.copy()
                pos=0
                end=False
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        try:
                            result[i,j]*=value[pos]
                        except IndexError:
                            end=True
                            break
                        pos+=1
                    if end:
                        break
                return matrix(c(result.flatten()),self.nrow,self.ncol,True,attributes=self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(c(self._data.flatten()*value),self.nrow,self.ncol,True,attributes=self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Division
    def __truediv__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix(c((self._data/value._data).flatten()),self.nrow,self.ncol,attributes=self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(c(self._data.flatten()/value._data),self.nrow,self.ncol,attributes=self.attributes)
            else:
                result=self._data.copy()
                pos=0
                end=False
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        try:
                            result[i,j]/=value[pos]
                        except IndexError:
                            end=True
                            break
                        pos+=1
                    if end:
                        break
                return matrix(c(result.flatten()),self.nrow,self.ncol,True,attributes=self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(c(self._data.flatten()/value),self.nrow,self.ncol,True,attributes=self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Integer division (floor division)
    def __floordiv__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix(c((self._data//value._data).flatten()),self.nrow,self.ncol,True,attributes=self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(c(self._data.flatten()//value._data),self.nrow,self.ncol,True,attributes=self.attributes)
            else:
                result=self._data.copy()
                pos=0
                end=False
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        try:
                            result[i,j]//=value[pos]
                        except IndexError:
                            end=True
                            break
                        pos+=1
                    if end:
                        break
                return matrix(c(result.flatten()),self.nrow,self.ncol,True,attributes=self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(c(self._data.flatten()//value),self.nrow,self.ncol,True,attributes=self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Module
    def __mod__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix(c((self._data%value._data).flatten()),self.nrow,self.ncol,True,attributes=self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(c(self._data.flatten()%value._data),self.nrow,self.ncol,True,attributes=self.attributes)
            else:
                result=self._data.copy()
                pos=0
                end=False
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        try:
                            result[i,j]%=value[pos]
                        except IndexError:
                            end=True
                            break
                        pos+=1
                    if end:
                        break
                return matrix(c(result.flatten()),self.nrow,self.ncol,True,attributes=self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(c(self._data.flatten()%value),self.nrow,self.ncol,True,attributes=self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Divmod
    def __divmod__(self,value):
        return self//value,self%value
    
    # Power
    #! Missing