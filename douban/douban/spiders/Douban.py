# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanSpider(scrapy.Spider):
    name = 'Douban'
    allowed_domains = ['movie.douban.com']
    url = 'https://movie.douban.com/top250?start='
    start = 0
    end = '&filter='
    start_urls = [url + str(start) + end]

    def parse(self, response):
        item = DoubanItem()
        for each in response.xpath('//div[@class="info"]'):
            title = each.xpath('div[@class="hd"]/a/span[@class="title"]/text()').extract()
            score = each.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
            content = each.xpath('div[@class="bd"]/p/text()').extract()
            info = each.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            item['title'] = title[0]
            item['score'] = score[0]
            item['content'] = content[0].replace(" ", "").lstrip()
            if info:
                item['info'] = info[0]
            else:
                item['info'] = ''

            yield item

        if self.start <= 250:
            self.start += 25
            yield scrapy.Request(self.url+str(self.start)+self.end, callback=self.parse)