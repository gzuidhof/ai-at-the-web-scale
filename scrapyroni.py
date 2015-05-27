import json
import urllib2
from credentials import *

base_url = 'http://krabspin.uci.ru.nl'
action = '/getcontext.json'


i = 1
run_id = 1

req_url = base_url + action + "?i={0}&runid={1}&teamid={2}&teampw={3}".format(i,run_id,TEAM_ID,PASSWORD)

swek = urllib2.urlopen(req_url)
print json.load(swek)
