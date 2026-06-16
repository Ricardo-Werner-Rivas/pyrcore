# Imports
from .core import Vector
from .functions import c
from .subclasses import MultiVariateTimeSeries
from functools import singledispatchmethod
from types import NoneType

def _testSlice(index:slice,label:bool=True):
    return True\
    if\
        isinstance(index.start,(str,Vector,NoneType) if label else (int,NoneType))\
        and isinstance(index.stop,(str,Vector,NoneType) if label else (int,NoneType))\
        and (type(index.start)==type(index.stop) if all(index.start,index.stop) else True)\
    else False

# Indexer for "loc" property
class _LocIndexer:
    def __init__(self,data:MultiVariateTimeSeries):
        self.data=data
    
    @singledispatchmethod
    def __getitem__(self,index:Vector[int]|str|slice|tuple[Vector[int]|str|slice,str|slice]):
        raise TypeError
    @__getitem__.register
    def _(self,index:Vector):
        return c(self.data._data[self.data._time.index(index)],names=self.data.colnames)
    @__getitem__.register
    def _(self,index:str):
        return c(self.data._data[:,self.data.colnames.index(index)],names=self.data._time)
    @__getitem__.register
    def _(self,index:slice):
        if _testSlice(index):
            if isinstance(index.start,Vector):
                return MultiVariateTimeSeries(
                    self.data._data[
                        slice(
                            self.data._time.index(index.start) if index.start else None,
                            self.data._time.index(index.stop) if index.stop else None,
                            index.step
                        ),
                        :
                    ]
                )
            else:
                return MultiVariateTimeSeries(
                    self.data._data[
                        :,
                        slice(
                            self.data.colnames.index(index.start) if index.start else None,
                            self.data.colnames.index(index.stop) if index.stop else None,
                            index.step
                        )
                    ]
            )
        else:
            raise TypeError
    @__getitem__.register
    def _(self,index:tuple):
        #// index=list(index)
        #// for i,label in zip(range(len(index)),index):
        #//     if isinstance(label,str):
        #//         index[i]=(self.data.rownames if i==0 else self.data.colnames).index(label)
        #//     elif isinstance(label,Vector):
        #//         if i==0:
        #//             index[i]=self.data._time.index(label)
        #//         else:
        #//             raise TypeError
        #//     elif isinstance(label,slice) and _testSlice(label):
        #//         index[i]=slice(
        #//             (
        #//                 (
        #//                     self.data._time
        #//                     if isinstance(label.start,Vector)
        #//                     else self.data.rownames
        #//                 ) if i==0 else self.data.colnames
        #//             ).index(label.start)
        #//             if label.start
        #//             else None,
        #//             (
        #//                 (
        #//                     self.data._time
        #//                     if isinstance(label.stop,Vector)
        #//                     else self.data.rownames
        #//                 ) if i==0 else self.data.colnames
        #//             ).index(label.stop)
        #//             if label.stop
        #//             else None,
        #//             label.step
        #//         )
        #//     else:
        #//         raise TypeError
        #// index=tuple(index)
        #// return self.data._data[index]
        return self.data.loc[index[0]][index[1]]
    
    @singledispatchmethod
    def __setitem__(self,index:Vector[int]|str|slice|tuple[Vector[int]|str|slice,str|slice],value):
        raise TypeError
    @__setitem__.register
    def _(self,index:Vector,value):
        self.data._data[self.data._time.index(index)]=value
    @__setitem__.register
    def _(self,index:str,value):
        self.data._data[:,self.data.colnames.index(index)]=value
    @__setitem__.register
    def _(self,index:slice,value):
        if _testSlice(index):
            self.data._data[
                :,
                slice(
                    (
                        self.data.colnames
                        if isinstance(index.start,str) and index.start in self.data.colnames
                        else self.data._time
                    ).index(index.start) if index.start else None,
                    (
                        self.data.colnames
                        if isinstance(index.stop,str) and index.stop in self.data.colnames
                        else self.data._time
                    ).index(index.stop) if index.stop else None,
                    index.step
                )
            ]=value
    @__setitem__.register
    def _(self,index:tuple,value):
        index=list(index)
        for i,label in zip(range(len(index)),index):
            if isinstance(label,str):
                index[i]=(self.data.rownames if i==0 else self.data.colnames).index(label)
            elif isinstance(label,Vector):
                if i==0:
                    index[i]=self.data._time.index[label]
                else:
                    raise TypeError
            elif isinstance(label,slice) and _testSlice(label):
                if isinstance(label.start,Vector):
                    if i==0:
                        index[i]=slice(
                            self.data._time.index(label.start) if label.start else None,
                            self.data._time.index(label.stop) if label.stop else None,
                            label.step
                        )
                    else:
                        raise TypeError
                else:
                    index[i]=slice(
                        (self.data.rownames if i==0 else self.data.colnames).index(label.start) if label.start else None,
                        (self.data.rownames if i==0 else self.data.colnames).index(label.stop) if label.stop else None,
                        label.step
                    )
            else:
                raise TypeError
        index=tuple(index)
        self.data._data[index]=value

# Indexer for "iloc" property
class _IlocIndexer:
    def __init__(self,data:MultiVariateTimeSeries):
        self.data=data
    
    @singledispatchmethod
    def __getitem__(self,index:int|slice|tuple[int|slice,int|slice]):
        raise TypeError
    @__getitem__.register
    def _(self,index:int):
        return c(self.data._data[index],names=self.data.colnames)
    @__getitem__.register
    def _(self,index:slice):
        if _testSlice(index,False):
            return self.data._data[index]
        else:
            raise TypeError
    @__getitem__.register
    def _(self,index:tuple):
        #// for pos in index:
        #//     if isinstance(pos,int):
        #//         pass
        #//     elif isinstance(pos,slice) and _testSlice(pos,False):
        #//         pass
        #//     else:
        #//         raise TypeError
        #// return self.data._data[index]
        return self.data.iloc[index[0]][index[1]]
    
    @singledispatchmethod
    def __setitem__(self,index:int|slice|tuple[int|slice,int|slice],value):
        raise TypeError
    @__setitem__.register
    def _(self,index:int,value):
        self.data._data[index]=value
    @__setitem__.register
    def _(self,index:slice,value):
        if _testSlice(index,False):
            self.data._data[index]=value
        else:
            raise TypeError
    @__setitem__.register
    def _(self,index:tuple,value):
        for pos in index:
            if isinstance(pos,int):
                pass
            elif isinstance(pos,slice) and _testSlice(pos,False):
                pass
            else:
                raise TypeError
        self.data._data[index]=value

#// class _LocIndexer:
#//     def __init__(self,data:MultiVariateTimeSeries):
#//         self.data=data
    
#//     @singledispatchmethod
#//     def __getitem__(self,label:str|slice|tuple[str|slice,str|slice]):
#//         raise TypeError
#//     @__getitem__.register
#//     def _(self,label:str):
#//         return self.data[label]
#//     @__getitem__.register
#//     def _(self,label:slice):
#//         if not all(tuple(isinstance(element,(str,NoneType)) for element in (label.start,label.stop))):
#//             raise TypeError
#//         else:
#//             return self.data[label]
#//     @__getitem__.register
#//     def _(self,label:tuple[str|slice]):
#//         if not all(tuple(isinstance(axis,(str,slice)) for axis in label)):
#//             raise TypeError
#//         else:
#//             for element in label:
#//                 if isinstance(element,slice) and not all((isinstance(element.start,(str,NoneType)),isinstance(element.stop,(str,NoneType)))):
#//                     raise TypeError
#//         return self.data[label]
    
#//     def __setitem__(self,index,value):
#//         self.__getitem__(index)
#//         self.data[index]=value

#// class _IlocIndexer:
#//     def __init__(self,data:MultiVariateTimeSeries):
#//         self.data=data
    
#//     @singledispatchmethod
#//     def __getitem__(self,pos:int|slice|tuple[int|slice,int|slice]):
#//         raise TypeError
#//     @__getitem__.register
#//     def _(self,pos:int):
#//         return self.data[pos]
#//     @__getitem__.register
#//     def _(self,pos:slice):
#//         if not all(tuple(isinstance(element,(int,NoneType)) for element in (pos.start,pos.stop))):
#//             raise TypeError
#//         else:
#//             return self.data[pos]
#//     @__getitem__.register
#//     def _(self,pos:tuple[int|slice]):
#//         if not all(tuple(isinstance(axis,(int,slice)) for axis in pos)):
#//             raise TypeError
#//         else:
#//             for element in pos:
#//                 if isinstance(element,slice) and not all((isinstance(element.start,(int,NoneType)),isinstance(element.stop,(int,NoneType)))):
#//                     raise TypeError
#//         return self.data[pos]
    
#//     def __setitem__(self,index,value):
#//         self.__getitem__(index)
#//         self.data[index]=value