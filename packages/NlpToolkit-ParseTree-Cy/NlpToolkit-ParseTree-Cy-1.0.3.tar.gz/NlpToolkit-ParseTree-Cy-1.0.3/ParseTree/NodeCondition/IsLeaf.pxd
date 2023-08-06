from ParseTree.NodeCondition.NodeCondition cimport NodeCondition
from ParseTree.ParseNode cimport ParseNode


cdef class IsLeaf(NodeCondition):

    cpdef bint satisfies(self, ParseNode parseNode)
