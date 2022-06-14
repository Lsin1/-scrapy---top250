import re

import scrapy
from dbtop250.items import Dbtop250Item     #调用items
from scrapy.http import Request

class StockSpider(scrapy.Spider):
    name = 'stock'      #定义爬虫名称
    allowed_domains = ['movie.douban.com']  #定义爬虫域
    start_urls = ['https://movie.douban.com/top250?start=0&filter=']   #值需修改为需要爬取的链接
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                     "537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    custom_settings = {
        'CONCURRENT_REQUEST_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1
    }
    def start_requests(self):
        for url in self.start_urls:
            # HTTP request
            i=0
            while True:
                yield Request(
                    url=url,
                    headers=self.headers,
                    callback=self.parse
                )
                i+= 25  #每次爬取25条
                if i == 250:
                    break   #top250当然只有250个啦
                url = f'https://movie.douban.com/top250?start={i}&filter='

    # 定义开始爬虫链接，可以多个也可以一个
    def parse(self, response):  #撰写爬虫逻辑
        '''
        #将爬取的html输出成一个txt 测试
        print('运行中')
        f = open('top250.txt', 'wb')
        f.write(response.body)
        f.close()
        '''
        item = Dbtop250Item()
        for k in range(1,26):
            item['movie_ranking'] = response.xpath(f'//*[@id="content"]/div/div[1]'
                                                   f'/ol/li[{k}]/div/div[1]/em/text()').extract()[0]
            item['movie_title'] = response.xpath(f'//*[@id="content"]/div/div[1]/ol/li[{k}]/'
                                                 'div/div[2]/div[1]/a/span[1]/text()').extract()[0]
            #经过结果分析需使用正则正确取值
            #临时使用变量存值   内容包括导演、主演、年份、上映城市、电影类别
            tem_text = response.xpath(f'//*[@id="content"]/div/div[1]/'
                                      f'ol/li[{k}]/div/div[2]/div[2]/p[1]/text()').extract()
            if '主演' in tem_text[0]:
                #导演
                item['movie_director'] = re.findall(r'(?<=导演:)[\S\s]*(?=主演)', tem_text[0])[0]\
                    .strip().replace('\xa0', '')
            else:
                item['movie_director'] = re.findall(r'(?<=导演:)[\S\s]*', tem_text[0])[0].strip().replace('\xa0', '')

            item['movie_lead'] = '导演过多主演无法正常显示' #可能会因为导演过多导致主演不显示
            if '主演' in tem_text[0]:
                #部分主演
                item['movie_lead'] = re.findall(r'(?<=主演)[\S\s]*', tem_text[0])[0].strip().replace(':', '')

            item['movie_years'] = tem_text[1].strip().split('/')[0].strip()     #特殊格式去掉
            item['movie_city'] = tem_text[1].strip().split('/')[1].strip()
            item['movie_type'] = tem_text[1].strip().split('/')[2].strip()

            item['movie_score'] = response.xpath(f'//*[@id="content"]/div/div[1]/ol/li[{k}]/'
                                                 f'div/div[2]/div[2]/div/span[2]/text()').extract()[0]
            item['movie_evaluation_people'] = response.xpath(f'//*[@id="content"]/div/div[1]'
                                                             f'/ol/li[{k}]/div/div[2]/div[2]/div/span[4]/text()').extract()[0]
            try:
                item['movie_synopsis'] = response.xpath(f'//*[@id="content"]/div/div[1]/ol/li[{k}]'
                                                        f'/div/div[2]/div[2]/p[2]/span/text()').extract()[0]
            except:
                item['movie_synopsis'] = '' #运行发现可能为空 需抛出

            ifplay = response.xpath(f'//*[@id="content"]/div/div[1]/ol/li[{k}]/div/div[2]/div[1]').extract()[0]
            item['movie_ifplay'] = '不可播放'
            if '可播放' in ifplay:
                item['movie_ifplay'] = '可播放'
            item['movie_web'] = response.xpath(f'//*[@id="content"]/div/div[1]/'
                                               f'ol/li[{k}]/div/div[2]/div[1]/a/@href').extract()[0]
            print(item)
            yield item  #映射
        return item
        pass
