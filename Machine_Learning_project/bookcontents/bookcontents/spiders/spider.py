import scrapy
import requests
from scrapy.http import TextResponse
import time
import datetime
import re

from bookcontents.items import BookcontentsItem


class Spider(scrapy.Spider):

    name = "bookcontents"
    allow_domain = ["http://www.yes24.co.kr/"]

    def __init__(self):
        self.start_urls = []

        req = requests.get(
            "http://www.yes24.com/24/category/bestseller?CategoryNumber=001001046&sumgb=06&PageNumber=1")
        response = TextResponse(req.url, body=req.text, encoding="utf-8")
        num = response.xpath(
            '//*[@id="bestList"]/div[3]/div[1]/div[1]/p/a[12]/@href').extract()[0][-3:]

        for i in range(1, int(num)):
            url = "http://www.yes24.com/24/category/bestseller?CategoryNumber=001001046&sumgb=06&PageNumber={}".format(
                i)
            self.start_urls.append(url)


    def parse(self, response):
        links = response.xpath(
            '//*[@class="goodsTxtInfo"]/p[1]/a[1]/@href').extract()

        links = ["https://www.yes24.com" + link for link in links]

        for link in links:
            yield scrapy.Request(link, callback=self.get_content)
    
    def get_content(self, response):

        item = BookcontentsItem()
        item['title']  = response.xpath('//*[@class="gd_titArea"]/h2/text()').extract()[0]
        item['img'] = response.xpath('//em[@class="imgBdr"]/img/@src').extract()[0]        
        item['url'] = response.request.url
        
        try:
            description = response.xpath(
                '//*[@class="infoWrap_txtInner"]').extract()
            description = "".join(description)
            description = re.sub('<.+?>', '', description)
            description = re.sub('\r\n', '', description)
            description = description.strip()
            item['description'] = description
        except:
            item['description'] = ''

            
        try :
            text = response.xpath('//*[@id="infoset_inBook"]/div[@class="infoSetCont_wrap"]/div/div[@class="infoWrap_txtInner"]/textarea').extract()
            text = "".join(text)
            text = re.sub('<.+?>', '', text)
            text = re.sub('\r\n','', text) 
            item['text'] = text  
        except:
            item['text'] = ''

        yield item
