from constants import *
import random
import time

def rand_proposal(context):

    header = random.choice(HEADER_TYPES)
    adtype = random.choice(AD_TYPES)
    color = random.choice(COLOR_TYPES)
    product_id = random.choice(PRODUCT)
    price = random.uniform(PRICE_MIN, PRICE_MAX)

    return  header, adtype, color, product_id, price


if __name__ == '__main__':
    import api



    for i in xrange(10000):
        header, adtype, color, product_id, price = rand_proposal(None)


        #print header, adtype, color, product_id, price
        print api.propose_page(i,0,header,adtype,color,product_id,price)

        #print api.propose_page(0, 0, 5, 'skyscraper', 'blue', 10, 25.41)
