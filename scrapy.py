import scrapy


class BrickSetSpider(scrapy.Spider):
    name = "mys_spider"
    start_urls = ['http://webscantest.com/']