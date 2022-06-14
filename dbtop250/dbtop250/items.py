# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Dbtop250Item(scrapy.Item):    #建立相应的字段
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_title = scrapy.Field()  #电影标题
    movie_director = scrapy.Field()  #电影导演
    movie_lead = scrapy.Field()     #部分主演
    movie_years = scrapy.Field()     #电影上映年份
    movie_city = scrapy.Field()     #电影上映城市
    movie_type = scrapy.Field()     #电影类别
    movie_score = scrapy.Field()    #电影评分
    movie_evaluation_people = scrapy.Field()   #电影评价人数
    movie_synopsis = scrapy.Field()         #电影简介
    movie_ifplay = scrapy.Field()       #电影是否可以播放
    movie_web = scrapy.Field()      #电影详情网址
    movie_ranking = scrapy.Field()  #排名
