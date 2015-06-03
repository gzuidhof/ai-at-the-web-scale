import json
import urllib2
from credentials import *

BASE_URL = 'http://krabspin.uci.ru.nl'
CONTEXT_ACTION = '/getcontext.json'
PROPOSAL_ACTION = '/proposePage.json'
HEADER_TYPES = [5, 15, 35]
AD_TYPES = ['skyscraper', 'square', 'banner']
COLOR_TYPES = ['green', 'blue', 'red', 'black', 'white']

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
    assert productid >= 10 and productid <= 25
    assert price >= 0.0 and price <= 50.0
    
    params = "?i={0}&runid={1}&teamid={2}&teampw={3}".format(i,run_id,TEAM_ID,PASSWORD)
    params += "&header={0}&adtype={1}&color={2}&productid={3}&price={4}".format(header, adtype, color, productid, price)
    request_url = BASE_URL + PROPOSAL_ACTION + params

    response = urllib2.urlopen(request_url)
    return json.load(response)


if __name__ == '__main__':
    print get_context(0,0)
    print propose_page(0, 0, 5, 'skyscraper', 'blue', 10, 25.41)
