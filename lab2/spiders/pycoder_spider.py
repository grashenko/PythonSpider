
from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.conf import settings
import re

class MyItem(Item):
    url = Field()
    countOfWords = Field()
    countOfLinks = Field()
    frequencyOfLength = Field()


class MyDictionary(Item):
    countLetters = Field()
    countWords = Field()


class PycoderSpider(CrawlSpider):
    name = "tut"
    settings.set('DEPTH_LIMIT', 1)
    start_urls = ['https://en.belstu.by']

    rules = (Rule(LinkExtractor(), callback='parse_url', follow=True), )

    def parse_url(self, response):
        item = MyItem()
        item['url'] = response.url
        links = response.xpath("//a[@href]").extract()
        item['countOfLinks'] = len(links)
        texts = response.xpath('//text()').extract()
        words = []
        for t in texts:
            t = ' '.join(t.split()).strip()
            if len(t) > 0:
                curWords = re.sub('[^0-9a-zA-Z]+', '*', t).split('*')
                curWords = list(filter(None, curWords))
                words.extend(curWords)
        
        item['countOfWords'] = len(words)

        frequency = []

        for w in words:
            l = len(w)
            finded = next((x for x in frequency if x['countLetters'] == l), None)
            if finded:
                finded['countWords'] = finded['countWords'] + 1
            else:
                newLength = MyDictionary()
                newLength['countLetters'] = l
                newLength['countWords'] = 1
                frequency.append(newLength)
        
        item['frequencyOfLength'] = frequency
        return item