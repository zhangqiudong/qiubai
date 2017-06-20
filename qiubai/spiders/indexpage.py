import  scrapy
from qiubai.items import QiubaiItem
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class QiuBaiSpider(CrawlSpider):
    name = 'qiubai'
    start_urls =[
        "http://www.qiushibaike.com"
    ]
    rules = [
        Rule(LinkExtractor(allow='/article/*')),
        Rule(LinkExtractor(allow='/users/*'),callback=('parse_name')),
    ]

    def parse_name(self, response):
        print(response.xpath('//div[@class="user-header-cover"]/h2/text()').extract()[0])

    '''def parse(self, response):
        for href in response.xpath('//a[@class="qiushi_comments"]/@href').extract():
            detail_url = response.urljoin(href)
            req = Request(detail_url,self.parse_detail)
            item = QiubaiItem()
            req.meta['item'] = item
            yield req
'''
    def parse_detail(self,response):
        item = response.meta["item"]
        item['author'] = response.xpath('//div[@class="author clearfix"]/a[2]/h2/text()').extract() if response.xpath('//div[@class="author clearfix"]').extract() else ""
        item['content'] = response.xpath('//div[@class="content"]/text()').extract()
        comments =[]
        for comment in response.xpath('//div[@class="comments-table"]'):
            comment_author = comment.xpath('./a[@class="comments-table-main"]/div[1]/div/text()').extract()
            comment_content = comment.xpath('./a[@class="comments-table-main"]/div[2]/text()').extract()
            comments.append({"comment_author":comment_author,"commenrt_content":comment_content})
            item["comments"] = comments
            yield item






