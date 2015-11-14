import scrapy
from wayfaircraw.items import ArchItem
from scrapy.utils.response import get_base_url
import scrapy.utils.url as surl

class archSpider(scrapy.Spider):
    name = "arch"
    allowed_domains = ["archiproducts.com"]
    start_urls = ["http://www.archiproducts.com/en/b1390/furniture.html"]

    def parse(self,response):
        urlstr = "%s://%s%s"
        print 'start'
	parsedurl = surl.parse_url(get_base_url(response))
	#col-categories-selected
	for catsel in response.css('.col-categories-selected'):
		item = ArchItem()
		pathurl = []
		pathurl.append(urlstr%(parsedurl.scheme,parsedurl.netloc,catsel.xpath('a/@href').extract()[0]))
		item['path_url'] = pathurl
		item['path_name'] = catsel.xpath('a/span/text()').extract()
		item['main_bread'] = catsel.xpath('//*[@itemprop="title"]/text()').extract()
		print "!!!!!!!!!!!!!",item['path_url']
		yield scrapy.Request(item['path_url'][-1],meta={'item':item},callback=self.pg2parse)

   
    def pg2parse(self,response):
        print 'pg2parse'
	parsedurl = surl.parse_url(get_base_url(response))
        urlstr = "%s://%s%s"
	for subcat in response.css('.cont-sub-content'):
		item =  response.meta['item']
		realurl = urlstr%(parsedurl.scheme,parsedurl.netloc,subcat.xpath('a/@href').extract()[0])
		item['path_url'].append(realurl)
		item['path_name'].append(subcat.xpath('a/*/h2[@itemprop="name"]/text()').extract()[0])
		item['main_bread'].append(response.xpath('//*[@itemprop="title"]/text()').extract())
                print '=======pathurl',item['path_url'][-1]
                print len(response.css('.search-result'))
                yield scrapy.Request(item['path_url'][-1],meta={'item':item},callback=self.parse_prod_list)
               # else:
               #     yield scrapy.Request(item['path_url'][-1],meta={'item':item},callback=self.pg2parse)

    def parse_prod_list(self,response):
        print 'parse_prod_list'
        urlstr = "%s://%s%s"
        parsedurl = surl.parse_url(get_base_url(response))
        for grid in response.css('.clearfix .grid_link'):
            item =  response.meta['item']
            prdlnk = grid.xpath('a/@href').extract()
            realurl = urlstr%(parsedurl.scheme,parsedurl.netloc,prdlnk)
            item['path_url'].append(realurl)
            item['path_name'].append(grid.css('.name-product').xpath('text()').extract())
            item['main_bread'].append(response.xpath('//*[@itemprop="title"]/text()').extract())
            yield scrapy.Request(item['path_url'][-1],meta={'item':item},callback=self.parse_content)
            #return item
        nxtpg = response.css('.btn-pag-right').xpath('@href').extract()
        if len(nxtpg)>0:
            nextpage = urlstr%(parsedurl.scheme,parsedurl.netloc,nxtpg[0])
            yield scrapy.Request(nextpage,meta={'item':response.meta['item']},callback=self.parse_prod_list)

    def parse_content(self,response):
        urlstr = "%s://%s%s"
        print 'parse_content'
        return   response.meta['item']
