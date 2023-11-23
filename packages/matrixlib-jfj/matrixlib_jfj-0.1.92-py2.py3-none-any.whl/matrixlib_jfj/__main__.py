from __future__ import annotations
from . import matrix, vector, utils

if __name__ == "__main__":
	matrix1 = matrix.Matrix(None, [
        [4, 7],
        [2, 6]
    ])

	print(matrix1, end="\n\n")

	matrix1.inverse()