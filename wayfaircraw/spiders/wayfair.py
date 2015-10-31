import scrapy
from wayfaircraw.items import WayfaircrawItem

class wayfairSpider(scrapy.Spider):
    name = "wayfair"
    allowed_domains = ["wayfair.com"]
    start_urls = ["http://www.wayfair.com/Furniture-C45974.html"]

    def parse(self,response):
        for lo in response.xpath("//*[@id='cms_lego_39325']/div[2]/span/a"):
            item  = WayfaircrawItem()
            item['lvone_name'] = lo.xpath('text()').extract()[0].replace('\n','').strip()
            item['lvone_url'] = lo.xpath('@href').extract()[0]
            yield scrapy.Request(item['lvone_url'],callback= self.parse_two)
    
    def parse_two(self,response):
        for lt in response.xpath("//*[@id='cms_lego_40656']/div[2]/span/a"):
            itemtwo = WayfaircrawItem()
            itemtwo['lvtwo_name'] = lt.xpath('text()').extract()[0].replace('\n','').strip() 
            itemtwo['lvtwo_url'] = lt.xpath('@href').extract()[0] 
            return itemtwo
    
    def parse_three(self,response):
        vlt_names = [ln.replace('\n','').strip() for ln in response.xpath('//*[@class="attributeul"]/a/text()').extract()]
        for lth  in response.xpath(
        pass

    def parse_content(self,response):
        pass
            
