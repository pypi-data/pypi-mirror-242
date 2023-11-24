"""
Matrix Library

A Python library for working with matrices and performing matrix operations.

Usage
----------
	import matrixlib

	# Example Usage
 
	matrix = matrixlib.matrix.Matrix((3, 3)) # Result: [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
 
Key Classes/Functions
----------
	- Matrix : Represents a matrix and provides numerous operations for manipulating matrices.

Examples
----------
	from matrixlib.matrix import Matrix

	matrix = Matrix((3, 3))

	matrix.set_value(1, 3, 6) # Result: [[0, 0, 6], [0, 0, 0], [0, 0, 0]]

 	transposed = matrix.transpose()

 	print(transposed) # Output:

 	0 0 0\n
	0 0 0\n
 	6 0 0

Version: 0.2.04 (HELP, HOW DOES VERSION SCHEMA WORK???)

Author: Jemma Starecki

Made By <a href="https://github.com/JemmaFromJupiter" target="_blank">JemmaFromJupiter</a> On Github.
"""
from __future__ import annotations
from . import matrix
from . import vector
from . import utils

__version__ = "0.2.05"
__author__ = "JemmaFromJupiter"

__all__ = ["matrix", "vector", "utils"]
