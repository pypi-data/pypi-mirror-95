from ParseTree.Symbol cimport Symbol


cdef class ConstituentSpan:

    cdef Symbol constituent
    cdef int start
    cdef int end

    cpdef int getStart(self)
    cpdef int getEnd(self)
    cpdef Symbol getConstituent(self)
