from ParseTree.ParseTree cimport ParseTree


cdef class TreeBank:

    cdef list parseTrees

    cpdef int size(self)
    cpdef int wordCount(self, bint excludeStopWords)
    cpdef ParseTree get(self, int index)
