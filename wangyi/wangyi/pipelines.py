# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class WangyiPipeline:
    fp = None
    def open_spider(self,spider):
        print('start')
        self.fp = open('网易新闻.txt', mode='w', encoding='utf-8')
    def close_spider(self, spider):
        print('over')
        self.fp.close()



    def process_item(self, item, spider):
        self.fp.write(item['title']+"\n"+item['content']+'\n')
        return item
