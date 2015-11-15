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
		item['main_bread'] = [catsel.xpath('//*[@itemprop="title"]/text()').extract()]
		print "!!!!!!!!!!!!!",item['path_url']
		yield scrapy.Request(item['path_url'][-1],meta={'item':item},callback=self.pg2parse)

   
    def pg2parse(self,response):
        print 'pg2parse'
	parsedurl = surl.parse_url(get_base_url(response))
        urlstr = "%s://%s%s"
	for subcat in response.css('.cont-sub-content').xpath('a'):
		item = ArchItem() 
                item['path_url']=[]
                item['path_name']=[]
                item['main_bread']=[]
                item['path_url'].extend( response.meta['item']['path_url'])
                item['path_name'] .append( response.meta['item']['path_name'])
                item['main_bread'] .append(  response.meta['item']['main_bread'])
                realurl = urlstr%(parsedurl.scheme,parsedurl.netloc,subcat.xpath('@href').extract()[0])
		item['path_url'].append(realurl)
		item['path_name'].append(subcat.xpath('*/h2[@itemprop="name"]/text()').extract()[0])
		item['main_bread'].append(response.xpath('//*[@itemprop="title"]/text()').extract())
                print "!!!!!!!!!!!!!==========",item['path_url']
                yield scrapy.Request(item['path_url'][-1],meta={'item':item},callback=self.parse_prod_list)
               # else:
               #     yield scrapy.Request(item['path_url'][-1],meta={'item':item},callback=self.pg2parse)

    def parse_prod_list(self,response):
        print 'parse_prod_list'
        urlstr = "%s://%s%s"
        parsedurl = surl.parse_url(get_base_url(response))
        for grid in response.css('.clearfix .grid_link'):
            item = ArchItem() 
            item['path_url']=[]
            item['path_name']=[]
            item['main_bread']=[]
            item['path_url'].extend( response.meta['item']['path_url'])
            item['path_name'] .append( response.meta['item']['path_name'])
            item['main_bread'] .append(  response.meta['item']['main_bread'])
            prdlnk = grid.xpath('a/@href').extract()[0]
            realurl = urlstr%(parsedurl.scheme,parsedurl.netloc,prdlnk)
            item['path_url'].append(realurl)
            item['path_name'].append([grid.css('.name-product').xpath('text()').extract()])
            item['main_bread'].append(response.xpath('//*[@itemprop="title"]/text()').extract())
            print "=======================PD:",item['path_url']
            yield scrapy.Request(item['path_url'][-1],meta={'item':item},callback=self.parse_content)
            #return item
        nxtpg = response.css('.btn-pag-right').xpath('@href').extract()
        if len(nxtpg)>0:
            nextpage = urlstr%(parsedurl.scheme,parsedurl.netloc,nxtpg[0])
            yield scrapy.Request(nextpage,meta={'item':response.meta['item']},callback=self.parse_prod_list)

    def parse_content(self,response):
        urlstr = "%s://%s%s"
        item  = ArchItem()
        item['path_url']=[]
        item['path_name']=[]
        item['main_bread']=[]
        item['path_url'].extend( response.meta['item']['path_url'])
        item['path_name'] .append( response.meta['item']['path_name'])
        item['main_bread'] .append(  response.meta['item']['main_bread'])
        item['product_bread'] = response.xpath('//*[@itemprop="title"]/text()').extract()
        item['product_name'] = response.css('.nomeInPage').xpath('text()').extract()[0]
        item['pre_title'] = response.css('.pretitleInPage').xpath('text()').extract()[0]
        item['manufacturer_name'] = response.css('.brandInPage').xpath('a/text()').extract()[0]
        item['designer'] = response.css('.designerInPage').xpath('span/a/span[@itemprop="name"]/text()').extract()[0]
        item['designer_description'] = response.css('.designerDescription').xpath('a/text()').extract()[0]
        item['description'] = ''.join(response.css('#ProductGeneralDescription').xpath('text()').extract())
        item['tags'] = response.css('.tags').xpath('a/text()').extract()
        item['image_urls'] = response.css('.productGalleryThumb ').xpath('ul/li/a/@href').extract()
        item['image_names']

        return item 
