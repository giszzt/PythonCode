# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SofangItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    address=scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    m_price = scrapy.Field()
    lon=scrapy.Field()
    lat=scrapy.Field()
