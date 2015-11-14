# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class WayfaircrawItem(Item):
    # define the fields for your item here like:
    # name = Field()
    path_name = Field()
    path_url = Field()
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
    breadcrumb = Field()
    product_nova_breadcrumbs = Field()
    pass

class ArchItem(Item):
    path_name_url=Field() #Sofas and Armchairs : http://www.archiproducts.com/en/b779/sofas-and-armchairs.html
    main_bread=Field()
    
