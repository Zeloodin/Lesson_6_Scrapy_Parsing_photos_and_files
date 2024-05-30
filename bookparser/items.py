# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from  itemloaders.processors import TakeFirst, MapCompose, Compose

def process_name(value):
    value = value[0].strip()
    return value

def process_price(value):
    value = value[0].strip()
    value = value.replace("\xa0"," ").replace(",",".")
    if value[:-1].isdigit():
        value, currency = int(value[:-1].replace(" ","")),value[-1]
    else:
        value, currency = value[:-1].replace(" ", ""),value[-1]
    return value, currency

def process_photo(value:str):
    if value.startswith("//"):
        value = "https:" + value.split()[0]
    else:
        if value.find(", ") != -1:
            value = value.split()[1]
    return value


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=Compose(process_name),output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(process_price))
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(process_photo))
    _id = scrapy.Field()

