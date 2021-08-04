import scrapy
from JD.items import JdItem

class A主板Spider(scrapy.Spider):
    name = '主板'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://search.jd.com/search?keyword=%E4%B8%BB%E6%9D%BF&suggest=1.his.0.0&wq=%E4%B8%BB%E6%9D%BF&cid3=681']
    url = 'https://search.jd.com/search?keyword=%E4%B8%BB%E6%9D%BF&suggest=1.his.0.0&wq=%E4%B8%BB%E6%9D%BF&pvid=53acbed8dc824f7e8eaf30f5cb222c3b&cid3=681&cid2=677&page={}'
    page_num = 3
    def parse(self, response):
        li_list = response.xpath('//*[@id="J_goodsList"]/ul/li')
        for li in li_list:
            money = li.xpath('./div/div[2]/strong/i/text()').extract_first()
            name = li.xpath('./div/div[3]/a/em/text()').extract_first()
            shop = li.xpath('./div/div[5]/span/a/text()').extract_first()
            # print(money, name, shop)
            item = JdItem()
            item['money'] = money
            item['name'] = name
            item['shop'] = shop
            yield item
        if self.page_num < 19:
            new_url = self.url.format(self.page_num)
            self.page_num += 2
            yield scrapy.Request(url=new_url, callback=self.parse)


# https://search.jd.com/search?keyword=%E4%B8%BB%E6%9D%BF&suggest=1.his.0.0&wq=%E4%B8%BB%E6%9D%BF&pvid=53acbed8dc824f7e8eaf30f5cb222c3b&cid3=681&cid2=677&page=1&s=1&click=0
# https://search.jd.com/search?keyword=%E4%B8%BB%E6%9D%BF&suggest=1.his.0.0&wq=%E4%B8%BB%E6%9D%BF&pvid=53acbed8dc824f7e8eaf30f5cb222c3b&cid3=681&cid2=677&page=3&s=57&click=0