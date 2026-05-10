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
#¡ Code for abstractmethod redefinition
#*===============================================================================================================================

#^ The different types of comments require the "Colorful Comments Refreshed" extension for VSCode to be properly distinguished

#* IMPORTS
# Abstract method decorator and class ABCMeta
from abc import abstractmethod,ABCMeta
from functools import wraps

#* BASE CLASS "RObject"
class RObject(metaclass=ABCMeta):
    #& Code comments
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
    def __init_subclass__(cls):
        for method in (getattr(cls,met) for met in "structure copy deepcopy".split()):
            @wraps(method)
            def wrapper(self,*args,**kwargs):
                return method(self,*args,**kwargs)
            wrapper.__doc__=method.__doc__.format(class_name=cls.__name__)
            setattr(cls,method.__name__,wrapper)
    
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
    def structure(self,**attributes)->RObject:
        """
        Updates attributes dictionary. Similar to R `structure` function.
        Returns the `{class_name}` object.\n
        ---
        Arguments:
            **attributes (Optional): Stream of attributes manually introduced.
        Both cannot be introduced at the same time.\n
        ---
        Returns:
            {class_name}: Returns the `{class_name}` instance with the updated attributes.
        """
        for attribute,value in attributes.items():
            self.attr(attribute,value)
        return self
    
    # Generate copy
    def copy(self):
        """
        Returns a shallow copy of the `{class_name}` object.
        """
        from copy import copy
        return copy(self)
    
    # Deep copy
    def deepcopy(self):
        """
        Returns a deep copy of the `{class_name}` object.
        """
        from copy import deepcopy
        return deepcopy(self)
    
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
        return {key:value for key,value in self._attributes.items() if value is not None}
    #^ No setter
    #^ No deleter
    
    #* ATTRIBUTES' MANAGEMENT DUNDER METHODS
    # Attribute not found
    def __getattr__(self,attribute:str):
        try:
            return self.attributes[attribute]
        except KeyError:
            return
    
    #* COPYING DUNDER METHODS
    # Shallow copy
    @abstractmethod
    def __copy__(self):
        ...
    
    # Deep copy
    @abstractmethod
    def __deepcopy__(self):
        #¡ from copy import deepcopy
        ...