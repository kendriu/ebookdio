# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst
from scrapy.loader import ItemLoader


class AudioBookItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()


class AudioBookLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_item_class = AudioBookItem
