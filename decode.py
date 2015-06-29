import numpy as np
from constants import *

def one_hot_reverse(action_key, action_values):
    #Select first
    #selection = np.argmax(action_values)

    #Select random
    one_indices = np.flatnonzero(action_values)

    #No ones, go full random
    if len(one_indices) == 0:
        one_indices = [np.random.choice(range(len(action_values)))]

    selection = np.random.choice(one_indices)


    possible_values = OPTIONS_FOR_FIELD[action_key]
    return possible_values[selection]


def decode_action(action):
    price = np.clip(action[0], PRICE_MIN, PRICE_MAX)
    product = np.clip(int(np.round(action[1])), PRODUCT_MIN, PRODUCT_MAX)

    cur = 2 #Cursor
    n_color = len(COLOR_TYPES)
    n_ad_types = len(AD_TYPES)
    n_headers = len(HEADER_TYPES)

    color = one_hot_reverse('Color', action[cur:cur+n_color])
    cur += n_color
    ad_type = one_hot_reverse('AdType', action[cur:cur+n_ad_types])
    cur += n_ad_types
    header = one_hot_reverse('Header', action[cur:cur+n_headers])

    return header, ad_type, color, product, price
