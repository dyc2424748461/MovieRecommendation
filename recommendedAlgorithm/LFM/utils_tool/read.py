#-*- coding:utf-8 -*-
import ast
import os
import django
django.setup()
from movie.models import MovieRatings
from movie.models import CollectMovieDB
def get_item_info():
  '''
  得到item的信息
  :param input_file:
  :return: a dict: key:itemid  value:[title,genre]
  '''
  # if not os.path.exists(input_file):
  #     return {}
  linenum=0
  item_info={}
  data=CollectMovieDB.objects.values('movie_id','title','genres')
  for i in data:
    itemid,title,genre=i['movie_id'],i['title'],ast.literal_eval(i['genres'])
    item_info[itemid]=[title,genre]
  return item_info


def get_ave_score():
    '''
    获取item的平均评分
    :param input_file: user rating file
    :return:
    '''
    # if not os.path.exists(input_file):
    #     return {}
    # linenum=0
    record_dict={}
    score_dict={}
    data = MovieRatings.objects.values_list('user_id','movie_id','rating')
    for i in data:
        userid,itemid,rating=i['user_id'],i['movie_id'],i['rating']
        if itemid not in record_dict:
            record_dict[itemid]=[0,0]
        record_dict[itemid][0]+=1   #记录出现的次数
        record_dict[itemid][1]+=float(rating)

    # fp=open(input_file)
    # for line in fp:
    #     if linenum==0:
    #         linenum+=1
    #         continue
    #     item=line.strip().split(',')
    #     if len(item)<4:
    #         continue;
    #     userid,itemid,rating=item[0],item[1],item[2]
    #     if itemid not in record_dict:
    #         record_dict[itemid]=[0,0]
    #     record_dict[itemid][0]+=1   #记录出现的次数
    #     record_dict[itemid][1]+=float(rating)
    # fp.close()
    for itemid in record_dict:
        score_dict[itemid]=round(record_dict[itemid][1]/record_dict[itemid][0],3)  #精度为3
    return score_dict


def get_train_data():
    '''
    获得训练样本
    :param input_file:
    :return: list[user,item,label]
    '''

    data = MovieRatings.objects.values_list('user_id','movie_id','rating')
    if len(data):
        return []
    score_dict=get_ave_score()
    #负采样要保证正负样本均衡
    pos_dict={}
    neg_dict={}
    train_data=[]
    score_thr=4
    # fp=open(input_file)
    # linenum=0
    # for line in fp:
    #     if linenum==0:
    #         linenum+=1
    #         continue
    #     item=line.strip().split(',')
    #     if len(item)<4:
    #         continue
    for i in data:
        userid,itemid,rating=i['user_id'],i['movie_id'],float(i['rating'])
        if userid not in pos_dict:
            pos_dict[userid]=[]
        if userid not in neg_dict:
            neg_dict[userid]=[]
        if rating>=score_thr:        #大于阙值则看作正样本
            pos_dict[userid].append((itemid,1))
        else:
            score=score_dict.get(itemid,0)
            neg_dict[userid].append((itemid,score))
    # fp.close()
    for userid in pos_dict:
            data_num=min(len(pos_dict[userid]),len(neg_dict.get(userid,[])))
            if data_num>0:
                train_data+=[(userid,temp[0],temp[1])for temp in pos_dict[userid]][:data_num]
            else:
                continue
            #对负样本按照平均评分进行排序，element是[itemid,score]
            sorted_neg_list=sorted(neg_dict[userid],key=lambda element:element[1],reverse=True)[:data_num]
            train_data+=[(userid,temp[0],0)for temp in sorted_neg_list]
    return train_data


if __name__=='__main__':
    '''
    item_dict=get_item_info("../data/movies.csv")
    print(len(item_dict))
    print(item_dict['11'])

    score_dict=get_ave_score("../data/ratings.csv")
    print(len(score_dict))
    print(score_dict['1'])
    '''
    train_data=get_train_data()
    print(len(train_data))
    print(train_data[:-20])