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
    path_name=Field() #Sofas and Armchairs : http://www.archiproducts.com/en/b779/sofas-and-armchairs.html
    path_url=Field()
    main_bread=Field()
    product_url=Field()
    product_bread = Field()
    product_name = Field() #nomeInPage
    pre_title = Field()
    manufacturer_name=Field() 
    designer = Field() #designerInPage
    designer_description = Field()
    description = Field() #description
    tags = Field()
    image_urls = Field()
    images = Field()
    image_name = Field()

class houzzItem(Item):
    path_name=Field()
    path_url=Field()
    main_bread=Field()
    product_url=Field()
    product_name = Field() #title
    product_bread = Field()
    manufacturer_name=Field()
    product_description=Field()
    product_spec = Field()
    description = Field()
    image_urls = Field()
    images = Field()
    image_name = Field()
