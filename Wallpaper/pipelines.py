# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from openpyxl import Workbook


class WallpaperPipeline:
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['图片网址', '作者', '大小', '分辨率'])
    def open_spider(self, spider):
        self.file = open('../wallpaper.txt', 'w')

    def process_item(self, item, spider):
        try:
            self.file.write(item['url']+'   '+item['author']+'   '+item['size']+'   '+item['reslution']+'\n')
            self.ws.append([item['url'], item['author'], item['size'], item['reslution']])
        except BaseException as e:
            print(e)
        finally:
            self.wb.save('wallpaper.xlsx')
        return item

    def close_spider(self, spider):
        self.file.close()

