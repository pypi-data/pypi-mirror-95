cdef class ConstituentSpan:

    def __init__(self, constituent: Symbol, start: int, end: int):
        self.constituent = constituent
        self.start = start
        self.end = end

    cpdef int getStart(self):
        return self.start

    cpdef int getEnd(self):
        return self.end

    cpdef Symbol getConstituent(self):
        return self.constituent