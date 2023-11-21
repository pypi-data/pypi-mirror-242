# Efficient compression and decompression of unsigned integer arrays using binary representation.

## pip install zipint

```python
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
```