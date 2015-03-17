# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
import numpy as np



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
        
        
        sel = Selector(response)
        
        links = sel.xpath('//a/@href').extract()
        nodes.append(url)  
        visited.append(url)
               
        
            
        for link in links:
            
            link = link.split('?')[0]            
            
            if self.valid_url(link):        
                if (url,link) not in lines:
                    lines.append( (url,link))
                if link not in nodes:
                    nodes.append(link)
                
                
            
        return None
    
    
    def closed(self,reason):

        lines = self.lines
        nodes = self.nodes        
        
        print '\n\n\n'
        print 'Amount of pages: ', len(nodes)
        print 'Amount of links: ', len(lines)
        
        indices = {page:i for i,page in enumerate(nodes)}
        
        dim = (len(nodes), len(nodes))        
        
        link_matrix = np.zeros(dim)
        
        for source, to in self.lines:
            fromIndex = indices[source]
            toIndex = indices[to]
            
            link_matrix[fromIndex,toIndex] = 1
            
            if to == 'http://www.ru.nl/artificialintelligence/master/ai-curriculum/double-degree/artificial/':
                print "yadayayadayadyadyadyadya", source
        
        sums = np.sum(link_matrix, axis=0)
        
        for i, summy in enumerate(sums):
            pass
            #print nodes[i], summy
        
        #print link_matrix
        #print self.lines
        
        #link_matrix = 
        
    
    
    def valid_url(self, url):
        return url.startswith(self.start_urls[0])
        


