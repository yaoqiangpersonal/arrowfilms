# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArrowfilmsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ProductId = scrapy.Field()
    StandardPrice = scrapy.Field()
    ProductOfferPrice = scrapy.Field()
    ReleaseDate = scrapy.Field()
    ProductCode = scrapy.Field()
    ProductName = scrapy.Field()
    year = scrapy.Field()
    
