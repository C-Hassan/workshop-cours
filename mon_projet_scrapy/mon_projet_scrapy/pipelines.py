# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NomDuProjetPipeline:
    def process_item(self, item, spider):
        return item
    
    # mon_projet_scrapy/pipelines.py

import csv

class CsvPipeline:
    def open_spider(self, spider):
        self.file = open(spider.settings.get('FEED_URI', 'output.csv'), 'w', newline='')
        self.writer = csv.writer(self.file)

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.writer.writerow([item.get('title', '')])
        return item

