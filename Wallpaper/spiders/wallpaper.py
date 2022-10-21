import scrapy
import time
from ..items import WallpaperItem


class WallpaperSpider(scrapy.Spider):
    a = 1
    name = 'wallpaper'
    # allowed_domains = ['www.wang.com']
    start_urls = ['https://wallhaven.cc/latest', 'https://wallhaven.cc/toplist', 'https://wallhaven.cc/random']

    def parse(self, response):
        self.a = self.a+1
        print('===='*20, self.a)
        # urls = 'https://wallhaven.cc/latest'
        urls = self.start_urls[0]+f'?page={self.a}'
        selectors = scrapy.Selector(response)
        url = selectors.xpath('//*[@id="thumbs"]/section[@class="thumb-listing-page"]//li/figure/a/@href').extract()
        for i in url:
            yield scrapy.Request(url=i, callback=self.imagemessage)
        # 爬取页数
        if self.a < 20:
            yield scrapy.Request(url=urls, callback=self.parse, dont_filter=True)


    def imagemessage(self, response):
        items = WallpaperItem()
        response = scrapy.Selector(response)
        try:
            # 图片网址
            url = response.xpath('//*[@id="showcase"]/div[@class="scrollbox"]/img/@src').extract()[0]
            # 作者
            author = response.xpath('//div[@class="sidebar-background"]/div[@class="sidebar-content"]/div[@data-'
                                    'storage-id="showcase-info"]/dl/dd[@class="showcase-uploader"]/a[@class='
                                    '"username usergroup-2"]/text()').extract()[0]
            # 图片大小
            size = response.xpath('//div[@class="sidebar-background"]/div[@class="sidebar-content"]/div[@data-'
                                  'storage-id="showcase-info"]/dl/dd[4]/text()').extract()[0]
            # 分辨率
            reslution = response.xpath('//div[@class="sidebar-'
                                       'background"]/div[@class="sidebar-content"]/h3/text()').extract()[0]
            items['url'] = url
            items['author'] = author
            items['size'] = size
            items['reslution'] = reslution
            yield items
        except BaseException as e:
            print('+++'*20, e)



