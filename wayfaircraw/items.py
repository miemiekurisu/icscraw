# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class WayfaircrawItem(Item):
    # define the fields for your item here like:
    # name = Field()
    lvone_name = Field()
    lvone_url = Field()
    lvtwo_name = Field()
    lvtwo_url = Field()
    lvthree_names = Field()
    prod_url = Field()
    imgs = Field()
    title_name = Field()
    manu_name = Field()
    product_info = Field()
    product_section_description = Field()
    product_sub_section =Field()
    product_last_section = Field()
    spec_dimentions = Field()
    spec_table= Field()
    pass
