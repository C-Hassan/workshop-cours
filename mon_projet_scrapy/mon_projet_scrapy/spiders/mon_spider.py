import scrapy
import logging

class MonSpider(scrapy.Spider):
    name = 'mon_spider'
    start_urls = ['https://www.kartable.fr/francais/college']

    custom_settings = {
        'LOG_LEVEL': logging.DEBUG,  # More detailed logging
        'ITEM_PIPELINES': {'mon_projet_scrapy.pipelines.CsvPipeline': 1},
        'FEEDS': {
            'kartable_result.csv': {
                'format': 'csv',
                'overwrite': True  # Ensures the file is overwritten each time the spider is run
            }
        }
    }

    def parse(self, response):
        # Extraction du titre de la page
        title = response.xpath('//title/text()').get()
        if title:
            yield {
                'title': title.strip()
            }
