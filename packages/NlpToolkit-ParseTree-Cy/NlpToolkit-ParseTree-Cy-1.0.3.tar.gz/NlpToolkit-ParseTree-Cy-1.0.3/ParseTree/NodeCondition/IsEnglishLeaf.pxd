from ParseTree.NodeCondition.IsLeaf cimport IsLeaf
from ParseTree.ParseNode cimport ParseNode


cdef class IsEnglishLeaf(IsLeaf):

    cpdef bint satisfies(self, ParseNode parseNode)
