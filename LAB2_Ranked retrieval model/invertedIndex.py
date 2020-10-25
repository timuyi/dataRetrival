import json
#from nltk.stem import WordNetLemmatizerW
import re
from term import Term
import math 

All_item = []

def loadFile(fileName):
    """
        返回列表
    """
    tmp = []
    for line in open(fileName,'r',encoding='utf-8'):
        tmp.append(json.loads(line))
    
    return tmp

def preprocessing(data,StopWords):
    """
    Parameters data
    ----------
    data : string
        数据的预处理  分离单词 去重、单词还原、去除标点
    Returns : pure data
    -------
    """
    words = data['text'].lower()#变小写
    r='[~`!#$%^&*()_+-=|\';":/.,?><~·！@#￥%……&*（）——+-=“：’；、。，？》《{}...]+'#去除标点
    words = re.sub(r,"",words)
    words = words.split(" ")#分离单词
    #去除停用词
    words = [word for word in words if word not in StopWords and word != '']
    #单词还原为原型 通过nltk 先标词形再还原_
    
    #words: [Term(a,n)...]
    ret_words = []
    words.sort()
    num = 0
    old = words[0]
    for i in words:
        if old == i:
            num = num+1
        else:
            ins = Term(old,num)
            ret_words.append(ins)#num就是tf
            old = i
            num=1
    ins = Term(old,num)#补充最后一个
    ret_words.append(ins)
    result = {"id":data['tweetId'],"words":ret_words,"size":len(words)}
    return result
    
    
def invertedIndexDict(data,StopWords):
    """
        {word : list} len:len(list)
    """
    global All_item
    retDict = {}
    for i in range(len(data)):#遍历所有文档
        dat = preprocessing(data[i],StopWords)#数据预处理
        All_item.append(dat)
        for word in dat["words"]:
            postinglist = []
            ins_term = Term(dat["id"],word.fre)
            if(retDict. __contains__(word.word)):
                postinglist = retDict.pop(word.word)#由于是列表因此列表的size就是DF
            postinglist.append(ins_term)
            retDict[word.word] = postinglist
    #smart notation不需要有序
    with open("retDict.txt","w",encoding="utf-8") as f:
        for key,value in retDict.items():
            f.write(key+" : ")
            if len(value) == 0: f.write("None")
            for i in value:
                f.write(str(i)+",")
            f.write("\n")
    return retDict

def tf_process(op,tf_raw):
    ret = []
    if op=="l":
        for i in tf_raw:
            if i==0: ret.append(0)
            else: ret.append(1+math.log10(i))
    elif op=="a":
        ma = max(tf_raw)
        ret = [0.5+0.5*item/ma for item in tf_raw]
    else:
        ret = tf_raw
    return ret

def df_process(op,N,tf_raw):
    ret = []
    if op == "n":
        for i in tf_raw:
            ret.append(1)
    elif op == "t":
        for i in tf_raw:
            if i==0: ret.append(0)
            else: ret.append(math.log10(N/i))#log 是e
    else:
        for i in tf_raw:
            if i==0: ret.append(0)
            else: ret.append(max(0,math.log10((N-i)/i)))
    return ret
def Normalization(op,weight):
    ret = 0
    if op == "n":
        ret = 1
    elif op=="c":
        for item in weight:
            ret += math.pow(item, 2)
        ret = 1/math.sqrt(ret)
    else:
        ret = 0
    return ret

def booleanRetrival(indexDict,StopWords):
    """
        只有在query和文档中都出现过的词才会对当前文档的打分起作用 因此我们可以使用交操作简化
    """
    global All_item
    query = input("Please input the query:")
    words = query.lower()#变小写
    r='[~`!#$%^&*()_+-=|\';":/.,?><~·！@#￥%……&*（）——+-=“：’；、。，？》《{}...]+'#去除标点
    words = re.sub(r,"",words)
    words = words.split(" ")#分离单词
    #去除停用词
    words = [word for word in words if word not in StopWords and word != '']
    if query == "" or len(words) == 0:
        print("未输入查询或查询的内容无效")
        return []
    query_words = []
    words.sort()
    num = 0
    old = words[0]
    for i in words:
        if old == i:
            num = num+1
        else:
            ins = Term(old,num)
            query_words.append(ins)
            old = i
            num=1
    ins = Term(old,num)
    query_words.append(ins)
    
    N = len(All_item)#文档总数 用于求idf
    #df包含单词的文档数 为 len(indexDict[word]
    smart_notation = input("Please input the smart notation:")
    if smart_notation == "":
        smart_notation = "lnc.ltn"
    D_smart_notation = smart_notation.split(".")[0]
    T_smart_notation = smart_notation.split(".")[1]
    #此处假设用户不会输入错误数据
    ans = []#(Term(文档id，score))
    for i in All_item:
        #遍历 所有文档项 {id words size} size为当前文档的单词数
        score = 0
        words = list(set(query_words)|set(i["words"]))#当前文档与查询的单词并集 也就是需要的term项 这里我们只关注单词就好了 tf重新寻找
        df = []
        D_tf_raw = []
        T_tf_raw = []
        D_weight = []
        T_weight = []
        
        #下面这几个实际上不在这里定义也可以
        D_tf_wght = []
        T_tf_wght = []
        D_idf = []
        T_idf = []
        D_n = []
        T_n = []
        
        for j in words:#构建查询与文档的单词向量矩阵
            if indexDict.__contains__(j.word):
                df.append(len(indexDict[j.word]))
            else:
                df.append(0)
            try:
                D_ind = i["words"].index(j)
                D_tf_raw.append(i["words"][D_ind].fre)
            except:
                D_tf_raw.append(0)
            try:
                T_ind = query_words.index(j)
                T_tf_raw.append(query_words[T_ind].fre)
            except:
                T_tf_raw.append(0)
        #文档
        D_tf_wght = tf_process(D_smart_notation[0],D_tf_raw)
        D_idf = df_process(D_smart_notation[1],N,df)
        for j in range(len(D_tf_raw)):
            D_weight.append(D_tf_wght[j]*D_idf[j])
        mul = Normalization(D_smart_notation[2],D_weight)
        D_n = [item*mul for item in D_weight]
        #查询
        T_tf_wght  = tf_process(T_smart_notation[0],T_tf_raw)
        T_idf = df_process(T_smart_notation[1],N,df)
        for j in range(len(T_tf_raw)):
            T_weight.append(T_tf_wght[j]*T_idf[j])
        mul = Normalization(T_smart_notation[2],T_weight)
        T_n = [item*mul for item in T_weight]
        for j in range(len(D_n)):
            score += D_n[j]*T_n[j]
        ans.append({"docId":i["id"],"score":score})
    ans = sorted(ans, key = lambda item: -item['score'])
    return ans
                
if __name__ == "__main__":
    fileName = "./tweets.txt"
    StopWords = []
    StopWords_file = "./StopWords.txt"
    for line in open(StopWords_file,'r',encoding='utf-8'):
        StopWords.append(line.strip('\n\t '))
    data = loadFile(fileName)
    indexDict = invertedIndexDict(data,StopWords)
    ans = booleanRetrival(indexDict,StopWords)
    print("qualified tweets:")
    k = 10
    for i in range(k):
        print(ans[i])
