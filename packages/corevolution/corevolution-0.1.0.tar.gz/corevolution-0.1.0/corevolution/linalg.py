"""
Wrapper for linalg functions
"""

import os
import ctypes

from corevolution.helper import convert_array_to_matrix

current_dir = os.getcwd()
full_path = current_dir + "/corevolution/warp/outer.so"

_lib = ctypes.CDLL(full_path)

_lib.outer.argtypes = (
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_int,
)
_lib.outer.restype = ctypes.POINTER(ctypes.c_double)


def outer(array_1: list, array_2: list) -> list[list]:
    """Wrapper function to apply outer function to two lists"""
    assert len(array_1) == len(array_2), RuntimeError(
        "The length of the given arrays do not match."
        "Please make sure both arrays have the same dimension."
    )
    length = len(array_1)

    array_1 = (ctypes.c_double * length)(*array_1)
    array_2 = (ctypes.c_double * length)(*array_2)

    matrix = [0 for i in range(length * length)]
    matrix = (ctypes.c_double * (length * length))(*matrix)

    _lib.outer(array_1, array_2, matrix, length)

    result = convert_array_to_matrix(list(matrix), length, length)
    return result