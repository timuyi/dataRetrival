import math

def generate_tweetid_gain(file_name):
    qrels_dict = {}
    with open(file_name, 'r', errors='ignore') as f:
        for line in f:
            ele = line.strip().split(' ')
            if ele[0] not in qrels_dict:
                qrels_dict[ele[0]] = {}
            # here we want the gain of doc_id in qrels_dict > 0,
            # so it's sorted values can be IDCG groundtruth
            if int(ele[3]) > 0:
                qrels_dict[ele[0]][ele[2]] = int(ele[3])
    return qrels_dict

def read_tweetid_test(file_name):
    # input file format
    # query_id doc_id
    # query_id doc_id
    # query_id doc_id
    # ...
    test_dict = {}
    with open(file_name, 'r', errors='ignore') as f:
        for line in f:
            ele = line.strip().split(' ')
            if ele[0] not in test_dict:
                test_dict[ele[0]] = []
            test_dict[ele[0]].append(ele[1])
    return test_dict

def MAP_eval(qrels_dict, test_dict, k = 100):
    #Mean Average Precision
    Aprecision = []
    for key,value in test_dict.items():
        # 0~min(k,len(test_dict)) ap = sum(每个相关文档的precision)/相关文档数量  每个相关文档的precision使用的ranklist为test_dict[0,目前相关文档]
        sum_P = 0
        relevant_list = [item for item in qrels_dict[key] if qrels_dict[key][item]!=0]
        n = len([item for item in value[0:k] if item in relevant_list])#要注意我们只需要关注前k个
        for i in range(min(len(value),k)):
            rank_list = []
            if value[i] in relevant_list:
                #只关注相关文档的 precision就可以了
                rank_list = value[0:i+1]
                rank_relevant = len([item for item in rank_list if item in relevant_list])
                sum_P += rank_relevant/(i+1)       
        Aprecision.append({"id":key,"precision":sum_P/n})
        """
        unrank_relevant = len([item for item in un_rank_list if qrels_dict[key].__contains__(item)])
        recall = rank_relevant/(unrank_relevant + rank_relevant)"""
    MAP = 0
    for i in Aprecision:
        MAP += i["precision"]
    MAP /= len(Aprecision)
    return MAP

def MRR_eval(qrels_dict, test_dict, k = 100):
    #Mean Reciprocal Rank  平均倒数排名
    RR_list = []
    for key,value in test_dict.items():
        # 0~min(k,len(test_dict)) ap = sum(每个相关文档的precision)/相关文档数量  每个相关文档的precision使用的ranklist为test_dict[0,目前相关文档]
        RR = 0
        relevant_list = [item for item in qrels_dict[key] if qrels_dict[key][item]!=0]
        for i in range(min(len(value),k)):
            if value[i] in relevant_list:
                RR = 1/(i+1)
                break;
        RR_list.append({"id":key,"score":RR})
    MRR = 0
    for i in RR_list:
        MRR += i["score"]
    MRR /= len(RR_list)
    return MRR
    
def NDCG_eval(qrels_dict, test_dict, k = 100):
    #Normalized Discounted Comulative Gain
    NDCG_score = 0
    NDCG = []
    for key,value in test_dict.items():
        # 0~min(k,len(test_dict)) ap = sum(每个相关文档的precision)/相关文档数量  每个相关文档的precision使用的ranklist为test_dict[0,目前相关文档]
        relevant_list = [item for item in qrels_dict[key] if qrels_dict[key][item]!=0]
        #DCG
        DCG = 0
        for i in range(min(len(value),k)):
            rel = 0
            if qrels_dict[key].__contains__(value[i]):
                rel = qrels_dict[key][value[i]]
            if i==0 : DCG+=rel
            elif rel != 0:
                DCG += rel/math.log(i+1,2)
            
        #IDCG  我们只需要关注相关的就可以了
        IDCG = 0
        new_value = sorted([item for item in value if item in relevant_list],key = lambda x:-qrels_dict[key][x])
        for i in range(min(len(new_value),k)):
            rel = 0
            if qrels_dict[key].__contains__(new_value[i]):#其实一定在 因为我们只关注相关的文档
                rel = qrels_dict[key][new_value[i]]
            if i==0 : DCG+=rel
            elif rel != 0:
                IDCG += rel/math.log(i+1,2)
        try:
            score = DCG/IDCG
        except:#当idcg为0
            score = 0
        NDCG.append({"id":key,"score":score})
    for i in NDCG:
        NDCG_score += i["score"]
    NDCG_score /= len(NDCG)
    return NDCG_score


def evaluation():
    k = 100
    # query relevance file
    file_qrels_path = 'qrels.txt'
    # qrels_dict = {query_id:{doc_id:gain, doc_id:gain, ...}, ...}
    qrels_dict = generate_tweetid_gain(file_qrels_path)
    # ur result, format is in function read_tweetid_test, or u can write by ur own
    file_test_path = 'result.txt'
    # test_dict = {query_id:[doc_id, doc_id, ...], ...}
    test_dict = read_tweetid_test(file_test_path)
    print(test_dict)
    MAP = MAP_eval(qrels_dict, test_dict, k)
    print('MAP', ' = ', MAP, sep='')
    MRR = MRR_eval(qrels_dict, test_dict, k)
    print('MRR', ' = ', MRR, sep='')
    NDCG = NDCG_eval(qrels_dict, test_dict, k)
    print('NDCG', ' = ', NDCG, sep='')

if __name__ == '__main__':
    evaluation()
