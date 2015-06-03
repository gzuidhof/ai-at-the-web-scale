import csv
import numpy as np
import json
import urllib2
import pandas as pd
from credentials import *
from constants import *

BASE_URL = 'http://krabspin.uci.ru.nl'
CONTEXT_ACTION = '/getcontext.json'
PROPOSAL_ACTION = '/proposePage.json'

def get_context(i=0,run_id=0):

    if i < 0 or i >10000:
        print "Warning: Possibly out of bounds i {0}".format(i)

    if run_id > 10000:
        print "Run_ID {0} higher than 10,000!".format(run_id)
        raise

    params = "?i={0}&runid={1}&teamid={2}&teampw={3}".format(i,run_id,TEAM_ID,PASSWORD)
    request_url = BASE_URL + CONTEXT_ACTION + params

    response = urllib2.urlopen(request_url)
    return json.load(response)

def propose_page(i, run_id, header, adtype, color, productid, price):
    if i < 0 or i >10000:
        print "Warning: Possibly out of bounds i {0}".format(i)

    header = int(header)

    assert run_id < 10001
    assert header in HEADER_TYPES
    assert adtype in AD_TYPES
    assert color in COLOR_TYPES
    assert productid >= PRODUCT_MIN and productid <= PRODUCT_MAX
    assert price >= PRICE_MIN and price <= PRICE_MAX

    params = "?i={0}&runid={1}&teamid={2}&teampw={3}".format(i,run_id,TEAM_ID,PASSWORD)
    params += "&header={0}&adtype={1}&color={2}&productid={3}&price={4}".format(header, adtype, color, productid, price)
    request_url = BASE_URL + PROPOSAL_ACTION + params

    response = urllib2.urlopen(request_url)
    return json.load(response)
    
def reward(prices, clicks):
    """
    Calculates the reward of a single run.
    
    param `prices`: a vector of price_i values
    param `clicks`: a vector of successes for each i (either 0 or 1)
    """
    return np.sum(prices * clicks)

if __name__ == '__main__':
    context_list = []
    
    for i in range(10000):
        context = get_context(i = i, run_id = 0)['context']
        context_list.append(context)
        
        #success = propose_page(i = i, runid = 0, 5, 'skyscraper', 'blue', 10, 25.41)['effect']['Success']

    with open('meuk.csv', 'wb') as f:
        w = csv.DictWriter(f, context_list[0].keys())
        w.writeheader()
        for d in context_list:
            w.writerow(d)
