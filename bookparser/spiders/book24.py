import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem
from scrapy.loader import ItemLoader

from pprint import pprint

class Book24Spider(scrapy.Spider):
    name = "book24"
    allowed_domains = ["book24.ru"]


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://book24.ru/search/?q={kwargs.get('query')}"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='pagination__item _link _button _next smartLink']").get()
        # print(f"{next_page = }")
        if next_page:
            yield response.follow(next_page, callback=self.parse)


        links = response.xpath("//div[@class='product-list__item']//a[@class='product-card__name']")
        for link in links:
            yield response.follow(link, callback=self.parse_book)

    def parse_book(self, response: HtmlResponse):
        # name = response.xpath("//h1/text()").get()
        # price = response.xpath("//span[@class='app-price product-sidebar-price__price']/text()").get().split(" ")
        # for n in range(len(price)):
        #     if not price[n] in ("\xa0",""):
        #         price = price[n].replace("\xa0","").replace(",",".")
        #         break
        #
        # url = response.url
        # # https://help.1forma.ru/Admin_Manual/xpath_basic.htm
        # photos = response.xpath("//picture[@class='product-poster__main-picture']/source[1]/@data-srcset | "
        #                         "//picture[@class='product-poster__main-picture']/source[1]/@srcset")
        # yield BookparserItem(name=name, price=price, url=url, photos=photos)

        loader = ItemLoader(item=BookparserItem(), response=response)
        loader.add_xpath('name',"//h1/text()")
        loader.add_xpath('price',"//span[@class='app-price product-sidebar-price__price']/text()")
        # loader.add_xpath('currency', "//span[@class='app-price product-sidebar-price__price']/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('photos', "//picture[@class='product-poster__main-picture']/source[1]/@data-srcset | "
                                   "//picture[@class='product-poster__main-picture']/source[1]/@srcset")


        yield loader.load_item()










