#*===============================================================================================================================
#* LEGEND
#*-------------------------------------------------------------------------------------------------------------------------------
#! Missing
#& Missing unimportant
#~ Revision notes
#? Question
#* Section
#^ Important
# Normal comment
#// Alternative or deprecated code
#*===============================================================================================================================

#* IMPORTS
# `currentframe` function from `inspect` package
from inspect import currentframe

#* ATTRIBUTE ACCESS MANAGER
# Define the attribute access manager descriptor
class SubclassAttrAccessManager:
    """
    Descriptor to block any access to the associated attribute from outside the given base class's ecosystem.
    The descriptor is the one storing the value of the attribute, instead of the owner class.
    
    The descriptor contains `__get__`, `__set__` and `__delete__` methods.
    
    It should be instanced in the base class's `__init_subclass__` method.
    
    Example:
    ```
    # Loop for an iterable containing the common attributes for all subclasses
    for attr ("attr_1","attr_2","attr_3"):
        # Create the access manager descriptor instance
        access_manager=SubclassAttrAccessManager(<BaseClass>)
        # Link it to the desired attributes
        setattr(cls,attr,access_manager)
        # Execute the `__set_name__` method from the descriptor
        access_manager.__set_name__(cls,attr)
    ```
    
    Methods
    -------
    __init__
        Descriptor constructor.
        Stores the desired base class or its name for subclass ecosystem validation.
    __set_name__
        Stores the descriptor instance's name.
        Obtains the desired base class for subclass ecosystem validation if a base class name was given in `__init__` method.
    __get__
        Checks if descriptor is called internally or externally.
        Returns the stored value if called internally.
        Else, it raises an `AttributeError`.
    __set__
        Checks if descriptor is called internally or externally.
        Stores the new value if called internally.
        Else, it raises an `AttributeError`.
    __delete__
        Checks if descriptor is called internally or externally.
        Deletes the stored value if called internally.
        Else, it raises an `AttributeError`.
    """
    #* METHODS
    # __init__
    def __init__(self,base_class:str|type):
        """
        Arguments
        ---------
        base_class : `str`|`type`
            Base class (or its name) from which ecosystem attribute access and manipulation is allowed.
        """
        # Store the base class (or its name)
        self.base=base_class
        # Initialize `value` attribute
        self.value={}
    
    # Custom name
    def __set_name__(self,owner:type,name:str):
        """
        Stores the descriptor instance's name.
        Obtains the desired base class for subclass ecosystem validation if a base class name was given in `__init__` method.
        
        Arguments
        ---------
        owner : `type`
            Class inside which the descriptor is instanced.
        name : `str`
            Descriptor instance's name.
        """
        # Store the variable's name
        self.name=name
        # Store the base class for inheritance descriptor duplication if a name was previously given
        if isinstance(self.base,str):
            self.base=owner.__bases__[tuple(base.__name__ for base in owner.__bases__).index(self.base)]
    
    # Getter
    def __get__(self,instance,owner:type):
        """
        Checks if descriptor is called internally or externally.
        Returns the stored value if called internally.
        
        Arguments
        ---------
        instance : `Any`
            Instance of the class inside which the descriptor was instanced.
        owner : `type`
            Class inside which the descriptor is instanced.
        
        Returns
        -------
        Any
            Value for the attribute for which the descriptor was instanced.
            This value is stored in the descriptor.
        
        Raises
        ------
        AttributeError
            If the attribute for which the descriptor was instanced is called outside the given base class's ecosystem.
        """
        # If the object calling the descriptor is an instance of a subclass of the base class's ecosystem
        if instance is not None and issubclass(currentframe().f_back.f_locals.get("self",None).__class__,self.base):
            # Return the stored value
            return self.value[id(instance)]
        # Else
        else:
            # Raise an `AttributeError`
            raise AttributeError(f"Attribute \"{self.name}\" is not accessible outside the \"{owner.__name__}\" class")
    
    # Setter
    def __set__(self,instance,value):
        """
        Checks if descriptor is called internally or externally.
        Stores the new value if called internally.
        
        Arguments
        ---------
        instance : `Any`
            Instance of the class inside which the descriptor was instanced.
        value : `Any`
            New value for the attribute for which the descriptor was instanced.
        
        Raises
        ------
        AttributeError
            If the attribute for which the descriptor was instanced is called outside the given base class's ecosystem.
        """
        # If the object calling the descriptor matches the received instance
        if issubclass(currentframe().f_back.f_locals.get("self",None).__class__,self.base):
            # Store the new value
            self.value[id(instance)]=value
        # Else
        else:
            # Raise an `AttributeError`
            raise AttributeError(f"Attribute \"{self.name}\" is not accessible outside the \"{instance.__class__.__name__}\" class")
    
    # Deleter
    def __delete__(self,instance):
        """
        Checks if descriptor is called internally or externally.
        Deletes the stored value if called internally.
        
        Arguments
        ---------
        instance : `Any`
            Instance of the class inside which the descriptor was instanced.
        
        Raises
        ------
        AttributeError
            If the attribute for which the descriptor was instanced is called outside the given base class's ecosystem.
        """
        # If the object calling the descriptor matches the received instance
        if issubclass(currentframe().f_back.f_locals.get("self",None).__class__,self.base):
            # Delete the stored value
            del self.value[id(instance)]
        # Else
        else:
            # Raise an `AttributeError`
            raise AttributeError(f"Attribute \"{self.name}\" is not accessible outside the \"{instance.__class__.__name__}\" class")