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
    proxy = "localhost:7890"

    def start_requests(self):
        data = {
            'ProductsPerPage': 12,
            'RequestingPageNumber': 1,
            'ProductionDateDecadeStart': 1900,
            'ProductionDateDecadeEnd': 2020,
            'ReleaseDateDecadeStart': 2003,
            'ReleaseDateDecadeEnd': 2021,
            'SortByField': 'release_date',
            'IsSortByAscendin': 'false'
        }
        for page in range(1,79):
            data['RequestingPageNumber'] = page
            yield scrapy.Request("https://api.arrowfilms.com/Umbraco/api/ProductSearch/GetAllActiveFilteredProducts?",
                                body=json.dumps(data),
                                headers={'Content-Type': 'application/json',#'application/x-www-form-urlencoded',
                                            'Accept': "*/*",
                                            'Accept-Encoding': 'gzip, deflate, br',
                                            'User-Agent': 'PostmanRuntime/7.26.8',
                                            'Connection': 'keep-alive',
                                            },
                                method="POST",
                                meta={"proxy": self.proxy},
                                callback=self.parse)

    def parse(self, response):
        if(response.url.find('api') > 0):

            results = json.loads(response.text)[
                'Data']['result']['ProductSearchResults']

            urls = []

            for item in results:
                url = 'https://arrowfilms.com/product-detail/gamera---the-heisei-trilogy--steelbook--blu-ray/' + item['ProductCode']
                urls.append(url);
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
                                ProductCode=productCode,
                                year="api"
                                )
                yield a
                yield from response.follow_all(urls, meta={"proxy": self.proxy})
        else:
            keyList  = response.css('#details-text').re(r'<b>(.+?):</b>')
            valueList  = response.css('#details-text::text').re(r'^[^\r]\s?(.+)\b')
            # 一种写法
            dic = {keyList[i]:valueList[i] for i in range(len(keyList)) }
            
            dic['year'] = 'desc'
            print(dic)
            # 简写
            #dic = dict(zip(keyList,valueList))
            #dic['year'] = 'desc'
            #print(dic)
            #for s in l:
                #print(type(s))

            yield dic