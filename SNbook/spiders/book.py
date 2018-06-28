# -*- coding: utf-8 -*-
import scrapy
from SNbook.items import  SnbookItem
import re
from copy import deepcopy


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['suning.com']
    start_urls = ['http://snbook.suning.com/web/trd-fl/999999/0.htm']

    def parse(self, response):
        li_list = response.xpath("//div[@class='three-sort']/a")
        for li in li_list:
            item = SnbookItem()
            item['title'] = li.xpath("./text()").extract_first()
            item['href'] = li.xpath("./@href").extract_first()
            # print(item)
            if item['href'] is not None:
                item['href'] = "http://snbook.suning.com" +  item['href']

                yield scrapy.Request(
                    item['href'],
                    callback=self.parse_detail,
                    meta = {'item':deepcopy(item)})


    def parse_detail(self,response):
        item = response.meta['item']
        book_list = response.xpath("//div[@class='filtrate-books list-filtrate-books']/ul/li")
        for book in book_list:

            item['image'] = book.xpath(".//div[@class='book-img']/a/img/@src").extract_first()
            if item['image'] is None:
                item['image'] = book.xpath(".//div[@class='book-img']/a/img/@src2").extract_first()

            item['bookname']=book.xpath(".//div[@class='book-title']/a/text()").extract_first()
            item['author']=book.xpath(".//div[@class='book-author']/a/text()").extract_first()
            item['content']=book.xpath(".//div[@class='book-descrip c6']/text()").extract_first()
            item['book_href']=  book.xpath(".//div[@class='book-title']/a/@href").extract_first()

            # print(item)
            # item['book_href'] = ["http://snbook.suning.com" + i for i in item['book_href']]
            yield scrapy.Request(
                item['book_href'],
                callback=self.parse_detail_book,
                meta={'item': deepcopy(item)})
            page_count = re.findall("var pagecount=(.*?);",response.body.decode()[0])
            current_page = re.findall("var currentPage=(.*?);", response.body.decode()[0])
            if current_page<page_count:
                next_url = item["next_url"]="?pageNumber={}&sort=0".format(current_page+1)
                yield scrapy.Request(
                    next_url,
                    callback=self.parse_detail,
                    meta = {"item":item}
                )

    def parse_detail_book(self,response):
        item = response.meta['item']
        item['price']=re.findall("\"bp\":'(.*?)',",response.body.decode())
        item['price']=item['price'][0] if len(item['price']) >0 else None
        # print(item['price'])
        yield item