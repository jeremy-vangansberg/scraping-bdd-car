# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader import ItemLoader


class CarAccident(CrawlSpider):
    name = 'accident'
    allowed_domains = ['data.gouv.fr']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2020/#resources', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//section[@class='ressources fr-py-10w']"),
             callback='parse_item', follow=True, process_request='set_user_agent'),
        # #Rule(LinkExtractor(
        #     restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"), process_request='set_user_agent')
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            "link": response.xpath("//dd[@class='fr-ml-0 fr-col-8 fr-col-md-9 fr-col-lg-10 text-overflow-ellipsis']/a/text()").extract()
        }
        