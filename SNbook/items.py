# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class SnbookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()
    href = scrapy.Field()
    image = scrapy.Field()
    author = scrapy.Field()
    bookname = scrapy.Field()
    content = scrapy.Field()
    book_href = scrapy.Field()
    price = scrapy.Field()
    next_url = scrapy.Field()
