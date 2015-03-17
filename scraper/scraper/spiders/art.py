# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector




class ArtSpider(CrawlSpider):
    name = "art"
    allowed_domains = ["www.ru.nl"]
    start_urls = (
        'http://www.ru.nl/artificialintelligence/',
    )
    
    rules = (Rule (LxmlLinkExtractor(allow=('.*/artificialintelligence.*'),deny=('.*\?.*'))
    , callback="parse_link", follow= True),
    )



    visited = []
    to_visit = []
    nodes = []
    lines = []
    
    
    def parse_link(self, response):
        
        url = response.url      
        
        nodes = self.nodes
        lines = self.lines
        visited = self.visited        
        to_visit = self.to_visit
        
        sel = Selector(response)
        print "------------------------------------\n"
        #print "Now in {0}".format(url)
       # print sel.xpath('//a/@href').extract()
        
        links = sel.xpath('//a/@href').extract()
        nodes.append(url)  
        visited.append(url)
               
        
        for link in links:
            
            link = link.split('?')[0]            
            
            if self.valid_url(link):        
            
                lines.append( (url,link))
                if link not in nodes:
                    nodes.append(link)
                if link not in visited and link not in to_visit:
                    to_visit.append(link)
            
        return None
    
    
    def closed(self,reason):
        print '\n\n\n'
        print self.nodes
        print 'Amount of pages: ', len(self.nodes)
        print 'Amount of links: ', len(self.lines)
        
        #print self.lines
        
        #link_matrix = 
        
    
    
    def valid_url(self, url):
        return url.startswith(self.start_urls[0])
        


