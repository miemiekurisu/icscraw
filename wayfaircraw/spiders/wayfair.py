import scrapy
from wayfaircraw.items import WayfaircrawItem

class wayfairSpider(scrapy.Spider):
    name = "wayfair"
    allowed_domains = ["wayfair.com"]
    start_urls = ["http://www.wayfair.com/Furniture-C45974.html"]

    def parse(self,response):
        print 'LV1'
        for lo in response.xpath("//*[@id='cms_lego_39325']/div[2]/span/a"):
            item  = WayfaircrawItem()
            item['lvone_name'] = lo.xpath('text()').extract()[0].replace('\n','').strip()
            item['lvone_url'] = lo.xpath('@href').extract()[0]
            print item['lvone_name']
            yield scrapy.Request(item['lvone_url'],meta={'item':item},callback= self.parse_two)
    
    def parse_two(self,response):
        print 'LV2'
        for lt in response.xpath("//*[@id='cms_lego_40656']/div[2]/span/a"):
            itemtwo = response.meta['item']
            itemtwo['lvtwo_name'] = lt.xpath('text()').extract()[0].replace('\n','').strip() 
            itemtwo['lvtwo_url'] = lt.xpath('@href').extract()[0] 
            print itemtwo['lvtwo_name']
            yield scrapy.Request(itemtwo['lvtwo_url'],meta={'item':itemtwo},callback=self.parse_three)
    
    def parse_three(self,response):
        print 'LV3'
        #parse_lvthree
        for lt in response.css('.productbox').xpath('@href').extract():
            itemthree = response.meta['item']
            itemthree['prod_url']=lt
            yield scrapy.Request(lt,meta={'item':itemthree},callback=self.parse_content)
	nextpage = response.css(".js-next-page").xpath('@href').extract()
        print 'nextpage=%s'%nextpage
        if(len(nextpage)>0):
            yield scrapy.Request(nextpage[0],meta={'item':response.meta['item']},callback=self.parse_three)
    
    def parse_content(self,response):
        ci = response.meta['item']
        ci['imgs']=response.css('.js-photoswipe-item').xpath('a/@data-original-src').extract()
        ci['title_name']=response.css('.title_name').xpath('text()').extract()[0].replace('\n','').strip()
        ci['manu_name']=response.css('.manu_name').xpath('text()').extract()[0].replace('\n','').strip()
        #ci['product_info']
        ci['product_section_description']=[i.replace('\n','').strip() for i in response.css('.product_section_description').xpath('text()').extract()]
        ci['product_sub_section']=[i.replace('\n','').strip() for i in response.css('.product_sub_section').xpath('ul/li/text()').extract()]
        ci['spec_dimentions']= [i.replace('\n','').strip() for i in response.css('.spec_dimensions').xpath('p/text()|ul/li/text()').extract()]
        ci['spec_table']= [i.replace('\n','').strip() for i in response.css('.spec_table').xpath('tr/td/strong/text() | tr/td/text()').extract()]
        return ci
