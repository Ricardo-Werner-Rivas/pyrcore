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

#* IMPORTS
# NumPy
import numpy as np
# TypeVar, Generic, Iterable and TYPE_CHECKING
from typing import TypeVar,Generic,Iterable,Literal,overload,TYPE_CHECKING
# Class RObject
from .core import RObject,Vector
# Combination function
from .functions import c

#* TYPING
# Import pandas.Series only for annotations
if TYPE_CHECKING:
    from pandas import Series,DataFrame
# Define new variable types with TypeVar
MT=TypeVar("MatrixDataTypes",int,float,str) # For matrixes
TS=TypeVar("TimeSeriesDataTypes") # For time-series
MTS=TypeVar("MultiVariateTimeSeries") # For multivariate time-series

#* CLASS "matrix"
class matrix(RObject,Generic[MT]):
    #~ Revise "attr()" and "structure()" methods and "attributes" property
    #& Code comments
    #& Documentation
    """
    Replicates R matrixes and R `matrix()` function.\n
    Unlike class `Vector`, this class properly creates the object so no auxiliar functions are needed.
    
    Attributes
    ----------
    data : `numpy.array`, Hidden
        Hidden attribute containing the data of the matrix in the form of a `numpy` array.
    attributes : `dict[str, Any]`, Hidden
        Hidden attribute containing the R like attributes of the matrix.
    
    Methods
    -------
    
    
    Properties
    ----------
    **nrow**
        Gets the number of rows
    **ncol**
        Gets the number of columns
    **dim**
        Gets the dimensions of the matrix
    **dimnames**
        Gets the names of rows and columns
    **rownames**
        Gets/sets the names of the rows
    **colnames**
        Gets/sets the names of the columns
    **attributes**
        Gets/sets the R like attributes of the matrix
    **type**
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
        Arguments
        ---------
        data : `Vector`|`Iterable`|`None`, Optional
            *Matrix-like* Python object to convert to an *R-like* matrix.
        nrow : `int`|`None`, Optional
            Number of rows to split the data. If not given, it is calculated.
        ncol : `int`|`None`, Optional
            Number of colums to split the data. If not given, it is calculated.
        byrow : `bool`, Optional
            Wether if the matrix will be built by rows (`True`) or by columns (`False`). `False` by default.
        dimnames : `tuple[Iterable[str]|None, Iterable[str]|None]`|`None`, Optional
            Ideally a tuple with the names for the rows (first position)
            and the names for the columns (second position).
            Any two position iterable works fine. Tuple is recommended if you just want to name the columns, so you can pass the following:
            ```
            m=matrix(<data>,<nrow>,2,dimnames=(None,["name1","name2"]))
            ```
            If only an iterable of strings is received, it will be passed to the rows.
        attributes : `dict[str, Any]`, Optional
            Stream of keyword arguments defining the matrix R attributes.
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
            if data.type in (int,float):
                data=c(data,tuple(0 for i in range(nrow*ncol-len(data))))
            elif data.type==bool:
                data=c(data,tuple(False for i in range(nrow*ncol-len(data))))
            else:
                data=c(data,tuple(float("nan") for i in range(nrow*ncol-len(data))))
        elif len(data)>nrow*ncol:
            data=data[:nrow*ncol]
        
        data_type=data._type
        data=data._data.reshape((nrow,ncol),order="C" if byrow else "F")
        super().__init__(data,**attributes)
        self._type=data_type
        self._attributes["dim"]=(nrow,ncol)
        match (
            isinstance(dimnames,Iterable),
            not any(
                tuple(isinstance(names,Iterable) for names in dimnames) if isinstance(dimnames,Iterable) else (False,)
            )
        ):
            case (False,True):
                dimnames=None
            case (True,True):
                dimnames=(dimnames,None)
            case (True,False):
                dimnames=tuple(c(names) if names else None for names in (dimnames if len(dimnames)<=2 else dimnames[:2]))
            case _:
                raise RuntimeError("A fatal error occured")
        self._attributes["dimnames"]=dimnames
        self._byrow=byrow
    
    # Get/set attribute
    def attr(self,attribute:str,value=None):
        if value is None:
            return super().attr(attribute,value)
        elif attribute=="dim" and value[0]*value[1]!=len(self._data):
            raise ValueError("Dimensions must fit the data")
        elif attribute=="dimnames":
            match value:
                case (None,None)|(float("nan"),float("nan")):
                    value=None
                case _:
                    if len(value)==2:
                        pass
                    elif len(value)>2 or all((len(value)<2,isinstance(value[0],Iterable))):
                        value=(c(value),None)
                    else:
                        raise ValueError("Dimnames cannot be a non-iterable")
                    if value[0]:
                        if len(value[0])==self.nrow:
                            pass
                        elif len(value[0])<self.nrow:
                            value=(c(value[0],*tuple(f"Row {row}" for row in range(len(value[0])+1,self.nrow+1))),value[1])
                        else:
                            raise ValueError("Rows' names iterable can't be larger than the number of rows")
                    if value[1]:
                        if len(value[1])==self.ncol:
                            pass
                        elif len(value[1])<self.ncol:
                            value=(value[0],c(value[1],*tuple(f"Column {col}" for col in range(len(value[1]+1),self.ncol+1))))
                        else:
                            raise ValueError("Columns' names iterable can't be larger than the number of columns")
        self._attributes[attribute]=value
    
    # Structure
    def structure(self,**attributes)->matrix[MT]:
        """
        Updates attributes dictionary. Similar to R `structure` function.
        Returns the `matrix` object.
        
        Arguments
        ---------
        attributes : `dict[str, Any]`, Optional
            Stream of R attributes manually introduced.
        
        Returns
        -------
        matrix
            Returns the `matrix` instance with the updated attributes.
        """
        return super().structure(**attributes)
    
    # Transform into vector
    def vectorize(self)->Vector[MT]:
        """
        Transforms the `matrix` object into a `Vector` object.
        
        Returns
        -------
        Vector
            Original `Vector` object from which the matrix was made from.
        """
        return c(self._data.base).structure(**self.attributes)
    
    # Transform to list
    def tolist(self)->list[MT]:
        """
        Returns the data in a `list` object.
        
        Returns
        -------
        list
            Listed data of the `matrix` object.
        """
        return self.vectorize().tolist()
    
    # Transform to tuple
    def tuple(self)->tuple[MT]:
        """
        Returns the data in a `tuple` object.
        
        Returns
        -------
        tuple
            Listed data of the `matrix` object.
        """
        return self.vectorize().tuple()
    
    # Determinant
    def det(self)->int|float:
        """
        Calculates the determinant of the matrix.
        
        Returns
        -------
        int|float
            Determinant of the matrix
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
            return sum(tuple(self._data[0,i]*((-1)**(1+i+1))*matrix(np.delete(self._data,i,1)[1:].base,self.nrow-1,self.ncol-1,self._byrow,**self.attributes).det() for i in range(self.ncol)))
    
    # Transpose
    def transpose(self)->matrix[MT]:
        """
        Switches rows and columns between each other.
        
        Returns
        -------
        matrix
            Transposed matrix
        """
        return matrix(self.vectorize(),self.nrow,self.ncol,not self._byrow,**self.attributes)
    
    #* PROPERTIES
    # Number of rows
    @property
    # Getter
    def nrow(self)->int:
        return self.dim[0]
    #^ No setter
    #^ No deleter
    
    # Number of columns
    @property
    # Getter
    def ncol(self)->int:
        return self.dim[1]
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
    def dimnames(self)->tuple[Iterable[str]|None,Iterable[str]|None]|None:
        return self.attributes["dimnames"] if "dimnames" in self.attributes else None
    #^ No setter
    #^ No deleter
    
    # Names of rows
    @property
    # Getter
    def rownames(self)->Vector[str]|None:
        return self.dimnames[0] if self.dimnames else None
    # Setter
    @rownames.setter
    def rownames(self,names:Iterable[str]|None):
        names=c(names) if names else None
        self.attr("dimnames",(names,self.colnames))
    #^ No deleter
    
    # Names of columns
    @property
    # Getter
    def colnames(self)->Vector[str]|None:
        return self.dimnames[1] if self.dimnames else None
    # Setter
    @colnames.setter
    def colnames(self,names:Iterable[str]|None):
        names=c(names) if names else None
        self.attr("dimnames",(self.rownames,names))
    #^ No deleter
    
    #¡ Attributes
    
    # Type
    #¡ Getter
    # Setter
    @RObject.type.setter
    def type(self,new_type:"type|str"):
        super(matrix,type(self)).type.__set__(self,new_type)
        self._data=np.array(tuple(self._type(value) for value in self._data.ravel()),dtype=object).reshape(self.nrow,self.ncol)
    #^ No deleter
    
    #* ATTRIBUTES' MANAGEMENT DUNDER METHODS
    # Attribute not found #¡ __getattr__
    
    #* COPYING DUNDER METHODS
    # Shallow copy #¡ __copy__
    def __copy__(self):
        return matrix(self.vectorize().copy(),*self.dim,byrow=self._byrow,**self.attributes)
    
    # Deep copy #¡ __deepcopy__
    def __deepcopy__(self):
        from copy import deepcopy
        return matrix(deepcopy(self.vectorize()),*self.dim,byrow=self._byrow,**deepcopy(self.attributes))
    
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
                return matrix((self._data+value._data).base,self.nrow,self.ncol,self._byrow,**self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(self._data.base+value._data,self.nrow,self.ncol,self._byrow,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]+=value[pos]
                        pos+=1
                return matrix(result.base,self.nrow,self.ncol,self._byrow,**self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(self._data.base+value,self.nrow,self.ncol,self._byrow,**self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Difference
    def __sub__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix((self._data-value._data).base,self.nrow,self.ncol,self._byrow,**self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(self._data.base-value._data,self.nrow,self.ncol,self._byrow,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]-=value[pos]
                        pos+=1
                return matrix(result.base,self.nrow,self.ncol,self._byrow,**self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(self._data.base-value,self.nrow,self.ncol,self._byrow,**self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Product
    def __mul__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix((self._data*value._data).base,self.nrow,self.ncol,self._byrow,**self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(c(self._data.base*value._data),self.nrow,self.ncol,self._byrow,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]*=value[pos]
                        pos+=1
                return matrix(result.base,self.nrow,self.ncol,self._byrow,**self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(self._data.base*value,self.nrow,self.ncol,self._byrow,**self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Division
    def __truediv__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix((self._data/value._data).base,self.nrow,self.ncol,**self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(self._data.base/value._data,self.nrow,self.ncol,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]/=value[pos]
                        pos+=1
                return matrix(result.base,self.nrow,self.ncol,self._byrow,**self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(self._data.base/value,self.nrow,self.ncol,self._byrow,**self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Integer division (floor division)
    def __floordiv__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix((self._data//value._data).base,self.nrow,self.ncol,self._byrow,**self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(self._data.base//value._data,self.nrow,self.ncol,self._byrow,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]//=value[pos]
                        pos+=1
                return matrix(result.base,self.nrow,self.ncol,self._byrow,**self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(self._data.base//value,self.nrow,self.ncol,self._byrow,**self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Module
    def __mod__(self,value):
        if isinstance(value,matrix):
            if self.dim==value.dim:
                return matrix((self._data%value._data).base,self.nrow,self.ncol,self._byrow,**self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(self._data.base%value._data,self.nrow,self.ncol,self._byrow,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]%=value[pos]
                        pos+=1
                return matrix(result.base,self.nrow,self.ncol,self._byrow,**self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(self._data.base%value,self.nrow,self.ncol,self._byrow,**self.attributes)
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
                return matrix((self._data**value._data).base,self.nrow,self.ncol,self._byrow,**self.attributes)
            else:
                raise ArithmeticError("Dimensions are not compatible")
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(self._data.base**value._data,self.nrow,self.ncol,self._byrow,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]**=value[pos]
                        pos+=1
                return matrix(result.base,self.nrow,self.ncol,self._byrow,**self.attributes)
        elif isinstance(value,(int,float)):
            return matrix(self._data.base**value,self.nrow,self.ncol,self._byrow,**self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Matrix product
    def __matmul__(self,value:"matrix|Vector|np.ndarray"):
        if isinstance(value,(matrix,Vector)):
            if self.ncol==value.nrow:
                return matrix((self._data@value._data).base,self.nrow,value.ncol,self._byrow,**self.attributes)
            else:
                raise ArithmeticError("Dimension conditions for matrix product are not met")
        elif isinstance(value,np.ndarray):
            if self.ncol==value.shape[0]:
                return matrix((self._data@value).base,self.nrow,value.shape[1],self._byrow,**self.attributes)
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
            return matrix(value%self._data.base,self.nrow,self.ncol,self._byrow,**self.attributes)
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(value._data%self._data.base,self.nrow,self.ncol,self._byrow,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]=value[pos]%result[i,j]
                        pos+=1
                return matrix(result.base,self.nrow,self.ncol,self._byrow,**self.attributes)
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
            return matrix(value**self._data.base,self.nrow,self.ncol,self._byrow,**self.attributes)
        elif isinstance(value,Vector):
            if len(value)>self.nrow*self.ncol:
                raise ArithmeticError("More values in vector than in matrix")
            elif len(value)==self.nrow*self.ncol:
                return matrix(value._data**self._data.base,self.nrow,self.ncol,self._byrow,**self.attributes)
            else:
                result=self._data.copy()
                pos=0
                for j in range(self.ncol):
                    for i in range(self.nrow):
                        if pos>=len(value):
                            pos=0
                        result[i,j]=value[pos]**result[i,j]
                        pos+=1
                return matrix(result.base,self.nrow,self.ncol,self._byrow,**self.attributes)
        else:
            data_type=str(type(value))
            data_type=data_type[data_type.find("'"):data_type.rfind("'")+1]
            raise TypeError(f"Object type {data_type} is not operable with matrixes")
    
    # Matrix product
    def __rmatmul__(self,value):
        if isinstance(value,np.ndarray):
            if self.ncol==value.shape[0]:
                return matrix((value@self._data).base,self.nrow,value.shape[1],self._byrow,**self.attributes)
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
            return matrix(-self._data.base,self.nrow,self.ncol,self._byrow,**self.attributes)
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
            return matrix(+self._data.base,self.nrow,self.ncol,self._byrow,**self.attributes)
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
            return matrix(abs(self._data.base),self.nrow,self.ncol,self._byrow,**self.attributes)
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
        return f"matrix(c({", ".join(str(value) for value in self._data.base)}),{self.nrow},{self.ncol},{self._byrow},**{self.attributes})"
    
    # HTML representation
    def _repr_html_(self):
        representation="""\
<div>
<style scoped>
    .matrix thead th {
        text-align: center;
    }
    .matrix tbody tr {
        text-align: center;
    }
</style>
<table class="matrix">
"""
        if self.colnames:
            representation+=f"""\
    <thead>
        <tr>{f"\n<th></th>" if self.rownames else ""}
            {"\n\
            ".join(tuple(f"<th>[,{col}]</th>" for col in self.colnames))
            }
        </tr>
    </thead>
"""
        representation+="""\
    <tbody>
"""
        for row in self._data:
            representation+="""\
        <tr>
"""
            if self.rownames:
                representation+=f"""\
            <th>[{self.rownames[self._data.tolist().index(row.tolist())]},]</th>
"""
            representation+=f"""\
            {"\n\
            ".join(tuple(f"<td>{value}</td>" for value in row))
            }
        </tr>
"""
        representation+="""\
    </tbody>
</table>
</div>\
"""
        return representation
    
    # Printing (__str__ method)
    def __str__(self):
        printing=f""
        printing+=(f"Rows' names: [{", ".join(self.rownames)}]\n" if self.rownames is not None else "")+(f"Columns' names: [{", ".join(self.colnames)}]\n" if self.colnames is not None else "")
        printing+=f"Dimensions: ({", ".join(tuple(str(dim) for dim in self.dim))})\n\n"
        printing+="\n".join(["\t".join(tuple(str(value) for value in row)) for row in self._data])
        #// if self.colnames is not None:
        #//     printing+=("\t " if self.rownames is not None else "")+f"[,{"]\t[,".join(self.colnames)}]\n"
        #// printing+="\n".join([("["+self.rownames[self._data.tolist().index(row.tolist())]+",]\t" if self.rownames is not None else "")+"\t".join(str(value) for value in row) for row in self._data])
        return printing

#* CLASS "TimeSeries"
class TimeSeries(RObject,Generic[TS]):
    #& Code comments
    #& Documentation
    """
    Class replicating R univariate time-series.
    
    Attributes
    ----------
    """
    #* METHODS
    # __init__
    def __init__(self,data:Vector[TS],start:Vector[int],end:Vector[int]|None,frequency:int,**attributes):
        """
        Arguments
        ---------
        data : `Vector`
            Data for the time-series
        start : `Vector`|`int`
            Starting time of the observations
        end : `Vector`|`int`|`None`
            Time of the last observation
        frequency : `int`
            Number of observations per time unit
        deltat : `int`|`float`
            Inverse of `frequency`
        attributes : `dict[str, Any]`, Optional
            Keyword arguments for R-like attributes
        """
        self._data:Vector[TS]
        super().__init__(data,**attributes)
        self._type=data._type
        
        # Time management
        current=start.copy()
        time:tuple[Vector[int]]=tuple()
        for i in range(len(self._data)):
            time=(*time,current.copy())
            if end is not None and all(current==end):
                break
            current[1]+=1
            if current[1]>frequency:
                current[0]+=1
                current[1]=1
        if end is None:
            end=time[-1]
        self._time,self._attributes["start"],self._attributes["end"],self._attributes["frequency"]=time,start,end,frequency
    
    # Get/set attribute
    def attr(self,attribute:str,value=None):
        if value is None:
            return super().attr(attribute,value)
        elif attribute in "start end".split():
            match type(value).__name__:
                case "int":
                    value=c(value,1)
                case "Vector":
                    if len(value)==0:
                        value=None
                    elif len(value)<2:
                        value=c(value,1)
                    elif len(value)>2:
                        raise ValueError(f"Invalid length for new \"{attribute}\" R attribute value (maximum 2)")
                case _:
                    if isinstance(value,Iterable) and not isinstance(value,str):
                        self.attr(attribute,c(value))
                    else:
                        raise ValueError(f"Expected \"{attribute}\" value is a \"Vector\" or \"int\" object or \"None\", but something else was given")
        elif attribute in "frequency deltat".split():
            match attribute:
                case "deltat":
                    attribute="frequency"
                    value=int(1/value) if int(1/value)>0 else 1
                case _:
                    value=int(value) if int(value)>0 else 1
        self._attributes[attribute]=value
    
    # Structure
    def structure(self,**attributes)->TimeSeries[TS]:
        """
        Updates attributes dictionary. Similar to R `structure` function.
        Returns the `TimeSeries` object.
        
        Arguments
        ---------
        attributes : `dict[str, Any]`, Optional
            Stream of attributes manually introduced.
        
        Returns
        -------
        TimeSeries
            Returns the `TimeSeries` instance with the updated attributes.
        """
        return super().structure(**attributes)
    
    # Time
    def time(self)->TimeSeries[float]:
        """
        Returns the time at which each observation data was taken, just like R does with its function `time()`.
        
        Returns
        -------
        TimeSeries
            `TimeSeries` object containing the time at which each data piece was taken instead of the original data.
        """
        return TimeSeries(c(tuple(f"{float(date[0]+self.deltat*(date[1]-1)):.3f}" for date in self._time)),**self.attributes)
    
    # Stational indexes
    def cycle(self)->TimeSeries[int]:
        """
        Returns the period of the time unit for each data piece. Replicates R `cycle()` function.
        
        Returns
        -------
        TimeSeries
            A `TimeSeries` object with same dimensions and
            R attributes as the original containing the stational indexes of each time unit for each data piece.
        """
        return TimeSeries(c(tuple(date[1] for date in self._time)),**self.attributes)
    
    # Window
    def window(
        self,
        start:Vector[int]|int|None=None,end:Vector[int]|int|None=None,
        frequency:int|None=None,deltat:float|int|None=None,
        extend:bool=False
    )->TimeSeries[TS]:
        """
        Replicates the R `window()` function and creates another `TimeSeries` object with the requested data.
        
        Arguments
        ---------
        start : `Vector[int]`|`int`|`None`, Optional
            New starting point.
        end : `Vector[int]`|`int`|`None`, Optional
            New ending point.
        frequency : `int`|`None`, Optional
            New frequency.
        deltat : `float`|`int`|`None`, Optional
            New `deltat`.
        extend : `bool`, Optional
            Whether to extend the series or not if `start` and/or `end` are not in the original time interval.
            Defaults to `False`.
        
        Returns
        -------
        TimeSeries
            Slice of the requested data as a new `TimeSeries` object.
        """
        data=self._data.copy()
        if not start:
            start=c(self.start,1) if isinstance(self.start,int) else self.start.copy()
        elif isinstance(start,int):
            start=c(start,1)
        if not end:
            end=c(self.end,1) if isinstance(self.end,int) else self.end.copy()
        elif isinstance(end,int):
            end=c(end,1)
        if frequency and deltat:
            if deltat!=1/frequency:
                raise ValueError("Parameters 'frequency' and 'deltat' should be the inverse of one another")
        elif frequency:
            deltat=1/frequency
        elif deltat:
            frequency=1/deltat
        else:
            frequency=self.frequency
            deltat=self.deltat
        time:tuple[Vector[int]]=self._time
        if start not in time:
            if extend:
                limit=time[0].copy()
                time=tuple()
                current=start.copy()
                while True:
                    time=(*time,current)
                    current[1]+=1
                    if current[1]>self.frequency:
                        current[0]+=1
                        current[1]=1
                    if all(current==limit):
                        break
                missing_start=len(time)
                time=(*time,*self._time)
            else:
                start=c(self.start,1) if isinstance(self.start,int) else self.start.copy()
                missing_start=None
                print("Warning: Value of parameter 'start' not changed")
        if end not in time:
            if extend:
                add_on:tuple[Vector[int]]=tuple()
                current=time[-1].copy()
                while True:
                    add_on=(*add_on,current)
                    if all(current==end):
                        break
                    current[1]+=1
                    if current[1]>self.frequency:
                        current[0]+=1
                        current[1]=1
                missing_end=len(add_on)
                time=(*time,*add_on)
            else:
                end=c(self.end,1) if isinstance(self.end,int) else self.end.copy()
                missing_end=None
                print("Warning: Value of parameter 'end' not changed")
        if missing_start:
            data=c(tuple(float("nan") for i in range(missing_start)),data)
        if missing_end:
            data=c(data,tuple(float("nan") for i in range(missing_end)))
        if frequency!=self.frequency and self.frequency%frequency==0:
            data=data[time.index(start):time.index(end):self.frequency/frequency]
        elif frequency!=self.frequency:
            frequency=self.frequency
            deltat=self.deltat
            print("Warning: Value of parameter 'frequency' not changed")
        return TimeSeries(data,start,end,frequency,deltat)
    
    # Transform to list
    def tolist(self)->list[TS]:
        """
        Returns the data in a `list` object.
        
        Returns
        -------
        list
            Listed data of the `TimeSeries` object.
        """
        return self._data.tolist()
    
    # Transform to tuple
    def tuple(self)->tuple[TS]:
        """
        Returns the data in a `tuple` object.
        
        Returns
        -------
        tuple
            Listed data of the `TimeSeries` object.
        """
        return self._data.tuple()
    
    # Transform to pandas.Series
    def to_pandas(self)->Series[TS]:
        """
        Returns a `pandas.Series` object equivalent to the `TimeSeries` object.
        
        Returns
        -------
        pandas.Series
            `pandas` equivalent to the `TimeSeries`object.
        """
        #? Create new index object to comfortably manage time
        from pandas import Series
        #~ Revise argument `index` in `pandas.Series`
        return Series(self._data._data,tuple(f"{str(date[0])}.{("0" if len(str(date[1]))==1 else "")+str(date[1])}" for date in self._time) if self.frequency!=1 else self._time,self.type)
    
    #* PROPERTIES
    # Type
    #¡ Getter
    # Setter
    @RObject.type.setter
    def type(self,new_type:type|str):
        super(TimeSeries,type(self)).type.__set__(self,new_type)
        self._data.type=self._type
    #^ No deleter
    
    # Start
    @property
    # Getter
    def start(self)->Vector[int]|int:
        return self.attributes["start"]
    # Setter
    @start.setter
    def start(self,new_start:Vector[int]|int|None):
        if new_start:
            self.attr("start",new_start)
        else:
            del self.start
    # Deleter
    @start.deleter
    def start(self):
        self.start=1 if self.frequency==1 else c(1,1)
    
    # End
    @property
    # Getter
    def end(self)->Vector[int]|int:
        return self.attributes["end"]
    # Setter
    @end.setter
    def end(self,new_end:Vector[int]|int|None):
        if new_end:
            self.attr("end",new_end)
        else:
            del self.end
    # Deleter
    @end.deleter
    def end(self):
        if self.frequency==1:
            self.end=c(len(self._data),1)
        else:
            end=self.start.copy()
            end[1]+=len(self._data)-1
            year=end[0]+end[1]//self.frequency-1
            if end[1]%self.frequency!=0:
                year+=1
            period=end[1]%self.frequency
            if period==0:
                period=self.frequency
            end[0],end[1]=year,period
            self.end=end.copy()
    
    # Frequency
    @property
    # Getter
    def frequency(self)->int:
        return self.attributes["frequency"]
    # Setter
    @frequency.setter
    def frequency(self,new_frequency:int):
        self.attr("frequency",new_frequency)
    # Deleter
    @frequency.deleter
    def frequency(self):
        self.frequency=1
    
    # Deltat
    @property
    # Getter
    def deltat(self)->int|float:
        return 1/self.frequency
    # Setter
    @deltat.setter
    def deltat(self,new_deltat:int|float):
        self.attr("deltat",new_deltat)
    # Deleter
    @deltat.deleter
    def deltat(self):
        self.deltat=1
    
    #¡ Attributes
    
    #* ATTRIBUTES' MANAGEMENT DUNDER METHODS
    # Attribute not found #¡ __getattr__
    
    #* COPYING DUNDER METHODS
    # Shallow copy
    def __copy__(self):
        return TimeSeries(self._data.copy(),**self.attributes)
    
    # Deep copy
    def __deepcopy__(self):
        from copy import deepcopy
        return TimeSeries(deepcopy(self._data),**deepcopy(self.attributes))
    
    #* COMPARATIVE DUNDER METHODS
    # Equality
    def __eq__(self,value):
        return self._data==value if not isinstance(value,TimeSeries) else self._data==value._data
    
    # Inequality
    def __ne__(self,value):
        return self._data!=value if not isinstance(value,TimeSeries) else self._data!=value._data
    
    # Less than
    def __lt__(self,value):
        return self._data<value if not isinstance(value,TimeSeries) else self._data<value._data
    
    # Less or equal
    def __le__(self,value):
        return self._data<=value if not isinstance(value,TimeSeries) else self._data<=value._data
    
    # Greater than
    def __gt__(self,value):
        return self._data>value if not isinstance(value,TimeSeries) else self._data>value._data
    
    # Greater or equal
    def __ge__(self,value):
        return self._data>=value if not isinstance(value,TimeSeries) else self._data>=value._data
    
    #* ARITHMETIC DUNDER METHODS
    # Addition
    def __add__(self,value):
        return TimeSeries(self._data+value if not isinstance(value,TimeSeries) else self._data+value._data,**self.attributes)
    
    # Difference
    def __sub__(self,value):
        return TimeSeries(self._data-value if not isinstance(value,TimeSeries) else self._data-value._data,**self.attributes)
    
    # Product
    def __mul__(self,value):
        return TimeSeries(self._data*value if not isinstance(value,TimeSeries) else self._data*value._data,**self.attributes)
    
    # Division
    def __truediv__(self,value):
        return TimeSeries(self._data/value if not isinstance(value,TimeSeries) else self._data/value._data,**self.attributes)
    
    # Integer division (floor division)
    def __floordiv__(self,value):
        return TimeSeries(self._data//value if not isinstance(value,TimeSeries) else self._data//value._data,**self.attributes)
    
    # Module
    def __mod__(self,value):
        return TimeSeries(self._data%value if not isinstance(value,TimeSeries) else self._data%value._data,**self.attributes)
    
    # Divmod
    def __divmod__(self,value):
        return self//value,self%value
    
    # Power
    def __pow__(self,value):
        return TimeSeries(self._data**value if not isinstance(value,TimeSeries) else self._data**value._data,**self.attributes)
    
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
        return TimeSeries(value%self._data,**self.attributes)
    
    # Divmod
    def __rdivmod__(self,value):
        return value//self,value%self
    
    # Power
    def __rpow__(self,value):
        return TimeSeries(value**self._data,**self.attributes)
    
    #* UNARY DUNDER METHODS
    # Negative
    def __neg__(self):
        return TimeSeries(-self._data,**self.attributes)
    
    # Positive
    def __pos__(self):
        return TimeSeries(+self._data,**self.attributes)
    
    # Absolute value
    def __abs__(self):
        return TimeSeries(abs(self._data),**self.attributes)
    
    #* INDEXATION DUNDER METHODS
    # Getter
    def __getitem__(self,index):
        return self._data[index]
    
    # Setter
    def __setitem__(self,index,value):
        self._data[index]=value
    
    #* LENGTH
    # Length
    def __len__(self):
        return len(self._data)
    
    #* SCREEN
    # Representation
    def __repr__(self):
        return f"TimeSeries({repr(self._data)}{", ".join(tuple(f"{attribute}={str(value) if not isinstance(value,Vector) else repr(value)}" for attribute,value in self.attributes.items()))})"
    
    # HTML representation
    def _repr_html_(self):
        if self.frequency>1:
            match self.frequency:
                case 4:
                    headers=tuple(f"<th>Q{quarter}</th>" for quarter in range(1,5))
                case 12:
                    headers=tuple(f"<th>{month}</th>" for month in "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())
                case _:
                    headers=tuple(f"<th>p{i+1}</th>" for i in range(self.frequency))
            representation=f"""\
<table>
    <thead>
        <tr>
            <th></th>
            {"\n\
            ".join(headers)}
        </tr>
    </thead>
    <tbody>
"""
            data=["<td></td>" for i in range(self.start[1]-1)] if self.start[1]-1>0 else []
            data.extend([f"<td>{str(value)}</td>" for value in self._data])
            if self.frequency!=self.end[1]:
                data.extend(["<td></td>" for i in range(self.frequency-self.end[1])])
            data=[[data.pop(0) for i in range(self.frequency)] for i in range(len(data)//self.frequency)]
            for year in range(self.start[0],self.end[0]+1):
                representation+=f"""\
        <tr>
            <th>{year}</th>
            {("\n\
            ".join(value for value in data[year-self.start[0]]))}
        </tr>
"""
            representation+="""\
    </tbody>
</table>\
"""
        else:
            representation=f"<p>{"&emsp;·&emsp;".join(str(value) for value in self._data)}</p>"
        return representation
    
    # Printing (__str__ method)
    def __str__(self):
        return f"""\
Time Series:
Start={repr(self.start)}
End={repr(self.end)}
Frequency={self.frequency}

{repr(self._data)}\
"""

#* CLASS "MultiVariateTimeSeries"
class MultiVariateTimeSeries(RObject,Generic[MTS]):
    #& Code comments
    #& Documentation
    """
    Class replicating R multivariate time-series.
    
    Attributes
    ----------
    """
    #* METHODS
    # __init__
    def __init__(self,data:matrix[MTS],start:Vector[int],end:Vector[int]|None,frequency:int,deltat:int|float,**attributes):
        """
        Arguments
        ---------
        """
        self._data:matrix[MTS]
        super().__init__(data,**attributes)
        self._type=data._type
        
        # Time management
        current=start.copy()
        time:tuple[Vector[int]]=tuple()
        for i in range(len(self._data.vectorize())):
            time=(*time,current.copy())
            if end is not None and all(current==end):
                break
            current[1]+=1
            if current[1]>frequency:
                current[0]+=1
                current[1]=1
        if end is None:
            end=time[-1]
        self._time=time
        
        # R attributes initialization
        self._attributes["start"],self._attributes["end"],self._attributes["frequency"]=start,end,(frequency or 1/deltat)
        self._attributes["dim"],self._attributes["dimnames"]=data.dim,(None,data.colnames) if data.colnames else None
    
    # Get/set attribute
    def attr(self,attribute:str,value=None):
        if value is None:
            return super().attr(attribute,value)
        elif attribute=="dim" and value[0]*value[1]!=len(self._data):
            raise ValueError("Dimensions must fit the data")
        elif attribute=="dimnames":
            match value:
                case (None,None)|(float("nan"),float("nan")):
                    value=None
                case _:
                    if len(value)==2:
                        pass
                    elif len(value)>2 or all((len(value)<2,isinstance(value[0],Iterable))):
                        value=(c(value),None)
                    else:
                        raise ValueError("Dimnames cannot be a non-iterable")
                    if value[0]:
                        if len(value[0])==self.nrow:
                            pass
                        elif len(value[0])<self.nrow:
                            value=(c(value[0],*tuple(f"Row {row}" for row in range(len(value[0])+1,self.nrow+1))),value[1])
                        else:
                            raise ValueError("Rows' names iterable can't be larger than the number of rows")
                    if value[1]:
                        if len(value[1])==self.ncol:
                            pass
                        elif len(value[1])<self.ncol:
                            value=(value[0],c(value[1],*tuple(f"Column {col}" for col in range(len(value[1]+1),self.ncol+1))))
                        else:
                            raise ValueError("Columns' names iterable can't be larger than the number of columns")
        elif attribute in "start end".split():
            match type(value).__name__:
                case "int":
                    value=c(value,1)
                case "Vector":
                    if len(value)==0:
                        value=None
                    elif len(value)<2:
                        value=c(value,1)
                    elif len(value)>2:
                        raise ValueError(f"Invalid length for new \"{attribute}\" R attribute value (maximum 2)")
                case _:
                    if isinstance(value,Iterable) and not isinstance(value,str):
                        self.attr(attribute,c(value))
                    else:
                        raise ValueError(f"Expected \"{attribute}\" value is a \"Vector\" or \"int\" object or \"None\", but something else was given")
        elif attribute in "frequency deltat".split():
            match attribute:
                case "deltat":
                    attribute="frequency"
                    value=int(1/value) if int(1/value)>0 else 1
                case _:
                    value=int(value) if int(value)>0 else 1
        self._attributes[attribute]=value
    
    # Structure
    def structure(self,**attributes)->MultiVariateTimeSeries[MTS]:
        """
        Updates attributes dictionary. Similar to R `structure` function.
        Returns the `MultiVariateTimeSeries` object.
        
        Arguments
        ---------
        attributes : `dict[str, Any]`, Optional
            Stream of R attributes manually introduced.
        
        Returns
        -------
        MultiVariateTimeSeries
            Returns the `MultiVariateTimeSeries` instance with the updated attributes.
        """
        return super().structure(**attributes)
    
    # Time
    def time(self)->TimeSeries[float]:
        """
        Returns the time at which each observation data was taken, just like R does with its function `time()`.
        
        Returns
        -------
        TimeSeries
            `TimeSeries` object containing the time at which each data piece was taken instead of the original data.
        """
        return TimeSeries(c([f"{float(date[0]+self.deltat*(date[1]-1)):.3f}" for date in self._time]),**self.attributes)
    
    # Cycle
    def cycle(self)->TimeSeries[int]:
        """
        Returns the period of the time unit for each data piece. Replicates R `cycle()` function.
        
        Returns
        -------
        TimeSeries
            A `TimeSeries` object with same dimensions and
            R attributes as the original containing the stational indexes of each time unit for each data piece.
        """
        return TimeSeries(c(tuple(date[1] for date in self._time)),**self.attributes)
    
    # Window
    def window(
        self,
        start:Vector[int]|int|None=None,end:Vector[int]|int|None=None,
        frequency:int|None=None,deltat:float|int|None=None,
        extend:bool=False
    )->MultiVariateTimeSeries[TS]:
        """
        Replicates the R `window()` function and creates another `MultiVariateTimeSeries` object with the requested data.
        
        Arguments
        ---------
        start : `Vector[int]`|`int`|`None`, Optional
            New starting point.
        end : `Vector[int]`|`int`|`None`, Optional
            New ending point.
        frequency : `int`|`None`, Optional
            New frequency.
        deltat : `float`|`int`|`None`, Optional
            New `deltat`.
        extend : `bool`, Optional
            Whether to extend the series or not if `start` and/or `end` are not in the original time interval.
            Defaults to `False`.
        
        Returns
        -------
        MultiVariateTimeSeries
            Slice of the requested data as a new `MultiVariateTimeSeries` object.
        """
        data=self._data.copy()
        if not start:
            start=c(self.start,1) if isinstance(self.start,int) else self.start.copy()
        elif isinstance(start,int):
            start=c(start,1)
        if not end:
            end=c(self.end,1) if isinstance(self.end,int) else self.end.copy()
        elif isinstance(end,int):
            end=c(end,1)
        if frequency and deltat:
            if deltat!=1/frequency:
                raise ValueError("Parameters 'frequency' and 'deltat' should be the inverse of one another")
        elif frequency:
            deltat=1/frequency
        elif deltat:
            frequency=1/deltat
        else:
            frequency=self.frequency
            deltat=self.deltat
        time:tuple[Vector[int]]=self._time
        if start not in time:
            if extend:
                limit=time[0].copy()
                time=tuple()
                current=start.copy()
                while True:
                    time=(*time,current)
                    current[1]+=1
                    if current[1]>self.frequency:
                        current[0]+=1
                        current[1]=1
                    if all(current==limit):
                        break
                missing_start=len(time)
                time=(*time,*self._time)
            else:
                start=c(self.start,1) if isinstance(self.start,int) else self.start.copy()
                missing_start=None
                print("Warning: Value of parameter 'start' not changed")
        if end not in time:
            if extend:
                add_on:tuple[Vector[int]]=tuple()
                current=time[-1].copy()
                while True:
                    add_on=(*add_on,current)
                    if all(current==end):
                        break
                    current[1]+=1
                    if current[1]>self.frequency:
                        current[0]+=1
                        current[1]=1
                missing_end=len(add_on)
                time=(*time,*add_on)
            else:
                end=c(self.end,1) if isinstance(self.end,int) else self.end.copy()
                missing_end=None
                print("Warning: Value of parameter 'end' not changed")
        if missing_start:
            data=matrix(c(tuple(float("nan") for i in range(missing_start)),data.vectorize()),ncol=data.ncol,byrow=data._byrow,**data.attributes)
        if missing_end:
            data=matrix(c(data.vectorize(),tuple(float("nan") for i in range(missing_end))),ncol=data.ncol,byrow=data._byrow,**data.attributes)
        if frequency!=self.frequency and self.frequency%frequency==0:
            data=data[time.index(start):time.index(end):self.frequency/frequency]
        elif frequency!=self.frequency:
            frequency=self.frequency
            deltat=self.deltat
            print("Warning: Value of parameter 'frequency' not changed")
        return MultiVariateTimeSeries(data,start,end,frequency,deltat)
    
    # Transform to dictionary
    def todict(self,list:bool=False)->dict[str,list[MTS]]|list[dict[str,MTS]]:
        """
        Returns a dictionary with the `MultiVariateTimeSeries` object's data.
        
        Arguments
        ---------
        list : `bool`
            Whether to return a list of dictionaries (`True`), containing one dictionary per row, or a dictionary of lists (`False`).
            Defaults to `False`.
        
        Returns
        -------
        dict[str,list]|list[dict]
            Dictionary containing the `MultiVariateTimeSeries` object's data.
        """
        return dict(zip(self.colnames,self._data.transpose()._data.tolist())) if not list else [dict(zip(self.colnames,row)) for row in self._data._data.tolist()]
    
    # Obtain variable names
    def keys(self)->Vector[str]:
        """
        Returns an R-like vector of strings containing the names of the variables (or columns).
        
        Returns
        -------
        Vector[str]
            Vector of variables' names.
        """
        return self.colnames
    
    # Obtain values
    @overload
    def values(self,format:Literal["matrix"])->matrix[MTS]:
        """
        Returns the values of the `MultiVariateTimeSeries` object.
        
        Arguments
        ---------
        format : `Literal["matrix","rows","cols"]`, Optional
            Core values' matrix is returned.
        
        Returns
        -------
        matrix
            Values of the time-series as a `matrix` object.
        """
        ...
    @overload
    def values(self,format:Literal["rows"])->list[Vector[MTS]]:
        """
        Returns the values of the `MultiVariateTimeSeries` object.
        
        Arguments
        ---------
        format : `Literal["matrix","rows","cols"]`, Optional
            Formats the output to a list of rows as `Vector` objects.
        
        Returns
        -------
        list[Vector]
            Values of the time-series grouped by rows.
        """
        ...
    @overload
    def values(self,format:Literal["cols"])->list[Vector[MTS]]:
        """
        Returns the values of the `MultiVariateTimeSeries` object.
        
        Arguments
        ---------
        format : `Literal["matrix","rows","cols"]`, Optional
            Formats the output to a list of columns as `Vector` objects.
        
        Returns
        -------
        list[Vector]
            Values of the time-series grouped by columns.
            It can be zipped with a list of keys to create a dictionary.
        """
        ...
    def values(self,format:Literal["matrix","rows","cols"]="matrix")->list[Vector[MTS]]|matrix[MTS]:
        """
        Returns the values of the `MultiVariateTimeSeries` object.
        
        Arguments
        ---------
        format : `Literal["matrix","rows","cols"]`, Optional
            Format of the output.
            Defaults to `"matrix"`.
        
        Returns
        -------
        list[Vector]|matrix
            Values of the time-series.
        """
        match format:
            case "matrix":
                return self._data
            case "rows":
                return [c(value) for value in self._data._data.tolist()]
            case "cols":
                return [c(value) for value in tuple(self.todict().values())]
            case _:
                raise ValueError("Unexpected value given por argument \"format\"")
    
    # Transform to pandas.DataFrame
    def to_pandas(self)->DataFrame[MTS]:
        """
        Returns a `pandas.DataFrame` object equivalent to the `MultiVariateTimeSeries` object.
        
        Returns
        -------
        pandas.DataFrame
            `pandas` equivalent to the `MultiVariateTimeSeries`object.
        """
        from pandas import DataFrame
        return DataFrame(self._data._data,tuple(f"{str(date[0])}.{("0" if len(str(date[1]))==1 else "")+str(date[1])}" for date in self._time) if self.frequency!=1 else self._time,self.colnames,self.type)
    
    #* PROPERTIES
    # Type
    #¡ Getter
    # Setter
    @RObject.type.setter
    def type(self,new_type:type|str):
        super(MultiVariateTimeSeries,type(self)).type.__set__(self,new_type)
        self._data.type=new_type
    #^ No deleter
    
    # Number of rows
    @property
    # Getter
    def nrow(self)->int:
        return self.dim[0]
    #^ No setter
    #^ No deleter
    
    # Number of columns
    @property
    # Getter
    def ncol(self)->int:
        return self.dim[1]
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
    def dimnames(self)->tuple[Iterable[str]|None,Iterable[str]|None]|None:
        return self.attributes["dimnames"] if "dimnames" in self.attributes else None
    #^ No setter
    #^ No deleter
    
    # Names of rows
    @property
    # Getter
    def rownames(self)->Vector[str]|None:
        return self.dimnames[0] if self.dimnames else None
    # Setter
    @rownames.setter
    def rownames(self,names:Iterable[str]|None):
        names=c(names) if names else None
        self.attr("dimnames",(names,self.colnames))
    #^ No deleter
    
    # Names of columns
    @property
    # Getter
    def colnames(self)->Vector[str]|None:
        return self.dimnames[1] if self.dimnames else None
    # Setter
    @colnames.setter
    def colnames(self,names:Iterable[str]|None):
        names=c(names) if names else None
        self.attr("dimnames",(self.rownames,names))
    #^ No deleter
    
    # Start
    @property
    # Getter
    def start(self)->Vector[int]|int:
        return self.attributes["start"]
    # Setter
    @start.setter
    def start(self,new_start:Vector[int]|int|None):
        if new_start:
            self.attr("start",new_start)
        else:
            del self.start
    # Deleter
    @start.deleter
    def start(self):
        self.start=1 if self.frequency==1 else c(1,1)
    
    # End
    @property
    # Getter
    def end(self)->Vector[int]|int:
        return self.attributes["end"]
    # Setter
    @end.setter
    def end(self,new_end:Vector[int]|int|None):
        if new_end:
            self.attr("end",new_end)
        else:
            del self.end
    # Deleter
    @end.deleter
    def end(self):
        if self.frequency==1:
            self.end=c(self.start[0]+len(self._data)-1,1)
        else:
            end=self.start.copy()
            end[1]+=len(self._data)-1
            year=end[0]+end[1]//self.frequency-1
            if end[1]%self.frequency!=0:
                year+=1
            period=end[1]%self.frequency
            if period==0:
                period=self.frequency
            end[0],end[1]=year,period
            self.end=end.copy()
    
    # Frequency
    @property
    # Getter
    def frequency(self)->int:
        return self.attributes["frequency"]
    # Setter
    @frequency.setter
    def frequency(self,new_frequency:int):
        self.attr("frequency",new_frequency)
    # Deleter
    @frequency.deleter
    def frequency(self):
        self.frequency=1
    
    # Deltat
    @property
    # Getter
    def deltat(self)->int|float:
        return 1/self.frequency
    # Setter
    @deltat.setter
    def deltat(self,new_deltat:int|float):
        self.attr("deltat",new_deltat)
    # Deleter
    @deltat.deleter
    def deltat(self):
        self.deltat=1
    
    #¡ Attributes
    
    #* ATTRIBUTES' MANAGEMENT DUNDER METHODS
    # Attribute not found #¡ __getattr__
    
    #* COPYING DUNDER METHODS
    # Shallow copy
    def __copy__(self):
        return MultiVariateTimeSeries(self._data.copy(),**self.attributes)
    
    # Deepcopy
    def __deepcopy__(self):
        from copy import deepcopy
        return MultiVariateTimeSeries(deepcopy(self._data),**deepcopy(self.attributes))
    
    #* COMPARATIVE DUNDER METHODS
    # Equality
    def __eq__(self,value):
        return self._data==value if not isinstance(value,MultiVariateTimeSeries) else self._data==value._data
    
    # Inequality
    def __ne__(self,value):
        return self._data!=value if not isinstance(value,MultiVariateTimeSeries) else self._data!=value._data
    
    # Less than
    def __lt__(self,value):
        return self._data<value if not isinstance(value,MultiVariateTimeSeries) else self._data<value._data
    
    # Less or equal
    def __le__(self,value):
        return self<value or self==value
    
    # Greater than
    def __gt__(self,value):
        return self._data>value if not isinstance(value,MultiVariateTimeSeries) else self._data>value._data
    
    # Greater or equal
    def __ge__(self,value):
        return self>value or self==value
    
    #* ARITHMETIC DUNDER METHODS
    # Addition
    def __add__(self,value):
        return MultiVariateTimeSeries(self._data+(value if not isinstance(value,MultiVariateTimeSeries) else value._data),**self.attributes)
    
    # Difference
    def __sub__(self,value):
        return MultiVariateTimeSeries(self._data-(value if not isinstance(value,MultiVariateTimeSeries) else value._data),**self.attributes)
    
    # Product
    def __mul__(self,value):
        return MultiVariateTimeSeries(self._data*(value if not isinstance(value,MultiVariateTimeSeries) else value._data),**self.attributes)
    
    # Division
    def __truediv__(self,value):
        return MultiVariateTimeSeries(self._data/(value if not isinstance(value,MultiVariateTimeSeries) else value._data),**self.attributes)
    
    # Integer division (floor division)
    def __floordiv__(self,value):
        return MultiVariateTimeSeries(self._data//(value if not isinstance(value,MultiVariateTimeSeries) else value._data),**self.attributes)
    
    # Module
    def __mod__(self,value):
        return MultiVariateTimeSeries(self._data%(value if not isinstance(value,MultiVariateTimeSeries) else value._data),**self.attributes)
    
    # Divmod
    def __divmod__(self,value):
        return self//value,self%value
    
    # Power
    def __pow__(self,value):
        return MultiVariateTimeSeries(self._data**(value if not isinstance(value,MultiVariateTimeSeries) else value._data),**self.attributes)
    
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
        return MultiVariateTimeSeries(value%self._data,**self.attributes)
    
    # Divmod
    def __rdivmod__(self,value):
        return value//self,value%self
    
    # Power
    def __rpow__(self,value):
        return MultiVariateTimeSeries(value**self._data,**self.attributes)
    
    #* UNARY DUNDER METHODS
    # Negative
    def __neg__(self):
        return MultiVariateTimeSeries(-self._data,**self.attributes)
    
    # Positive
    def __pos__(self):
        return MultiVariateTimeSeries(+self._data,**self.attributes)
    
    # Absolute value
    def __abs__(self):
        return MultiVariateTimeSeries(abs(self._data),**self.attributes)
    
    #* INDEXATION DUNDER METHODS
    # Getter
    def __getitem__(self,index:int|str|tuple[int|str,int|str])->Vector[MTS]|MultiVariateTimeSeries[MTS]:
        #~ Revise for slices
        match len(index): #! Wrong. Checking "int" length will raise an error.
            case 1:
                match type(index).__name__:
                    case "str":
                        return c(self._data[:,self.colnames.tuple().index(index)])
                    case "int":
                        return c(self._data[index])
                    case _:
                        raise TypeError(f"\"{type(index).__name__}\" index is not allowed")
            case 2:
                match type(index[0]).__name__:
                    case "str":
                        if self.rownames:
                            row=index[0]
                            index=(self.rownames.tuple().index(index[0]),index[1])
                        else:
                            raise ValueError(f"This \"{self.__class__.__name__}\" object has no \"rownames\" R attribute, so \"int\" index is expected")
                    case "int":
                        pass
                    case _:
                        raise TypeError(f"\"{type(index).__name__}\" index is not allowed")
                match type(index[1]).__name__:
                    case "str":
                        if self.colnames:
                            col=index[1]
                            index=(index[0],self.colnames.tuple().index(index[1]))
                        else:
                            raise ValueError(f"This \"{self.__class__.__name__}\" object has no \"colnames\" R attribute, so \"int\" index is expected")
                    case "int":
                        pass
                    case _:
                        raise TypeError(f"\"{type(index).__name__}\" index is not allowed")
                return self._data[index]
            case _:
                raise IndexError("Sequence index out of range.")
    
    # Setter
    def __setitem__(self,index:int|str|tuple[int|str,int|str],value):
        self.__getitem__(index)
        self._data[index]=value