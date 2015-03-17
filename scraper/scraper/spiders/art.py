# -*- coding: utf-8 -*-
from scrapy import *



class ArtSpider(Spider):
    name = "art"
    allowed_domains = ["www.ru.nl"]
    start_urls = (
        'http://www.ru.nl/artificialintelligence/',
    )
    


    visited = []
    to_visit = []
    nodes = []
    lines = []
    
    meta = {"dont_redirect":True}

    def parse(self, response):
        
        url = response.url      
        
        nodes = self.nodes
        lines = self.lines
        visited = self.visited        
        to_visit = self.to_visit
        
        
        sel = Selector(response)
        print "\n------------------------------------\n"
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
            
        return self.get_next(None)
            
    def get_next(self, err):
        next = self.to_visit.pop()  
        
        #print "Next: {0}".format(next)
        return Request(next, 
                      callback = self.parse, 
                      meta = self.meta, 
                      errback = self.get_next)
        
    
    
    
    def valid_url(self, url):
        return url.startswith(self.start_urls[0])
        
    
