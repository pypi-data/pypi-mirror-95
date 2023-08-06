from Dictionary.Word cimport Word


cdef class Symbol(Word):

    cpdef bint isVP(self)
    cpdef bint isTerminal(self)
    cpdef bint isChunkLabel(self)
    cpdef Symbol trimSymbol(self)