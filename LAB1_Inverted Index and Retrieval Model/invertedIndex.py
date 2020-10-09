import json
#from nltk.stem import WordNetLemmatizer
from RPM import RPM
import re

All_item = []

def loadFile(fileName):
    """
        返回列表
    """
    tmp = []
    for line in open(fileName,'r',encoding='utf-8'):
        tmp.append(json.loads(line))
    
    return tmp
"""
def invertedIndexDict(data):
    #   {word,fre : list}
    retDict = {}
    for i in range(len(data)):
        
        tmp = data[i]['text'].split(" ")
        tmp = list(set(tmp))#去重
        for word in tmp:
            key = Term(word = word,fre=1)
            if(retDict. __contains__(key)):
                l = retDict[key]
                l.append(i+1)
                fre = len(l)
                key = Term(word = word,fre=fre)
                retDict[key] = l
            else:
                retDict[key] = [i+1]
        print(retDict)
        break
"""

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
    #单词还原为原型 通过nltk 先标词形再还原
    
    words = list(set(words)) #去重
    result = {"id":data['tweetId'],"words":words}
    return result
    
    
    
    
    
def invertedIndexDict(data,StopWords):
    """
        {word : list} len:len(list)
    """
    retDict = {}
    global All_item
    for i in range(len(data)):#遍历所有文档
        tup = preprocessing(data[i],StopWords)#数据预处理
        for word in tup["words"]:#预处理后同一个文档的单词不重复
            All_item.append(tup["id"])
            if(retDict. __contains__(word)):
                retDict[word].append(tup["id"])
            else:#不存在增加
                retDict[word] = [tup["id"]]
    All_item = list(set(All_item))
    All_item.sort()
    for key,value in retDict.items():
        value.sort()#使有序
    with open("retDict.txt","w",encoding="utf-8") as f:
        for key,value in retDict.items():
            f.write(key+" : "+','.join(value)+'\n\n')
    return retDict

def And(item1,item2):
    """
    求 交集
    Parameters 
    ----------
    item1 : string
    item2 : string
    indexDict : dict 文档倒排索引表
    Returns : list (共同出现的文档id)
    
    list（a,b)求并集 list(set(item1) | set(item2))
    交集 list(set(a)&set(b))
    差集 list(set(a)-set(b)) 在a不在b
    对称差集 list(set(a)^set(b)) a并b-a交b
    
    a = [1,2,3] b = [2,3,4]
    list(set(a)|set(b))  [1, 2, 3, 4]
    list(set(a)&set(b))  [2, 3]
    list(set(a)-set(b))  [1]
    list(set(a)^set(b))  [1, 4]
    -------
    """
    result = []
    result = list(set(item1) & set(item2))
    return result

def Or(item1,item2):
    """
    求 并集
    """
    result = []
    result = list(set(item1) | set(item2))
    return result

def Not(item1,item2):
    """
    在1不在2
    item 可以为 空
    此时去求全集
    """
    global All_item
    item1 = All_item
    result = [id for id in item1 if id not in item2]
    
    return result

def booleanRetrival(indexDict):
    """
        A op B
    """
    global All_item
    op = input("请输入查询语句:")
    op = op.lower()
    op = op.replace("(", "( ")
    op = op.replace(")", " )")
    expression = [ele for ele in op.split(" ") if ele != " " and ele != ""]
    operator = ["and","or","not","(",")"]
    ret = RPM(expression,operator)
    ans = []     
    for i in ret:
        #print("**",ans)
        if i == "and":
            item1 = ans.pop()
            item2 = ans.pop()
            if type(item1)==str: list1 = indexDict[item1]
            else: list1 = item1
            if type(item2)==str: list2 = indexDict[item2]
            else: list2 = item2
            curr_ans = And(list1,list2)
            curr_ans.sort()
            ans.append(curr_ans)
        elif i == "or":
            item1 = ans.pop()
            item2 = ans.pop()
            if type(item1)==str: list1 = indexDict[item1]
            else: list1 = item1
            if type(item2)==str: list2 = indexDict[item2]
            else: list2 = item2
            curr_ans = Or(list1,list2)
            curr_ans.sort()
            ans.append(curr_ans)
        elif i == "not":
            index = ans.pop()
            if type(index) == str :
                if indexDict.__contains__(index):
                    item = indexDict[index]
                else:
                    ans.append(All_item)
                    continue
            else: item = index
            curr_ans = Not(None,item)
            curr_ans.sort()
            ans.append(curr_ans)
        else:
            ans.append(i)
    with open("result.txt","w",encoding = "utf-8") as f:
        f.write(" ".join(ans[0]))
    return ans[0]
                
if __name__ == "__main__":
    fileName = "./tweets.txt"
    StopWords = []
    StopWords_file = "./StopWords.txt"
    for line in open(StopWords_file,'r',encoding='utf-8'):
        StopWords.append(line.strip('\n\t '))
    data = loadFile(fileName)
    indexDict = invertedIndexDict(data,StopWords)
    ans = booleanRetrival(indexDict)
    print("qualified tweets:", ans)
