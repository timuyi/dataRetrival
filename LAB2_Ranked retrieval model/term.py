class Term():
    def __init__(self,word,fre):
        self.word = word
        self.fre = fre
    def __hash__(self):
        return hash(self.word)
    def __eq__(self,other):
        return self.word==other.word
    def __lt__(self,other):
        return self.word<other.word
    def __str__(self):
        return "("+self.word+","+str(self.fre)+")"


if __name__ == "__main__":
    a = Term("apple",4)
    b = Term("apples",5)
    c = Term("aa",5)
    l = [a,b,c]
    l.sort()
    for i in l:
        print(i.word)