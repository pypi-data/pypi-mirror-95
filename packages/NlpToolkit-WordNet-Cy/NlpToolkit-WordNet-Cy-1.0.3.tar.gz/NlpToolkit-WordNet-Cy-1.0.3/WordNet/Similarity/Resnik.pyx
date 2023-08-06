from WordNet.Similarity.ICSimilarity cimport ICSimilarity
from WordNet.SynSet cimport SynSet
from WordNet.WordNet cimport WordNet


cdef class Resnik(ICSimilarity):

    def __init__(self, wordNet: WordNet, informationContents: dict):
        super().__init__(wordNet, informationContents)

    cpdef double computeSimilarity(self, SynSet synSet1, SynSet synSet2):
        cdef list pathToRootOfSynSet1
        cdef list pathToRootOfSynSet2
        cdef str LCSid
        pathToRootOfSynSet1 = self.wordNet.findPathToRoot(synSet1)
        pathToRootOfSynSet2 = self.wordNet.findPathToRoot(synSet2)
        LCSid = self.wordNet.findLCSid(pathToRootOfSynSet1, pathToRootOfSynSet2)
        return self.informationContents[LCSid]
