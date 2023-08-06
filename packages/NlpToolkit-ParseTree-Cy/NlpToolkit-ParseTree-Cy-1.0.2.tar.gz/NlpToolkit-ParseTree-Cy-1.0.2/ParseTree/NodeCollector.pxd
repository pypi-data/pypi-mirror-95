from ParseTree.NodeCondition.NodeCondition cimport NodeCondition
from ParseTree.ParseNode cimport ParseNode


cdef class NodeCollector:

    cdef NodeCondition condition
    cdef ParseNode rootNode

    cpdef __collectNodes(self, ParseNode parseNode, list collected)
    cpdef list collect(self)
