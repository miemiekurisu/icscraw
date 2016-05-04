import scrapy
from wayfaircraw.items import firstItem
from scrapy.utils.response import get_base_url
import scrapy.utils.url as surl


base_url = 'https://www.1stdibs.com%s'
class firstSpider(scrapy.Spider):
    name = "1st"
    start_urls = [ 'https://www.1stdibs.com/furniture/?page=%s'%i for i in range(0,5000)]

    def parse(self,response):
        for grid_url in response.xpath('//*[@class="product-container"]/a/@href').extract():

            yield scrapy.Request(base_url%grid_url,callback=self.parse_content)
        #self.parse_next(response)
   
    def parse_next(self, response):
        next_arrow = response.xpath('//*[contains(@class,"is-arrow") and contains(@class,"is-right") and contains(@class,"is-last")]/a/@href').extract()
        print next_arrow
        if len(next_arrow) == 1:
            scrapy.Request(base_url%next_arrow[0],callback=self.parse)
 
    def parse_content(self,response):
        item = firstItem()
        item['title']= response.xpath('//*[@property="og:title"]/@content').extract()[0].replace('| 1stdibs.com','')
        item['url']=response.xpath('//*[@property="og:url"]/@content').extract()[0]
        item['description']= response.xpath('//*[@name="twitter:description"]/@value').extract()[0]
        item['bread']= response.xpath('//*[@class="page-breadcrumb"]/a/span/text()').extract()
        item['image_urls'] = response.xpath('//*[@class="pdp-hero-carousel-image"]/@src').extract()
        
        info_block =response.xpath('//*[@class="pdp-details-entry"]')
        info_dict = {}
        for i in info_block:
            key = i.xpath('div/span/text()').extract()[0]
            value = i.xpath('div/div/span/text() | div/div/a/text() | div/div/text()').extract()
            info_dict[key] =  ' '.join([c.strip() for c in value])
        item['info']=info_dict
        return item
