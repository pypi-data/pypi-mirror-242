from __future__ import annotations

from . import matrix, vector

def delete_matrix(matrix: Matrix):
    matrix = matrix * 0
    del matrix