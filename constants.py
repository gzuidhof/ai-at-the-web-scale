HEADER_TYPES = [5, 15, 35]
AD_TYPES = ['skyscraper', 'square', 'banner']
COLOR_TYPES = ['green', 'blue', 'red', 'white']

#Context possibilities
AGENTS = ['OSX', 'Windows', 'Linux', 'mobile']
REFERERS = ['Google', 'Bing', 'NA']
LANGUAGES = ['EN', 'NL', 'GE', 'NA']

PRICE_MAX = 50.00
PRICE_MIN = 0.01

PRODUCT = range(10,26)
PRODUCT_MAX = PRODUCT[-1]
PRODUCT_MIN = PRODUCT[ 0]

AGE_MIN = 10
AGE_MAX = 110

#Field in JSON response to list of options mapping
OPTIONS_FOR_FIELD = {
    'Header': HEADER_TYPES,
    'AdType': AD_TYPES,
    'Color': COLOR_TYPES,

    'Agent': AGENTS,
    'Referer': REFERERS,
    'Language': LANGUAGES
}
