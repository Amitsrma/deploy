# -*- coding: utf-8 -*-
import scrapy


class GooglenewsheadlineSpider(scrapy.Spider):
    name = 'googlenewsheadline'
    allowed_domains = ['https://newsapi.org/v2/everything?q=bitcoin&apiKey=APIKEY']
    start_urls = ['http://https://newsapi.org/v2/everything?q=bitcoin&apiKey=APIKEY/']

    def parse(self, response):
        pass
