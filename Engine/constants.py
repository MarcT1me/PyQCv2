""" Engine CONSTANTS
"""
from typing import BinaryIO


class __EngineEmptyClass:
    """ Engine data type class """

    def __init__(self, val, des: str): self.r, self.__des = val, des

    def __str__(self): return self.__des[0].upper() + self.__des[1:].lower() + 'Type'

    def __repr__(self): return self.__str__()

    def __bool__(self): return bool(self.r)

    def __eq__(self, other): return self.r is other

    def __ne__(self, other): return self.r is not other


""" types """
# nullable date
NULL = 0
EMPTY = __EngineEmptyClass(None, 'EMPTY')
# file types
BINARY = __EngineEmptyClass(BinaryIO, 'BINARY')
TEXT = __EngineEmptyClass(str, 'TEXT')
# result
Success = __EngineEmptyClass(200, 'SUCCESS')
NotFinished = __EngineEmptyClass(None, "NotFinished")
# boolean
NO = False
YES = True
# flags
VERTEX_SHADER = 2
FRAGMENT_SHADER = 4
GEOMETRY_SHADER = 8
COMPUTE_SHADER = 16
