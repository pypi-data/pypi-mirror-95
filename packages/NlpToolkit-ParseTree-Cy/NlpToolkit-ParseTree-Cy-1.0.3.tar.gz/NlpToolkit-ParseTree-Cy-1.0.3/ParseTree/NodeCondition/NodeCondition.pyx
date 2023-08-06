cdef class NodeCondition:

    cpdef bint satisfies(self, ParseNode parseNode):
        pass
