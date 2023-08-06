from ParseTree.Symbol cimport Symbol


cdef class ParseNode:

    cdef list children
    cdef ParseNode parent
    cdef Symbol data

    cpdef ParseNode __searchHeadChild(self, list priorityList, object direction, bint defaultCase)
    cpdef ParseNode headLeaf(self)
    cpdef ParseNode headChild(self)
    cpdef addChild(self, ParseNode child, index=*)
    cpdef correctParents(self)
    cpdef removeXNodes(self)
    cpdef setChild(self, int index, ParseNode child)
    cpdef removeChild(self, ParseNode child)
    cpdef int leafCount(self)
    cpdef int nodeCount(self)
    cpdef int nodeCountWithMultipleChildren(self)
    cpdef int numberOfChildren(self)
    cpdef ParseNode getChild(self, int i)
    cpdef ParseNode firstChild(self)
    cpdef ParseNode lastChild(self)
    cpdef bint isLastChild(self, ParseNode child)
    cpdef int getChildIndex(self, ParseNode child)
    cpdef bint isDescendant(self, ParseNode node)
    cpdef ParseNode previousSibling(self)
    cpdef ParseNode nextSibling(self)
    cpdef ParseNode getParent(self)
    cpdef Symbol getData(self)
    cpdef setData(self, Symbol data)
    cpdef int wordCount(self, bint excludeStopWords)
    cpdef bint isLeaf(self)
    cpdef bint isDummyNode(self)
    cpdef moveLeft(self, ParseNode node)
    cpdef moveRight(self, ParseNode node)
    cpdef str ancestorString(self)
    cpdef constituentSpanList(self, int startIndex, list constituentSpanList)