import scrapy
from selenium import webdriver
from wangyi.items import WangyiItem

class WangyinetSpider(scrapy.Spider):
    name = 'wangyinet'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://news.163.com/']
    model_urls = []     # 每一个板块对应的url

    # 实例化了一个全局的浏览器对象
    bro = webdriver.Chrome(executable_path='./chromedriver.exe')

    # 数据解析：每一个板块对应的url
    def parse(self, response):
        li_list = response.xpath('//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        # print(li_list)
        indexs = [2,3, 5]
        for index in indexs:
            model_li = li_list[index]
            model_url = model_li.xpath('./a/@href').extract_first()
            # print(model_url)
            self.model_urls.append(model_url)
        # 对每一个板块的url发起请求
        for url in self.model_urls:
            yield scrapy.Request(url=url, callback=self.parse_model)
    # 数据解析:新闻标题＋新闻详情页的url（动态加载）
    def parse_model(self,response):
        # 可以使用中间件将不满足需求的相应对象中的相应数据篡改成包含了动态加载数据的相应数据，将其编程满足需求的响应对象
        div_list = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div[1]/div/ul/li/div/div')
        for div in div_list:
            titile = div.xpath('./div/div[1]/h3/a/text()').extract_first()
            new_detail_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()
            item = WangyiItem()
            item['title'] = titile

            if titile==None:
                continue
            # print(titile, new_detail_url)
            yield scrapy.Request(url=new_detail_url, callback=self.parse_new_detail, meta={'item':item})

    def parse_new_detail(self,response):
        item = response.meta['item']
        content = response.xpath('//*[@id="content"]/div[2]/p/text()').extract()
        content = ''.join(content)
        item['content'] = content
        yield item

    # 爬虫类父类的方法，该方法实在爬虫结束最后一刻执行
    def closed(self, spider):
        self.bro.quit()




