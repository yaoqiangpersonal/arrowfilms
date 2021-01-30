import scrapy
import json
import requests
from lxml import etree
import re
from functools import reduce
from arrowfilms.items import ArrowfilmsItem


class ArrowSpider(scrapy.Spider):
    name = 'arrow'
    allowed_domains = ['arrowfilms.com']
    proxy = "192.168.1.199:7890"

    def start_requests(self):
        data = {
            'ProductsPerPage': 12,
            'RequestingPageNumber': 1,
            'ProductionDateDecadeStart': 1900,
            'ProductionDateDecadeEnd': 2020,
            'ReleaseDateDecadeStart': 2003,
            'ReleaseDateDecadeEnd': 2021,
            'SortByField': 'release_date',
            'IsSortByAscendin':'false'
        }
        for page in range(2,79):
            data['RequestingPageNumber'] = page
            yield scrapy.Request("https://api.arrowfilms.com/Umbraco/api/ProductSearch/GetAllActiveFilteredProducts?",
                             body=json.dumps(data),
                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                      'Accept': "*/*",
                                      'Accept-Encoding': 'gzip, deflate, br',
                                      'User-Agent': 'PostmanRuntime/7.26.8',
                                      'Connection': 'keep-alive',
                                      },
                             method="POST",
                             meta={"proxy": self.proxy},
                             callback=self.parse)

    def parse(self, response):
        results = json.loads(response.text)[
            'Data']['result']['ProductSearchResults']
        for item in results:
            req = requests.get(
                'https://arrowfilms.com/product-detail/gamera---the-heisei-trilogy--steelbook--blu-ray/' +
                item['ProductCode'],
                proxies={'http': self.proxy}
            )
            selector = etree.HTML(req.text)
            l = selector.xpath('//div[@id="details-text"]/text()')
            desc = reduce(lambda a, b: a.strip() + "." + b.strip(), l)

            productId = item['ProductId']
            standardPrice = item['StandardPrice']
            roductOfferPrice = item['ProductOfferPrice']
            releaseDate = item['ReleaseDate']
            productCode = item['ProductCode']
            productName = item['ProductName']

            a = ArrowfilmsItem(ProductId=productId,
                               StandardPrice=standardPrice,
                               ProductOfferPrice=roductOfferPrice,
                               ReleaseDate=releaseDate,
                               ProductName=productName,
                               Desc=desc,
                               ProductCode=productCode
                               )

            yield a
