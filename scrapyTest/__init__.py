#!/usr/bin/env python
# -*- coding:utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://www.baidu.com/s?wd=%E6%96%B0%E7%95%99%E5%AE%88%E9%9D%92%E5%B9%B4&pn=0',
    ]

    # def parse(self, response):
    #     for quote in response.css('div.quote'):
    #         yield {
    #             'text': quote.css('span.text::text').get(),
    #             'author': quote.xpath('span/small/text()').get(),
    #         }
    #
    #     next_page = response.css('li.next a::attr("href")').get()
    #     if next_page is not None:
    #         yield response.follow(next_page, self.parse)


    def parse(self, response):
        for quote in response.css('div.result'):
            yield {
                'title': quote.css('h3.t>a').get(),
                #'author': quote.xpath('span/small/text()').get(),
            }

        next_page = response.css('a.n::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)