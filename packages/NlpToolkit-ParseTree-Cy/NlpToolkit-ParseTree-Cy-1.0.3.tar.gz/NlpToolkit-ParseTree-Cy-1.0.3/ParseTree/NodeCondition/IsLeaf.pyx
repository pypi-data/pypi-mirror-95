cdef class IsLeaf(NodeCondition):

    """
    Implemented node condition for the leaf node. If a node has no children it is a leaf node.

    PARAMETERS
    ----------
    parseNode : ParseNode
        Checked node.

    RETURNS
    -------
    bool
        True if the input node is a leaf node, false otherwise.
    """
    cpdef bint satisfies(self, ParseNode parseNode):
        return parseNode.numberOfChildren() == 0
