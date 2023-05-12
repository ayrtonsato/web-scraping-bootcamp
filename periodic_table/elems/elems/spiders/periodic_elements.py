import scrapy
from scrapy.loader import ItemLoader
from elems.items import PeriodicElementItem
from scrapy_playwright.page import PageMethod


class PeriodicElementsSpider(scrapy.Spider):
    name = "periodic_elements"

    def start_requests(self):
        yield scrapy.Request(
            'https://pubchem.ncbi.nlm.nih.gov/ptable',
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod('wait_for_selector', 'div.ptable div#an-1')
                ]
            }
        )

    def parse(self, response):
        for element in response.css("div.ptable div.element"):
            i = ItemLoader(item=PeriodicElementItem(), selector=element)

            i.add_css('symbol', '[data-tooltip="Symbol"]')
            i.add_css('name', '[data-tooltip="Name"]')
            i.add_css('atomic_number', '[data-tooltip="Atomic Number"]')
            i.add_css('atomic_mass', '[data-tooltip*="Atomic Mass"]')
            i.add_css('chemical_group',
                      '[data-tooltip="Chemical Group Block"]')

            yield i.load_item()
