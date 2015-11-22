import scrapy
from wayfaircraw.items import houzzItem
from scrapy.utils.response import get_base_url
import scrapy.utils.url as surl

class houzzSpider(scrapy.Spider):
    name = "houzz"
    allowed_domains = ["houzz.com"]
    start_urls = ["http://www.houzz.com/photos/furniture"]

    def parse(self,response):
        print 'start houzz'
	#col-categories-selected
        for catsel in response.xpath('//*[@class="sidebar filter-tree collapsible"]').xpath('*/ul/li[@class="D2 sidebar-item"]'):
            item = houzzItem()
	    pathurl = []
	    pathurl.append(catsel.xpath('a/@href').extract()[0])
            item['path_url'] = pathurl
            item['path_name'] = catsel.xpath('a/span/text()').extract()
	    item['main_bread'] = [response.xpath('//*[@class="breadcrumb-item "]/a/span/text()').extract()]
            print "!!!!!!!!!!!!!",item
            yield scrapy.Request(item['path_url'][-1],meta={'item':item},callback=self.pg2parse)

    def nstage(self,ttmap):
        for i in ttmap.keys():
            treenode = ttmap.get(i)
            if len(treenode)>1:
                return ttmap.get(i)
            else:
                continue
        return None

   
    def pg2parse(self,response):
        print 'pg2parse'
        #selected D2 D3 D4 maybe D5
        topic_tree = response.xpath('//*[@id="topicTreeFilter"]/li')
        ttmap={'d1': topic_tree.css('.D1') ,'d2': topic_tree.css('.D2') ,'d3': topic_tree.css('.D3') ,'d4': topic_tree.css('.D4') ,'d5':topic_tree.css('.D5')}
        next_step = self.nstage(ttmap=ttmap)
        if None == next_step:
            pass
            #go to product list page
        else:
            #goto pg2parse
            for subcat in next_step:
                
		item = houzzItem() 
                item['path_url']=[]
                item['path_name']=[]
                item['main_bread']=[]
                item['path_url'].extend( response.meta['item']['path_url'])
                item['path_name'].extend( response.meta['item']['path_name'])
                item['main_bread'].extend(  response.meta['item']['main_bread'])
		item['path_url'].append(subcat.xpath('a/@href').extract()[0])
		item['path_name'].append(subcat.xpath('a/span/text()').extract()[0])
		item['main_bread'].append(response.xpath('//*[@class="breadcrumb-item "]/a/span/text()').extract())
                print "!!!!!!!!!!!!!==========",item
                yield scrapy.Request(item['path_url'][-1],meta={'item':item},callback=self.pg2parse)
               # else:
               #     yield scrapy.Request(item['path_url'][-1],meta={'item':item},callback=self.pg2parse)

    def parse_prod_list(self,response):
        print 'parse_prod_list'
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
            print "=======================PD:",item
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
        item['product_name'] = response.css('.nomeInPage').xpath('text()').extract()
        item['pre_title'] = response.css('.pretitleInPage').xpath('text()').extract()
        item['manufacturer_name'] = response.css('.brandInPage').xpath('a/text()').extract()
        item['designer'] = response.css('.designerInPage').xpath('span/a/span[@itemprop="name"]/text()').extract()
        item['designer_description'] = response.css('.designerDescription').xpath('a/text()').extract()
        item['description'] = ''.join(response.css('#ProductGeneralDescription').xpath('text()').extract())
        item['tags'] = response.css('.tags').xpath('a/text()').extract()
        item['image_urls'] = response.css('.productGalleryThumb ').xpath('ul/li/a/@href').extract()

        return item 
