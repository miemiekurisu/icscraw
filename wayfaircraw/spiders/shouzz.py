import scrapy
from wayfaircraw.items import houzzItem
from scrapy.utils.response import get_base_url
import scrapy.utils.url as surl

class houzzSpider(scrapy.Spider):
    name = "houzz"
    allowed_domains = ["houzz.com"]
    start_urls = ["http://www.houzz.com/photos/furniture"]

    def parse(self,response):
        all_furnitures = response.css('.D2 a').xpath('@href').extract()
        for to_grid in all_furnitures:
            yield scrapy.Request(to_grid, callback=self.parse_sub_cata)
    
    def parse_sub_cata(self,response):
        for grid in response.xpath('//*[@class="ic whiteCard m "]').xpath('*/a/@href').extract():
            yield scrapy.Request(grid,callback=self.parse_content)
        nxtpg = response.xpath('//*[@class="navigation-button next"]/@href').extract()
        if len(nxtpg)>0:
            nextpage = nxtpg[0]
            print 'parse_prod_list, to nxtpg:'
            yield scrapy.Request(nextpage,callback=self.parse_sub_cata)


    def parse_content(self,response):
        pageinfo = response.xpath('//*[@id="hzProductInfo"]')
        item  = houzzItem()
        item['product_bread'] = response.xpath('//*[@class="breadcrumb-item "]/a/span/text()').extract()
        item['product_name'] =pageinfo.xpath('*/header/*[@itemprop="name"]/text()').extract()[0]
        item['description'] = ' '.join([i.strip() for i in pageinfo.xpath('//*[@class="description"]/text()').extract()])
        item['image_urls']=response.css('#mainImage').xpath('@src').extract()
        item['image_urls'].extend(response.css('.productGalleryThumb ').xpath('ul/li/a/@href').extract())
        spec = {}
        keys = []
        values = []
        for i in pageinfo.xpath('//*[@class="productSpec"]').xpath('*//*[@class="key"]'):
            keys.append(''.join(i.xpath('span/a/text()|text()|span/text()|a/text()').extract()).strip())
        for j in pageinfo.xpath('//*[@class="productSpec"]').xpath('*//*[@class="value"]'):
            values.append(''.join(j.xpath('span/a/text()|text()|span/text()|a/text()').extract()).strip())
        if len(keys) != len(values):
            print str(keys),str(values)
        for k in range(0,len(keys)):
            spec[keys[k]]=values[k]
        item['product_spec'] = spec
        item['product_url'] = response.url
        print "parse_content",item
        return item 
