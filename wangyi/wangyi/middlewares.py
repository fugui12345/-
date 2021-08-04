# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from time import sleep
from scrapy.http import HtmlResponse    # scrapy封装好的响应类

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

class WangyiDownloaderMiddleware:

    def process_request(self, request, spider):

        return None
    # 拦截所有响应对象
    # 整个工程发起的请求：1+5+n，相应也会有1+5+n个响应对象
    # 只有指定的五个响应对象是不满足需求的
    # 只将不满足需求的五个响应对象的相应数据进行篡改
    def process_response(self, request, response, spider):
        # 将拦截到的所有的相应对象中指定的五个响应对象找出
        if request.url in spider.model_urls:
            bro = spider.bro
            # response表示的事指定的不满足需求的响应对象
            # 篡改相应数据：首先获取满足需求的响应数据，将其篡改到响应对象中即可
            # 满足需求的响应数据可以通过selenium获取
            bro.get(request.url) # 使用selenium对五个板块发请求
            sleep(2)
            bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')     # 下拉
            sleep(1)
            # 捕获到了板块页面中加载的全部数据（包含了动态加载的数据）
            page_text = bro.page_source
            # response = page_text
            # return response     # 5
            # 返回了一个新的响应对象，新的响应对象替换了原来不满足需求的旧响应对象
            return HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)
        else:

            return response     # 1+n

    def process_exception(self, request, exception, spider):

        pass
