# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from swiatczytnikow.items import EbookLoader


class CrawlSpider(CrawlSpider):
    name = 'crawl'
    allowed_domains = ['ebooki.swiatczytnikow.pl']
    start_urls = ['http://ebooki.swiatczytnikow.pl/katalog']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths=('//ul[@class="letters"]',
                             '//div[@class="pagination"]')),
             callback='parse_list', follow=True),

    )
    books = []

    def parse_list(self, response):
        result = []
        for sel in response.xpath('//ul[@class="cataloglist"]/li'):
            l = EbookLoader(selector=sel)
            l.add_xpath(
                'title', './/div[contains(@class, "title")]//a/text()')
            l.add_xpath(
                'author', './/div[contains(@class, "author")]//a/text()')
            item = l.load_item()
            if 'author' in item:
                data = (item['author'], item['title'])
                if data not in self.books:
                    result.append(item)
                    self.books.append(data)
        return result
