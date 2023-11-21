import sys
from functools import partial
import numpy as np
int_array = np.frompyfunc(int, 2, 1)

backupdata=sys.modules[__name__]
backupdata.alldtypes={}
def binrep(w,ar):
    return  [np.binary_repr(t,w).encode() for t in ar]
def zipint(arr):
    """
    Efficient compression and decompression of unsigned integer arrays using binary representation.

    This module provides functions for compressing and decompressing integer arrays efficiently
    using binary representation. It is designed to work with 2D numpy arrays and supports compression
    and decompression of unsigned integers in a way that minimizes storage space.

    Usage:
    from zipint import zipint,unzipint
    import numpy as np
    import pandas as pd

    df=pd.DataFrame(np.random.randint(2,1000,(5,5)))
    print(df.to_string())
    f1=zipint(df)
    print(f'{f1=}')
    f2=unzipint(f1)
    print(f'{f2=}')
    df2=pd.DataFrame(f2)
    print(df2.to_string())

    #      0    1    2    3    4
    # 0  393  489  469    4  777
    # 1  436  322  491  753  143
    # 2  257  275  920  303  176
    # 3  654  981  337  395  211
    # 4  444  337  972  251  749


    # f1=array([432633621254921, 479733330199695, 282870732340400, 720134299069651,
    #        488546033200877], dtype=uint64)


    # f2=array([[393, 489, 469,   4, 777],
    #        [436, 322, 491, 753, 143],
    #        [257, 275, 920, 303, 176],
    #        [654, 981, 337, 395, 211],
    #        [444, 337, 972, 251, 749]], dtype=uint64)


    #      0    1    2    3    4
    # 0  393  489  469    4  777
    # 1  436  322  491  753  143
    # 2  257  275  920  303  176
    # 3  654  981  337  395  211
    # 4  444  337  972  251  749

    Note: The module uses binary representation to efficiently store and retrieve unsigned integer values.
    The compressed data is stored as uint64 for optimization. If overflow occurs during conversion,
    the data is stored as an object type array.

    """
    maxval=np.max(arr)
    maxvalasbin = np.binary_repr(maxval)
    zfill = len(maxvalasbin)
    lookupdict={k:np.binary_repr(k,width=zfill).encode() for k in np.unique(arr)}
    cond_list = []
    choice_list = []
    for nom in lookupdict.items():
        cond_list.append(arr == nom[0])
        choice_list.append(nom[1])

    choice_list = np.array(choice_list, dtype=f'S{zfill}')
    binarray=np.select(cond_list, choice_list, b'0'*zfill)
    zfilltotal=zfill*arr.shape[1]
    joinedbyte=binarray.view('S1').reshape((-1, zfilltotal)).view(f'S{zfilltotal}')
    byteasdecimal=int_array(joinedbyte,2)
    try:
        dt2 = np.dtype(np.uint64, metadata={'origshape':arr.shape,"zfill": zfill,'zfilltotal':zfilltotal})
        byteasdecimalconv=np.array(byteasdecimal.flatten(),dtype=dt2)
        if byteasdecimalconv.dtype.metadata:
            backupdata.alldtypes[arr.shape[-1]] = {'origshape': arr.shape, "zfill": zfill, 'zfilltotal': zfilltotal}
            return byteasdecimalconv

    except OverflowError :
        pass
    dt2= np.dtype('object', metadata={'origshape':arr.shape,"zfill": zfill,'zfilltotal':zfilltotal})
    byteasdecimalconv=np.array(byteasdecimal.tolist(),dtype=dt2)
    backupdata.alldtypes[arr.shape[-1]]={'origshape':arr.shape,"zfill": zfill,'zfilltotal':zfilltotal}
    return byteasdecimalconv
def unzipint(arr):
    try:
        zfilltotalval=arr.dtype.metadata['zfilltotal']
        zfillval=arr.dtype.metadata["zfill"]
        origshape=arr.dtype.metadata['origshape'][-1]
    except Exception:
        zfilltotalval=backupdata.alldtypes[arr.shape[-1]]['zfilltotal']
        zfillval=backupdata.alldtypes[arr.shape[-1]]["zfill"]
        origshape=backupdata.alldtypes[arr.shape[-1]]['origshape'][-1]
    flala2 = np.ascontiguousarray(np.apply_along_axis(partial(binrep, zfilltotalval), 0, arr))
    flala3 = np.ascontiguousarray(flala2.view(f'S{zfillval}')).reshape((-1,origshape))
    return np.array(int_array(flala3,2),dtype=np.uint64)


