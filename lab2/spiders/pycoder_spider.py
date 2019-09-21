
from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MyItem(Item):
    url= Field()

class PycoderSpider(CrawlSpider):
    name = "tut"
    allowed_domains = ['belstu.by']
    start_urls = ['https://en.belstu.by']

    rules = (Rule(LinkExtractor(), callback='parse_url', follow=False), )

    def parse_url(self, response):
        item = MyItem()
        item['url'] = response.url
        return item