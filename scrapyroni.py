import json
import urllib2
from credentials import *

BASE_URL = 'http://krabspin.uci.ru.nl'
CONTEXT_ACTION = '/getcontext.json'

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


if __name__ == '__main__':
    print get_context(0,0)
