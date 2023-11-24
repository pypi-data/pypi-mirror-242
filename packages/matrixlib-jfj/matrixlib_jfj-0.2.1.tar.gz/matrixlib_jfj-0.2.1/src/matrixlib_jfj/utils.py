from __future__ import annotations

from . import matrix, vector

def delete_matrix(mat: matrix.Matrix):
    matrix = matrix * 0
    del matrix
    
def is_square(mat: matrix.Matrix):
    if matrix.shape[0] == matrix.shape[1]:
        return True
    else:
        return False