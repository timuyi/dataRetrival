class Term():
    def __init__(self,word,fre):
        self.word = word
        self.fre = fre
    def __hash__(self):
        return hash(self.word)
    def __eq__(self,other):
        return self.word==other.word
