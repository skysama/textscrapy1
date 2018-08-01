# -*- coding: utf-8 -*-
import scrapy
from textscrapy.items import TextscrapyItem


class VmovieSpider(scrapy.Spider):
    name = 'vmovie'
    allowed_domains = ['vmovier.com']
    start_urls = ['http://www.vmovier.com/']

    def parse(self, response):
        """

        :type response: object
        """
        # moivelist = response.xpath("//li[@class='clearfix']")
        moivelist = response.xpath("//*[@class='clearfix']")
        for m in moivelist:
            item = TextscrapyItem()
            #  xpath取出来的是个数组 所以要取第一个
            item['cover'] = m.xpath('./a/img/@src')[0].extract()
            item['title'] = m.xpath('./a/@title')[0].extract()
            item['dec'] = m.xpath("./div/div[@class='index-intro']/a/text()")[0].extract()
            print(item)


            # 提前
            urlitem = m.xpath("./div/h1/a/@href")[0].extract()
            url = response.urljoin(urlitem)

            yield scrapy.Request(url, callback=self.parse_movie, meta={
                'cover':item['cover'],
                'title':item['title'],
                'dec':item['dec'],
            } )

            # // *[ @ id = "post-list"] / li[1] / div / h1 / a[2]



    def parse_movie(self, response):
        item = TextscrapyItem()
        item['cover'] = response.meta['cover']
        item['title'] = response.meta['title']
        item['dec'] = response.meta['dec']
        item['playUrl'] = response.xpath("//div[@class='p00b204e980']/p/iframe/@src")[0].extract()
        # // *[ @ id = "player"]
        # // *[ @ id = "main-container"] / div[1] / div[1] / div[4] / p[1] / iframe
        yield item





