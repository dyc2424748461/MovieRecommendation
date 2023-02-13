#-*- coding:utf-8 -*-

from __future__ import division

import random

import django
django.setup()
import datetime
import os
import operator
from  movie.models import MovieBrows
import sys
# sys.path.append("../")
from recommendedAlgorithm.ContentBased.util import read
class ContentBase:

    def __init__(self,user_id):
        self.user_id = user_id

    max_time=datetime.datetime.now()
    def get_up(self,item_cate):
        '''

        :param item_cate: key:item_id value{cate:ratio}
        :param input_file: 用户浏览记录，其默认评分 为5
        :return:
        '''
        last_brows = 50
        # data = MovieBrows.objects.values_list('user_id','movie_id','brow_time')[:last_brows:-1]
        data = MovieBrows.objects.all().values_list('user_id','movie_id','brow_time').order_by('-brow_time').filter(user_id=self.user_id)
        data = data[:last_brows:]
        if not data.exists():
            now = datetime.datetime.now()
            data = [[self.user_id,1292052,now,],
                    [self.user_id,1293182,now,],
                    [self.user_id,1298624,now,]]
        max_time = data[0][2]

        record={}
        for item in data:
            userid,itemid,rating,timestamp=item[0],item[1],5,item[2]
            if itemid not in item_cate:
                continue
            time_score=self.get_time_score(timestamp)
            print('timeScor'+str(time_score))
            if userid not in record:
                record[userid]={}
            for cate in item_cate[itemid]:
                if cate not in record[userid]:
                    record[userid][cate]=0
                record[userid][cate]+=rating*time_score*item_cate[itemid][cate]  #用户对某一类别的偏好程度

        up={}  #保存结果
        topK=3
        for userid in record:
            if userid not in up:
                up[userid]=[]
            total_score=0
            for instance in sorted(record[userid].items(),key=operator.itemgetter(1),reverse=True)[:topK]:
                up[userid].append((instance[0],instance[1]))
                total_score+=instance[1]    #用来对类别分数归一化
            for index in range(len(up[userid])):
                up[userid][index]=(up[userid][index][0],round(up[userid][index][1]/total_score,3))
        return up

    def get_time_score(self,timestamp):
        '''

        :param timestamp: 时间戳
        :return: 时间的得分
        '''
        #已知最大时间戳是1537799250
        # max_timestamp=1537799250
        max_timestamp = self.max_time
        total_sec=24*60*60
        delta=(max_timestamp-timestamp)/total_sec  #时间越近，即差距越小，分数越大
        t = 1/(1+delta.seconds)
        return (1/(1+delta.seconds))*1000

    def recom(self,cate_item_sort,up,userid,topK=5):
        '''

        :param cate_item_sort:  类别中item的倒排结果
        :param up: 用户对类别的偏好程度
        :param userid:
        :param topK:
        :return:
        '''
        topN = 100
        if userid not in up:
            return{}
        recom_result={}
        if userid not in recom_result:
            recom_result[userid]=[]
        for instance in up[userid]:
            cate=instance[0]
            ratio=instance[1]
            num=int(topK*ratio)+1
            if cate not in cate_item_sort:
                continue
            recom_list=random.sample(cate_item_sort[cate][:topN],num)
            print('in+_'+str(recom_list))
            recom_result[userid]+=recom_list
        recom_result[userid] = recom_result[userid][:topK]
        return recom_result

    def run_main(self,):
        ave_score=read.get_ave_score()
        item_cate,cate_item_sort=read.get_item_cate(ave_score)
        #print(item_cate)
        #print(cate_item_sort)
        up=self.get_up(item_cate)
        print(len(up))
        print(self.recom(cate_item_sort,up,self.user_id))
        return self.recom(cate_item_sort,up,self.user_id)

if __name__=="__main__":
    ContentBase(2).run_main()