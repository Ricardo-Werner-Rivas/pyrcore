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
#*===============================================================================================================================

#^ The different types of comments require the "Colorful Comments Refreshed" extension for VSCode to be properly distinguished

#* IMPORTS
# Abstract method decorator and class ABCMeta
from abc import abstractmethod,ABCMeta

#* BASE CLASS "RObject"
class RObject(metaclass=ABCMeta):
    """
    Base class for all R-based or *R-like* object or class in this package.
    """
    #* METHODS
    # __init__
    @abstractmethod
    def __init__(self,data,**attributes):
        self._data=data
        self._attributes=attributes or {}
        self._type=type(data)
        ...
    # Get/set R attribute
    @abstractmethod
    def attr(self,attribute:str,value=None):
        """
        Gets the value of an attribute if `value` not provided.\n
        If `value` is provided, attribute is set to that value.\n
        ---
        Arguments:
            attribute (`str`): Attribute to get or set.
            value (`Any`|`None`, Optional): New value of the attribute.
        ---
        Returns:
            Any: Value of the fetched attribute (if `value` not given).
        """
        if value is None:
            try:
                return self._attributes[attribute]
            except KeyError:
                return None
            except Exception as excep:
                raise type(excep)(
                    f"""A fatal error occured, please report this in our issues page: https://github.com/Ricardo-Werner-Rivas/pyrcore/issues
                    Include the following error message in your report:
                    {excep}
                    """
                ) from None
    # Structure
    @abstractmethod
    def structure(self,atts:dict[str,]|None=None,**attributes):
        if atts and attributes:
            raise ValueError("Given both parameters. Only one expected.")
        else:
            attributes=attributes or atts
        self._attributes.update(attributes)
        ...
    
    #* PROPERTIES
    # Type
    @property
    # Getter
    def type(self):
        return self._type
    # Setter
    @type.setter
    @abstractmethod
    def type(self,new_type:"type|str"):
        if isinstance(new_type,type):
            self._type=new_type
        else:
            self._type=eval(new_type)
        ...
    #^ No deleter
    
    # Attributes
    @property
    # Getter
    def attributes(self):
        return {key:value for key,value in self._attributes.items() if value is not None}
    #^ No setter
    #^ No deleter