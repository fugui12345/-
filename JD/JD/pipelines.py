# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class JdPipeline:
    fp = None
    def open_spider(self, spider):
        print('爬虫开始')
        self.fp = open('JD.csv', mode='w', encoding='utf-8')
    def close_spider(self, spider):
        print('爬虫结束')
        self.fp.close()

    def process_item(self, item, spider):
        # print(item['money'], item['name'], item['shop'])
        self.fp.write(item['money']+ ',' +item['name']+','+ item['shop']+'\n')
        return item
