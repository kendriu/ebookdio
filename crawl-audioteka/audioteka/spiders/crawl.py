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
    start_urls = ['http://audioteka.com/pl/']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths=('(//ul[contains(@class, "menu_level_1")])[1]',
                             '//div[contains(@class, "load-more")]'
                             ),
            deny=('prasa-n$')
        ),
            callback='parse_list',
            follow=True),
    )
    books = []

    def parse_list(self, response):
        result = []
        for sel in response.css('.product-tile'):
            l = AudioBookLoader(selector=sel)
            l.add_xpath(
                'title', './/h3[@class="product-tile__name"]/a/text()')
            l.add_xpath(
                'author', './/div[@class="product-tile__author"]/a/text()')
            l.add_xpath('category', '//h1/text()')

            item = l.load_item()
            if 'author' in item and item['author'] not in EXCLUDED_AUTHORS:
                data = (item['author'], item['title'])
                if data not in self.books:
                    result.append(item)
                    self.books.append(data)
        return result