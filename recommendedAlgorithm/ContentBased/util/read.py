#-*-coding:utf-8 -*-

from __future__ import division
import os
import operator
import ast
import django
django.setup()
from movie.models import MovieRatingDB
from movie.models import CollectMovieDB
def get_ave_score():
    '''
    得到item的平均评分
    :param input_file:
    :return: dict key:itemid  value:score
    '''
    ave_score={}
    # if not os.path.exists(input_file):
    #     return{}
    # linenum=0
    # record={}
    # ave_score={}
    # fp=open(input_file)
    # for line in fp:
    #     if linenum==0:
    #         linenum+=1
    #         continue
    #     item=line.strip().split(',')
    #     if len(item)<4:
    #         continue
    #     userid,itemid,rating=item[0],item[1],float(item[2])
    #     if itemid not in record:
    #         record[itemid]=[0,0]
    #     record[itemid][0]+=rating   #评分和
    #     record[itemid][1]+=1    #评分次数
    # fp.close()
    # for itemid in record:
    #     ave_score[itemid]=round(record[itemid][0]/record[itemid][1],3)
    data=MovieRatingDB.objects.values('movie_id_id','rating')
    for line in data:
        ave_score[line['movie_id_id']] = float(line['rating'])
    return ave_score

def get_item_cate(ave_score):
    '''
    获取item的类别，以及每个类别下的所有item，这些item按照score倒排序
    :param ave_score:
    :param input_file:
    :return:   dict1: key:item value:category
               dict2: key:category value:items
    '''
    # 获取数据库中电影的信息
    data = CollectMovieDB.objects.values_list('movie_id','genres','content_base')
    if not len(data):
        return {},{}
    linenum=0
    item_cate={}  #记录item的类别
    record={}
    cate_item_sort={} #记录每一类别中前topk的items

    for line in data:
        item=line
        # if len(item)<3:
        #     continue
        itemid=item[0]
        cate_str=ast.literal_eval(item[1])   + ast.literal_eval(item[2]) #得到类别
        cate_list=cate_str
        ratio=round(1/len(cate_list),3)   #类别出现的概率等分
        if itemid not in item_cate:
            item_cate[itemid]={}   #字典，类别：得分
        for cate in cate_list:
            item_cate[itemid][cate]=ratio
    topK=100
    for itemid in item_cate:
        for cate in item_cate[itemid]:
            if cate not in record:
                record[cate]={}
            itemid_rating_score=ave_score.get(itemid,0)    #如果指定itemid不存在，则返回0
            record[cate][itemid]=itemid_rating_score
    for cate in record:
        if cate not in cate_item_sort:
            cate_item_sort[cate]=[]     #每个cate保存一个列表
        for instance in sorted(record[cate].items(),key=operator.itemgetter(1),reverse=True)[:topK]:
            cate_item_sort[cate].append(instance[0])
    return item_cate,cate_item_sort


if __name__=="__main__":
    ave_score=get_ave_score() # 修改为使用数据库
    print(len(ave_score))
    item_cate,cate_item_sort=get_item_cate(ave_score) # 修改为使用数据库
    print (item_cate['1'])
    print(cate_item_sort)