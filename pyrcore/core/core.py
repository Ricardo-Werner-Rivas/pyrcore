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
#¡ Needed code for abstractmethod redefinition
#*===============================================================================================================================

#^ The different types of comments require the "Colorful Comments Refreshed" extension for VSCode to be properly distinguished

#* IMPORTS
# Abstract method decorator and class ABCMeta
from abc import abstractmethod,ABCMeta

#* BASE CLASS "RObject"
class RObject(metaclass=ABCMeta):
    #& Missing code comments
    """
    Base class for every R-based or *R-like* object or class in `pyrcore` package.
    """
    #* METHODS
    # __init__
    @abstractmethod
    def __init__(self,data,**attributes):
        self._data=data
        self._attributes=attributes or {}
        self._type:type=type(data)
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
        #¡ if value is None:
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
        #¡ else/elif ...:
    # Structure
    @abstractmethod
    def structure(self,**attributes)->RObject:
        ...
        self._attributes.update(attributes)
        return self
    
    #* PROPERTIES
    # Type
    @property
    # Getter
    def type(self)->type:
        return self._type
    # Setter
    @type.setter
    @abstractmethod
    def type(self,new_type:type|str):
        if isinstance(new_type,type):
            self._type=new_type
        else:
            self._type:type=eval(new_type)
        ...
    #^ No deleter
    
    # Attributes
    @property
    # Getter
    def attributes(self):
        #¡ Introduce controls for subclass specific R attributes if needed
        return self._attributes
    #^ No setter
    #^ No deleter