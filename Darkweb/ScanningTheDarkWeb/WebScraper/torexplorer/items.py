import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags
import datetime


class TorexplorerItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
            )
    url = scrapy.Field(output_processor=TakeFirst())
    redirected_url = scrapy.Field(output_processor=TakeFirst())
    status = scrapy.Field(output_processor=TakeFirst())
    headers = scrapy.Field(output_processor=TakeFirst())
    last_checked = scrapy.Field(output_processor=TakeFirst())
    redirects = scrapy.Field()
    links = scrapy.Field()
    bitcoin = scrapy.Field()
    google = scrapy.Field()
    email = scrapy.Field()
    pgp = scrapy.Field()
    encoding = scrapy.Field(output_processor=TakeFirst())
    favicon = scrapy.Field(output_processor=TakeFirst())
    robots = scrapy.Field()

 