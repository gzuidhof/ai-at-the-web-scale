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
    
    rules = (Rule (LxmlLinkExtractor(allow=('.*/artificialintelligence.*'),)#deny=('.*\?.*'))
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
        
        #if '?' in url:
        #    return
        sel = Selector(response)
        
        links = sel.xpath('//a/@href').extract()
        nodes.append(url)  
        visited.append(url)
               
        
            
        for link in links:
            
           # link = link.split('?')[0]            
                        
            
            
            if self.valid_url(link):        
                if (url,link) not in lines:
                    lines.append( (url,link))
                #if link not in nodes:
                   # nodes.append(link)
                
                
            
        return None
    
    
    def closed(self,reason):

        lines = self.lines
        nodes = self.nodes        
        
        print '\n\n\n'
        print 'Amount of pages: ', len(nodes)
        print 'Amount of links: ', len(lines)
        
        # Prune the links for present pages
        nl = []
        for f,t in lines:
            if t in nodes and f in nodes:
                nl.append( (f,t))
        
                
        
        X = build_link_matrix(nodes, nl)
        Q = np.zeros(X.shape)
        sums = np.sum(X, axis=1)
        
        m = X.shape[0]
        
        for i, row in enumerate(X):
            for j, entry in enumerate(row):
                sum_of_row = sums[i]
                if sum_of_row == 0:
                    Q[i,j] = 1/m
                else:
                    Q[i,j] = 1/sum_of_row
        
        print Q
        
       
        a = 0.85
        J = np.ones(X.shape)
        
        draws = np.random.uniform(size=m)
        p = draws/sum(draws)     
        
        G = a * Q + (1-a)*(J /m)
        print G
        
        p_store = []
        
        for n in xrange(50):
            p_store.append(p)
            p = p*G#np.dot(p,G)
        
        print p_store
        last = p_store[-1]
        for i, p in enumerate(last):
            print nodes[i], p
        
        #for i, summy in enumerate(sums):
            #print nodes[i], summy
            #if (summy == 0):
                #print "\n\nimpossible", nodes[i]
                
                
        
    
    
    def valid_url(self, url):
        return url.startswith(self.start_urls[0])
        


def build_link_matrix(nodes, lines):
    print 'Building link matrix'
    print 'Amount of pages: ', len(nodes)
    print 'Amount of links: ', len(lines)
    
    indices = {page:i for i,page in enumerate(nodes)}
    dim = (len(nodes), len(nodes))  
    
    link_matrix = np.zeros(dim)
        
    for source, to in lines:
        from_index = indices[source]
        to_index = indices[to]
        
        link_matrix[from_index,to_index] = 1
           
    
    return link_matrix
       
nodes = ['a','b']
lines = [('b','a')]
print np.sum(build_link_matrix(nodes, lines), axis=0)
