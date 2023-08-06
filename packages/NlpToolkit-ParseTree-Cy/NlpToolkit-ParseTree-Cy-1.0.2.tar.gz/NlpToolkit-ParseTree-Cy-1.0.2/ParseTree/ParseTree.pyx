from ParseTree.NodeCollector cimport NodeCollector
from ParseTree.NodeCondition.IsEnglishLeaf cimport IsEnglishLeaf


cdef class ParseTree:

    sentenceLabels = ["SINV", "SBARQ", "SBAR", "SQ", "S"]

    def __init__(self, rootOrFileName=None):
        """
        Basic constructor for a ParseTree. Initializes the root node with the input.

        PARAMETERS
        ----------
        rootOrFileName : ParseNode
            Root node of the tree
        """
        cdef str line
        if isinstance(rootOrFileName, ParseNode):
            self.root = rootOrFileName
        elif isinstance(rootOrFileName, str):
            inputFile = open(rootOrFileName, "r", encoding="utf8")
            line = inputFile.readline()
            if "(" in line and ")" in line:
                line = line[line.index("(") + 1:line.rindex(")")].strip()
                self.root = ParseNode(None, line, False)
            else:
                self.root = None
            inputFile.close()

    cpdef ParseNode nextLeafNode(self, ParseNode parseNode):
        """
        Gets the next leaf node after the given leaf node in the ParseTree.

        PARAMETERS
        ----------
        parseNode : ParseNode
            ParseNode for which next node is calculated.

        RETURNS
        -------
        ParseNode
            Next leaf node after the given leaf node.
        """
        cdef NodeCollector nodeCollector
        cdef list leafList
        cdef int i
        nodeCollector = NodeCollector(self.root, IsEnglishLeaf())
        leafList = nodeCollector.collect()
        for i in range(len(leafList) - 1):
            if leafList[i] == parseNode:
                return leafList[i + 1]
        return None

    cpdef ParseNode previousLeafNode(self, ParseNode parseNode):
        """
        Gets the previous leaf node before the given leaf node in the ParseTree.

        PARAMETERS
        ----------
        parseNode : ParseNode
            ParseNode for which previous node is calculated.

        RETURNS
        -------
        ParseNode
            Previous leaf node before the given leaf node.
        """
        cdef NodeCollector nodeCollector
        cdef list leafList
        cdef int i
        nodeCollector = NodeCollector(self.root, IsEnglishLeaf())
        leafList = nodeCollector.collect()
        for i in range(1, len(leafList)):
            if leafList[i] == parseNode:
                return leafList[i - 1]
        return None

    cpdef int nodeCountWithMultipleChildren(self):
        """
        Calls recursive method to calculate the number of all nodes, which have more than one children.

        RETURNS
        -------
        int
            Number of all nodes, which have more than one children.
        """
        return self.root.nodeCountWithMultipleChildren()

    cpdef int nodeCount(self):
        """
        Calls recursive method to calculate the number of all nodes tree.

        RETURNS
        -------
        int
            Number of all nodes in the tree.
        """
        return self.root.nodeCount()

    cpdef int leafCount(self):
        """
        Calls recursive method to calculate the number of all leaf nodes in the tree.

        RETURNS
        -------
        int
            Number of all leaf nodes in the tree.
        """
        return self.root.leafCount()

    cpdef bint isFullSentence(self):
        if self.root is not None and self.root.data.getName() in self.sentenceLabels:
            return True
        return False

    cpdef save(self, str fileName):
        """
        Saves the tree into the file with the given file name. The output file only contains one line representing tree.

        PARAMETERS
        ----------
        fileName : str
            Output file name
        """
        outputFile = open(fileName, "w", encoding="utf8")
        outputFile.write("( " + self.__str__() + " )\n")
        outputFile.close()

    cpdef correctParents(self):
        """
        Calls recursive method to restore the parents of all nodes in the tree.
        """
        self.root.correctParents()

    cpdef removeXNodes(self):
        """
        Calls recursive method to remove all nodes starting with the symbol X. If the node is removed, its children are
        connected to the next sibling of the deleted node.
        """
        self.root.removeXNodes()

    cpdef ParseNode getRoot(self):
        """
        Accessor method for the root node.

        RETURNS
        -------
        ParseNode
            Root node
        """
        return self.root

    def __str__(self) -> str:
        """
        Calls recursive function to convert the tree to a string.

        RETURNS
        -------
        str
            A string which contains all words in the tree.
        """
        return self.root.__str__()

    cpdef int wordCount(self, bint excludeStopWords):
        """
        Calls recursive function to count the number of words in the tree.

        PARAMETERS
        ----------
        excludeStopWords : bool
            If true, stop words are not counted.

        RETURNS
        -------
        int
            Number of words in the tree.
        """
        return self.root.wordCount(excludeStopWords)

    cpdef list constituentSpanList(self):
        """
        Generates a list of constituents in the parse tree and their spans.

        RETURNS
        -------
        list
            A list of constituents in the parse tree and their spans.
        """
        cdef list result
        result = []
        self.root.constituentSpanList(1, result)
        return result
