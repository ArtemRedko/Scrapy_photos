import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import ZebrsItem
from itemloaders.processors import MapCompose


class ImagesSpider(CrawlSpider):
    name = "images"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/"]

    rules = (Rule(LinkExtractor(restrict_xpaths="//*[@id=':Rlue:']/div/div/div/descendant::figure/div[@class='yu56q']/a"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        loader = ItemLoader(item=ZebrsItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)
        loader.add_value('name', response.xpath('//*[@id="app"]/div/div/div[3]/div/div[1]/div[4]/div[3]/div[1]/h1/text()').get())
        category = response.xpath('//*[@id="app"]/div/div/div[3]/div/div[1]/div[4]/div[5]/a/text()').getall()
        loader.add_value('category', category)
        image_urls = response.xpath('//*[@id="app"]/div/div/div[3]/div/div[1]/div[2]/div/img[2]/@src').get()
        loader.add_value('image_urls',image_urls)
        yield loader.load_item()
        