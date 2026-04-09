#*===============================================================================================================================
#* LEGEND
#*-------------------------------------------------------------------------------------------------------------------------------
#! Missing
#& Missing unimportant
#~ Revision notes
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
# TypeVar, Generic, Iterable and TYPE_CHECKING
from typing import TypeVar,Generic,Iterable,TYPE_CHECKING
# Class RObject
from .core import RObject,Vector
# Combination function
from .functions import c

#* TYPING
# Import pandas.Series only for annotations
if TYPE_CHECKING:
    from pandas import Series
# Define new variable types with TypeVar
MT=TypeVar("MatrixDataTypes",int,float,str) # For matrixes
TS=TypeVar("TimeSeriesDataTypes") # For time-series

#* CLASS "matrix"
class matrix(RObject,Generic[MT]):
    #^ Revise "attr()" and "structure()" methods and "attributes" property
    #& Missing code comments
    """
    Replicates R matrixes and R `matrix()` function.\n
    Unlike class `Vector`, this class properly creates the object so no auxiliar functions are needed.\n
    ---
    Attributes:
        data (`numpy.array`, Hidden): Hidden attribute containing the data of the matrix in the form of a `numpy` array.
        attributes (`dict`, Hidden): Hidden attribute containing the R like attributes of the matrix.
    ---
    ## Methods
    
    ---
    ## Properties\n
    :nrow: *`MethodType`*\n
        Gets the number of rows\n
    :ncol: *`MethodType`*\n
        Gets the number of columns
    :dim: *`MethodType`*\n
        Gets the dimensions of the matrix\n
    :dimnames: *`MethodType`*\n
        Gets the names of rows and columns\n
    :rownames: *`MethodType`*\n
        Gets/sets the names of the rows\n
    :colnames: *`MethodType`*\n
        Gets/sets the names of the columns\n
    :attributes: *`MethodType`*\n
        Gets/sets the R like attributes of the matrix
    :type: *`MethodType`*\n
        Gets/sets the type of the data
    """
    #* METHODS
    # __init__
    def __init__(
        self,
        data:Vector[MT]|Iterable[MT]|None=None,nrow:int|None=None,ncol:int|None=None,byrow:bool=False,
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
                m=matrix(<data>,<nrow>,2,dimnames=(None,["name1","name2"]))
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
        #~ Attributes' updating validation
        if value is None:
            return super().attr(attribute,value)
        elif attribute=="dimnames" and any((len(value[0])>self.nrow,len(value[1])>self.ncol)):
            raise ValueError(f"{"Row" if len(value[0])>self.nrow else "Column"} names iterable can't be larger than {"row" if len(value[0])>self.nrow else "column"}'s length")
        else:
            self._attributes[attribute]=value
    
    # Structure
    def structure(self,**attributes)->matrix:
        #~ Attributes' updating validation
        if all([len(attributes["dimnames"][0])!=self.nrow,attributes["dimnames"][0] is not None]) or all([len(attributes["dimnames"][1])!=self.ncol,attributes["dimnames"][1] is not None]):
            raise IndexError(f"{"Row" if len(attributes["dimnames"][0])>self.nrow else "Column"} names iterable can't be larger than {"row" if len(attributes["dimnames"][0])>self.nrow else "column"}'s length")
        return super().structure(**attributes)
    
    # Determinant
    def det(self):
        """
        Calculates the determinant of the matrix.\n
        ---
        Returns:
            int: Determinant of the matrix
        """
        if self.nrow!=self.ncol:
            raise ValueError("Matrix is not square")
        elif self.nrow==1:
            return int(self._data)
        elif self.nrow==2:
            return self._data[0,0]*self._data[1,1]-self._data[0,1]*self._data[1,0]
        elif self.nrow==3:
            return self._data[0,0]*self._data[1,1]*self._data[2,2]+self._data[1,0]*self._data[2,1]*self._data[0,2]+self._data[0,1]*self._data[1,2]*self._data[2,0]-(self._data[0,2]*self._data[1,1]*self._data[2,0]+self._data[1,2]*self._data[2,1]*self._data[0,0]+self._data[0,1]*self._data[1,0]*self._data[2,2])
        else:
            return sum([self._data[0,i]*((-1)**(1+i+1))*matrix(np.delete(self._data,i,1)[1:].flatten(),self.nrow-1,self.ncol-1,True,**self.attributes).det() for i in range(self.ncol)])
    
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
        if "dimnames" not in self.attributes:
            return (None,None)
        return self.attributes["dimnames"]
    #^ No setter
    #^ No deleter
    
    # Names of rows
    @property
    # Getter
    def rownames(self)->Vector[str]:
        return c(self.dimnames[0]) if self.dimnames[0] is not None else None
    # Setter
    @rownames.setter
    def rownames(self,names:Iterable[str]|None):
        self._attributes["dimnames"][0]=names
    #^ No deleter
    
    # Names of columns
    @property
    # Getter
    def colnames(self)->Vector[str]:
        return c(self.dimnames[1]) if self.dimnames[1] is not None else None
    # Setter
    @colnames.setter
    def colnames(self,names:Iterable[str]|None):
        self._attributes["dimnames"][1]=names
    #^ No deleter
    
    #¡ "attributes" property redefinition
    @RObject.attributes.getter
    def attributes(self):
        #~ "attributes" property usage
        if "dimnames" in self._attributes and self._attributes["dimnames"]==(None,None):
            del self._attributes["dimnames"]
        return super().attributes
    
    # Type
    #¡ Getter
    # Setter
    @RObject.type.setter
    def type(self,new_type:"type|str"):
        super(matrix,type(self)).type.__set__(self,new_type)
        self._data=np.array([self._type(value) for value in self._data.ravel()],dtype=object).reshape(self.nrow,self.ncol)
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
    
    #* ARITHMETIC DUNDER METHODS
    # Addition
    def __add__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix(c((self._data+value._data).flatten()),self.nrow,self.ncol,True,**self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(c(self._data.flatten()+value._data),self.nrow,self.ncol,True,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]+=value[pos]
                        pos+=1
                return matrix(c(result.flatten()),self.nrow,self.ncol,True,**self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(c(self._data.flatten()+value),self.nrow,self.ncol,True,**self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Difference
    def __sub__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix(c((self._data-value._data).flatten()),self.nrow,self.ncol,True,**self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(c(self._data.flatten()-value._data),self.nrow,self.ncol,True,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]-=value[pos]
                        pos+=1
                return matrix(c(result.flatten()),self.nrow,self.ncol,True,**self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(c(self._data.flatten()-value),self.nrow,self.ncol,True,**self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Product
    def __mul__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix(c((self._data*value._data).flatten()),self.nrow,self.ncol,True,**self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(c(self._data.flatten()*value._data),self.nrow,self.ncol,True,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]*=value[pos]
                        pos+=1
                return matrix(c(result.flatten()),self.nrow,self.ncol,True,**self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(c(self._data.flatten()*value),self.nrow,self.ncol,True,**self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Division
    def __truediv__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix(c((self._data/value._data).flatten()),self.nrow,self.ncol,**self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(c(self._data.flatten()/value._data),self.nrow,self.ncol,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]/=value[pos]
                        pos+=1
                return matrix(c(result.flatten()),self.nrow,self.ncol,True,**self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(c(self._data.flatten()/value),self.nrow,self.ncol,True,**self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Integer division (floor division)
    def __floordiv__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix(c((self._data//value._data).flatten()),self.nrow,self.ncol,True,**self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(c(self._data.flatten()//value._data),self.nrow,self.ncol,True,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]//=value[pos]
                        pos+=1
                return matrix(c(result.flatten()),self.nrow,self.ncol,True,**self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(c(self._data.flatten()//value),self.nrow,self.ncol,True,**self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Module
    def __mod__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix(c((self._data%value._data).flatten()),self.nrow,self.ncol,True,**self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(c(self._data.flatten()%value._data),self.nrow,self.ncol,True,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]%=value[pos]
                        pos+=1
                return matrix(c(result.flatten()),self.nrow,self.ncol,True,**self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(c(self._data.flatten()%value),self.nrow,self.ncol,True,**self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Divmod
    def __divmod__(self,value):
        return self//value,self%value
    
    # Power
    def __pow__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix(c((self._data**value._data).flatten()),self.nrow,self.ncol,True,**self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(c(self._data.flatten()**value._data),self.nrow,self.ncol,True,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]**=value[pos]
                        pos+=1
                return matrix(c(result.flatten()),self.nrow,self.ncol,True,**self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(c(self._data.flatten()**value),self.nrow,self.ncol,True,**self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Matrix product
    def __matmul__(self,value:"matrix|Vector|np.ndarray"):
        if isinstance(value,(matrix,Vector)):
            if self.ncol==value.nrow:
                return matrix(c((self._data@value._data).flatten()),self.nrow,value.ncol,True,**self.attributes)
            else:
                raise ArithmeticError("Dimension conditions for matrix product are not met")
        elif isinstance(value,np.ndarray):
            if self.ncol==value.shape[0]:
                return matrix(c((self._data@value).flatten()),self.nrow,value.shape[1],True,**self.attributes)
            else:
                raise ArithmeticError("Dimension conditions for matrix product are not met")
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} cannot be matricially multiplied")
    
    #* REFLEXED ARITHMETIC DUNDER METHODS
    # Addition
    def __radd__(self,value):
        return self+value
    
    # Difference
    def __rsub__(self,value):
        return (self-value)*-1
    
    # Product
    def __rmul__(self,value):
        return self*value
    
    # Division
    def __rtruediv__(self,value):
        return (self/value)**-1
    
    # Integer division (floor division)
    def __rfloordiv__(self,value):
        return (self//value)**-1
    
    # Module
    def __rmod__(self,value):
        if isinstance(value,(int,float)):
            return matrix(c(value%self._data.flatten()),self.nrow,self.ncol,True,**self.attributes)
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(c(value._data%self._data.flatten()),self.nrow,self.ncol,True,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]=value[pos]%result[i,j]
                        pos+=1
                return matrix(c(result.flatten()),self.nrow,self.ncol,True,**self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Divmod
    def __rdivmod__(self,value):
        return value//self,value%self
    
    # Power
    def __rpow__(self,value):
        if isinstance(value,(int,float)):
            return matrix(c(value**self._data.flatten()),self.nrow,self.ncol,True,**self.attributes)
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(c(value._data**self._data.flatten()),self.nrow,self.ncol,True,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]=value[pos]**result[i,j]
                        pos+=1
                return matrix(c(result.flatten()),self.nrow,self.ncol,True,**self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Matrix product
    def __rmatmul__(self,value):
        if isinstance(value,np.ndarray):
            if self.ncol==value.shape[0]:
                return matrix(c((value@self._data).flatten()),self.nrow,value.shape[1],True,**self.attributes)
            else:
                raise ArithmeticError("Dimension conditions for matrix product are not met")
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} cannot be matricially multiplied")
    
    #* UNARY DUNDER METHODS
    # Negative
    def __neg__(self):
        try:
            return matrix(c(-self._data.flatten()),self.nrow,self.ncol,True,**self.attributes)
        except TypeError:
            raise TypeError("Negative unary method only available for numeric matrixes") from None
        except Exception as excep:
            raise type(excep)(
                "A fatal error has occured. Please report this in our issues page: {}\
                \n\nPlease include, along with the error type, the following message in your report:\n\"{}\""\
                .format("https://github.com/Ricardo-Werner-Rivas/pyrcore/issues",excep)
            ) from None
    
    # Positive
    def __pos__(self):
        try:
            return matrix(c(+self._data.flatten()),self.nrow,self.ncol,True,**self.attributes)
        except TypeError:
            raise TypeError("Positive unary method only available for numeric matrixes") from None
        except Exception as excep:
            raise type(excep)(
                "A fatal error has occured. Please report this in our issues page: {}\
                \n\nPlease include, along with the error type, the following message in your report:\n\"{}\""\
                .format("https://github.com/Ricardo-Werner-Rivas/pyrcore/issues",excep)
            ) from None
    
    # Absolute value
    def __abs__(self):
        try:
            return matrix(c(abs(self._data.flatten())),self.nrow,self.ncol,True,**self.attributes)
        except TypeError:
            raise TypeError("Absolute value unary method only available for numeric matrixes") from None
        except Exception as excep:
            raise type(excep)(
                "A fatal error has occured. Please report this in our issues page: {}\
                \n\nPlease include, along with the error type, the following message in your report:\n\"{}\""\
                .format("https://github.com/Ricardo-Werner-Rivas/pyrcore/issues",excep)
            ) from None
    
    #* INDEXATION DUNDER METHODS
    # Getter
    def __getitem__(self,index):
        try:
            return self._data[index]
        except IndexError:
            if len(index)!=2:
                raise IndexError(
                    "Given one index. Two were expected"
                ) from None
            else:
                raise IndexError(
                    "One index is out of bounds"
                ) from None
        except Exception as excep:
            raise type(excep)(
                "A fatal error has occured. Please report this in our issues page: {}\
                \n\nPlease include, along with the error type, the following message in your report:\n\"{}\""\
                .format("https://github.com/Ricardo-Werner-Rivas/pyrcore/issues",excep)
            ) from None
    
    # Setter
    def __setitem__(self,index,value):
        try:
            self._data[index]=value
        except IndexError:
            if len(index)!=2:
                raise IndexError(
                    "Given one index. Two were expected"
                ) from None
            else:
                raise IndexError(
                    "One index is out of bounds"
                ) from None
        except Exception as excep:
            raise type(excep)(
                "A fatal error has occured. Please report this in our issues page: {}\
                \n\nPlease include, along with the error type, the following message in your report:\n\"{}\""\
                .format("https://github.com/Ricardo-Werner-Rivas/pyrcore/issues",excep)
            ) from None
    
    #^ No deleter
    
    #* LENGTH
    # Length
    def __len__(self):
        return self._data.size
    
    #* SCREEN
    # Representation
    def __repr__(self):
        return f"matrix(c({", ".join(str(value) for value in self._data.flatten())}),{self.nrow},{self.ncol},{True},**{self.attributes})"
    
    # HTML representation
    def _repr_html_(self):
        representation=f"""<table>"""
        if self.colnames is not None:
            representation+=f"""
            <thead>
                <tr>{f"\n<th style=\"text-align: center;\"></th>" if self.rownames is not None else ""}
                    {"\n".join([f"<th style=\"text-align: center;\">[,{col}]</th>" for col in self.colnames])}
                </tr>
            </thead>
            <tbody>"""
        for row in self._data:
            representation+="""
            \t<tr>"""
            if self.rownames is not None:
                representation+=f"""
                    <th style=\"text-align: center;\"><b>[{self.rownames[self._data.tolist().index(row.tolist())]},]</b></th>"""
            representation+=f"""
                    {"\n".join([f"<td style=\"text-align: center;\">{value}</td>" for value in row])}
                </tr>"""
        representation="\n".join(representation.split("\n")[:-1])
        if "<tbody>" in representation.split():
            representation+="""
            </tbody>"""
        representation+="""
        </table>"""
        return representation
    
    # Printing (__str__ method)
    def __str__(self):
        printing=f""
        printing+=(f"Rows' names: [{", ".join(self.rownames)}]\n" if self.rownames is not None else "")+(f"Columns' names: [{", ".join(self.colnames)}]\n" if self.colnames is not None else "")
        printing+=f"Dimensions: ({", ".join([str(dim) for dim in self.dim])})\n\n"
        printing+="\n".join(["\t".join([str(value) for value in row]) for row in self._data])
        #// if self.colnames is not None:
        #//     printing+=("\t " if self.rownames is not None else "")+f"[,{"]\t[,".join(self.colnames)}]\n"
        #// printing+="\n".join([("["+self.rownames[self._data.tolist().index(row.tolist())]+",]\t" if self.rownames is not None else "")+"\t".join(str(value) for value in row) for row in self._data])
        return printing

#* CLASS "TimeSeries"
class TimeSeries(RObject,Generic[TS]):
    #& Code comments
    """
    Class replicating R univariate time-series.\n
    ---
    Attributes:
    """
    #* METHODS
    # __init__
    def __init__(self,data:Vector[TS],start:Vector[int],end:Vector[int]|None,frequency:int,deltat:int|float,**attributes):
        """
        Arguments:
            data (`TS`): Data for the time-series
            start (`Vector`|`int`): Starting time of the observations
            end (`Vector`|`int`|`None`): Time of the last observation
            frequency (`int`): Number of observations per time unit
        """
        super().__init__(data,**attributes)
        self._type=data._type
        
        # Time management
        self._attributes["start"],self._attributes["end"],self._attributes["frequency"],self._attributes["deltat"]=start,end,frequency,deltat
        current=start.copy()
        time=[]
        for i in range(len(self._data)):
            time.append(current)
            if current==end:
                break
            current[1]+=1
            if current[1]>frequency:
                current[0]+=1
                current[1]=1
        self._time=time
    
    # Get/set attribute
    def attr(self,attribute:str,value=None):
        if value is None:
            return super().attr(attribute,value)
        elif any((attribute=="frequency" and value!=1/self._attributes["deltat"],attribute=="deltat" and value!=1/self._attributes["frequency"])):
            match attribute:
                case "frequency":
                    other="deltat"
                case "deltat":
                    other="frequency"
                case _:
                    pass
            self._attributes[attribute]=value
            self._attributes[other]=1/value
        else:
            self._attributes[attribute]=value
    
    # Structure
    def structure(self,**attributes)->TimeSeries:
        """
        Updates attributes dictionary. Similar to R `structure` function.
        Returns the `TimeSeries` object.\n
        ---
        Arguments:
            **attributes (Optional): Stream of attributes manually introduced.
        Both cannot be introduced at the same time.\n
        ---
        Returns:
            TimeSeries: Returns the `TimeSeries` instance with the updated attributes.
        """
        super().structure(**attributes)
        self.attr("frequency",self._attributes["frequency"])
        return self
    
    # Generate copy
    def copy(self)->TimeSeries:
        """
        Returns a copy of the `TimeSeries` object.\n
        ---
        Returns:
            TimeSeries: Copy of the `TimeSeries` object.
        """
        self._data:Vector[TS]
        return TimeSeries(self._data.copy(),**self._attributes)
    
    # Transform to list
    def tolist(self)->list:
        """
        Returns the data in a `list` object.\n
        ---
        Returns:
            list: Listed data of the `TimeSeries` object.
        """
        return self._data.tolist()
    
    # Transform to pandas.Series
    def to_pandas(self)->Series:
        """
        Returns a `pandas.Series` object equivalent to the `TimeSeries` object.\n
        ---
        Returns:
            pandas.Series: `pandas` equivalent to the `TimeSeries`object.
        """
        #? Create new index object to comfortably manage time
        from pandas import Series
        #^ Revise argument `index` in `pandas.Series`
        result=Series(self._data._data,index=[f"{str(date[0])}.{("0" if len(str(date[1]))==1 else "")+str(date[1])}" if self._attributes["frequency"]!=1 else date for date in self._time])
        del Series
        return result
    
    #* PROPERTIES
    # Type
    #¡ Getter
    # Setter
    @RObject.type.setter
    def type(self,new_type:type|str):
        super(TimeSeries,type(self)).type.__set__(self,new_type)
        self._data.type=self._type
    #^ No deleter