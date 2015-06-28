import numpy as np
from constants import *

def one_hot_reverse(action_key, action_values):
    #Select first
    #selection = np.argmax(action_values)

    #Select random
    one_indices = np.flatnonzero(action_values)
    selection = np.random.choice(one_indices)


    possible_values = OPTIONS_FOR_FIELD[action_key]
    return possible_values[selection]


def decode_action(action):
    header = one_hot_reverse('Header', action[10:13])
    ad_type = one_hot_reverse('AdType', action[7:10])
    color = one_hot_reverse('Color', action[2:7])

    product = np.clip(int(np.round(action[1])), PRODUCT_MIN, PRODUCT_MAX)
    price = np.clip(action[0], PRICE_MIN, PRICE_MAX)

    return header, ad_type, color, product, price
