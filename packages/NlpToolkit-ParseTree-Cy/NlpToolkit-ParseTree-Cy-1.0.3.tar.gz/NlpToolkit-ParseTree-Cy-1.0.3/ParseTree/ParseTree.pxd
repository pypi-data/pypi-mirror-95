from ParseTree.ParseNode cimport ParseNode


cdef class ParseTree:

    cdef ParseNode root

    cpdef ParseNode nextLeafNode(self, ParseNode parseNode)
    cpdef ParseNode previousLeafNode(self, ParseNode parseNode)
    cpdef int nodeCountWithMultipleChildren(self)
    cpdef int nodeCount(self)
    cpdef int leafCount(self)
    cpdef bint isFullSentence(self)
    cpdef save(self, str fileName)
    cpdef correctParents(self)
    cpdef removeXNodes(self)
    cpdef ParseNode getRoot(self)
    cpdef int wordCount(self, bint excludeStopWords)
    cpdef list constituentSpanList(self)
