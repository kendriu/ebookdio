# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from audioteka.items import AudioBookLoader

EXCLUDED_AUTHORS = [
    'CIDEB EDITRICE',
    'Gamma',
    'Disney'
]


class CrawlSpider(CrawlSpider):
    name = 'crawl'
    allowed_domains = ['audioteka.com']
    start_urls = ['http://audioteka.com/pl/audiobooks']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths=('//ul[contains(@class, "all-categories")]',
                             '//h2[contains(@class, "fs17")]',
                             '//div[contains(@class, "items-loader")]'
                             ),
            deny=('prasa-n$', 'polityka-n$')
        ),
            callback='parse_list',
            follow=True),
    )
    books = []

    def parse_list(self, response):
        result = []
        for sel in response.css('.item'):
            l = AudioBookLoader(selector=sel)

            l.add_xpath(
                'title', './/h2[@class="item__title"]/a/text()')
            l.add_xpath(
                'author', './/div[@class="item__author"]/a/text()')

            item = l.load_item()
            if 'author' in item and item['author'] not in EXCLUDED_AUTHORS:
                data = (item['author'], item['title'])
                if data not in self.books:
                    result.append(item)
                    self.books.append(data)
        return result
