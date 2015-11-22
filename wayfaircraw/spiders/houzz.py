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
        #item = houzzItem()
        #item['path_url']=[]
        #item['path_name']=[]
        #item['main_bread']=[]
        #item['path_url'].extend( response.meta['item']['path_url'])
        #item['path_name'].extend( response.meta['item']['path_name'])
        #item['main_bread'].extend(  response.meta['item']['main_bread'])

        if None == next_step:
            #go to product list page
            item = houzzItem()
            item['path_url']=[]
            item['path_name']=[]
            item['main_bread']=[]
            item['path_url'].extend( response.meta['item']['path_url'])
            item['path_name'].extend( response.meta['item']['path_name'])
            item['main_bread'].extend(  response.meta['item']['main_bread'])
            yield scrapy.Request(item['path_url'][-1],meta={'item':item},callback=self.parse_prod_list)
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

    def parse_prod_list(self,response):
        print 'parse_prod_list'
        for grid in response.xpath('//*[@class="ic whiteCard m "]'):
            item = ArchItem() 
            item['path_url']=[]
            item['path_name']=[]
            item['main_bread']=[]
            item['path_url'].extend( response.meta['item']['path_url'])
            item['path_name'] .append( response.meta['item']['path_name'])
            item['main_bread'] .append(  response.meta['item']['main_bread'])
            prdlnk = grid.xpath('*/a/@href').extract()[0]
            realurl = urlstr%(parsedurl.scheme,parsedurl.netloc,prdlnk)
            item['path_url'].append(realurl)
            item['path_name'].append(grid.xpath('*/a/text()').extract())
            item['main_bread'].append(response.xpath('//*[@class="breadcrumb-item "]/a/span/text()').extract())
            print "=======================PD:",item
            yield scrapy.Request(item['path_url'][-1],meta={'item':item},callback=self.parse_content)
            #return item
        nxtpg = response.xpath('//*[@class="navigation-button next"]/@href').extract()
        if len(nxtpg)>0:
            nextpage = nxtpg[0]
            yield scrapy.Request(nextpage,meta={'item':response.meta['item']},callback=self.parse_prod_list)

    def parse_content(self,response):
        pageinfo = response.xpath('//*[@id="hzProductInfo"]')
        item  = houzzItem()
        item['path_url']=[]
        item['path_name']=[]
        item['main_bread']=[]
        item['path_url'].extend( response.meta['item']['path_url'])
        item['path_name'] .append( response.meta['item']['path_name'])
        item['main_bread'] .append(response.meta['item']['main_bread'])
        item['product_bread'] = response.xpath('//*[@class="breadcrumb-item "]/a/span/text()').extract()
        item['product_name'] =pageinfo.xpath('*/header/*[@itemprop="name"]/text()').extract()[0]
        item['description'] = ' '.join([i.strip() for i in pageinfo.xpath('//*[@class="description"]/text()').extract()])
        item['image_urls'] = response.css('.productGalleryThumb ').xpath('ul/li/a/@href').extract()
        spec = {}
        keys = []
        values = []
        for i in pageinfo.xpath('//*[@class="productSpec"]').xpath('*//*[@class="key"]'):
            keys.append(''.join(i.xpath('span/a/text()|text()|span/text()|a/text()').extract()).strip())
        for j in pageinfo.xpath('//*[@class="productSpec"]').xpath('*//*[@class="key"]'):
            values.append(''.join(i.xpath('span/a/text()|text()|span/text()|a/text()').extract()).strip())
        if len(keys) != len(values):
            print str(keys),str(values)
        for k in range(0,len(keys)):
            spec[keys[k]]=values[k]
        item['product_spec'] = spec
        print item
        return item 
