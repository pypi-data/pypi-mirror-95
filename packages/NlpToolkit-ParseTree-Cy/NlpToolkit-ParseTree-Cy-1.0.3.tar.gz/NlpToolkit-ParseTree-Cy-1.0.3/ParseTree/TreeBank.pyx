import os
import re


cdef class TreeBank:

    def __init__(self, folder: str = None, pattern: str = None):
        """
        A constructor of TreeBank class which reads all ParseTree files with the file name satisfying the
        given pattern inside the given folder. For each file inside that folder, the constructor creates a ParseTree
        and puts in inside the list parseTrees.

        PARAMETERS
        ----------
        folder : str
            Folder where all parseTrees reside.
        pattern : str
            File pattern such as "." ".train" ".test".
        """
        self.parseTrees = []
        if str is not None:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    fileName = os.path.join(root, file)
                    if (pattern is None or pattern in fileName) and re.match("\\d+\\.", file):
                        parseTree = ParseTree(fileName)
                        self.parseTrees.append(parseTree)

    cpdef int size(self):
        """
        Returns number of trees in the TreeBank.

        RETURNS
        -------
        int
            Number of trees in the TreeBank.
        """
        return len(self.parseTrees)

    cpdef int wordCount(self, bint excludeStopWords):
        """
        Returns number of words in the parseTrees in the TreeBank. If excludeStopWords is true, stop words are not
        counted.

        PARAMETERS
        ----------
        excludeStopWords : bool
            If true, stop words are not included in the count process.

        RETURNS
        -------
        int
            Number of all words in all parseTrees in the TreeBank.
        """
        cdef int total
        cdef ParseTree tree
        total = 0
        for tree in self.parseTrees:
            total += tree.wordCount(excludeStopWords)
        return total

    cpdef ParseTree get(self, int index):
        """
        Accessor for a single ParseTree.

        PARAMETERS
        ----------
        index : int
            Index of the parseTree.

        RETURNS
        -------
        ParseTree
            The ParseTree at the given index.
        """
        return self.parseTrees[index]
