class Similarity:
    """
    Class to maintain the similarity matrix and the business ID
    mapping to indices
    """
    def __init__(self, matrix, mapping):
        self.matrix = matrix
        self.mapping = mapping
    def getSimilarity(self, id1, id2):
        if(type(id1)==type('abc')and type(id2)==type('abc')):
            return self.matrix[self.mapping[id1]][self.mapping[id2]]
        try:
            return self.matrix[int(id1)][int(id2)]
        except:
            return None
