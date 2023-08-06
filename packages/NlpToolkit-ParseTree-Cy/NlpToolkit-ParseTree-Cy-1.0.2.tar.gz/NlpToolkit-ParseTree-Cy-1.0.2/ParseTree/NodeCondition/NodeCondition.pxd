from ParseTree.ParseNode cimport ParseNode


cdef class NodeCondition:

    cpdef bint satisfies(self, ParseNode parseNode)
