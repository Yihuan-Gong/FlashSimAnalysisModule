from typing import TypeVar, List
from collections.abc import Iterable


class DataConverter:
    T = TypeVar('T') 
    
    def data3dTo2d(self, data3d: Iterable[Iterable[Iterable[T]]], axis: str, index: int) \
        -> Iterable[Iterable[T]]:
        match axis:
            case "x":
                return data3d[index,:,:]
            case "y":
                return data3d[:,index,:]
            case "z":
                return data3d[:,:,index]

    
    def data3dTo2dMiddle(self, data3d: Iterable[Iterable[Iterable[T]]], axis: str) \
        -> Iterable[Iterable[T]]:
        index = data3d[:][:].__len__()//2
        return self.data3dTo2d(data3d, axis, index)
    
    
    def data3dTo2dGetAxisName(self, axis: str) -> List[str]:
        '''
        return:
        List[0]: Horizonatal axis
        List[1]: Vertival axis
        '''
        axes = ["x", "y", "z"]
        axes.remove(axis)
        return axes