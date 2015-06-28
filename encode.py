import numpy as np
from constants import *


def encode_context(context):
    context_vector = np.array([context['Age']])

    # One-hot encoding
    agent_encoding = one_hot('Agent', context['Agent'])
    ref_encoding = one_hot('Referer', context['Referer'])
    lang_encoding = one_hot('Language', context['Language'])

    #Join encodings
    encodings = np.concatenate((agent_encoding, ref_encoding, lang_encoding))

    #Append encodings to context vector
    context_vector = np.concatenate((context_vector, encodings))

    return context_vector

def encode_action(action):
    action_vector = np.array([action[4], action[3]]) #price, product_id

    color_encoding = one_hot('Color', action[2])
    adtype_encoding = one_hot('AdType', action[1])
    header_encoding = one_hot('Header', action[0])

    encodings = np.concatenate((color_encoding, adtype_encoding, header_encoding))

    action_vector = np.concatenate((action_vector, encodings))

    return action_vector


def one_hot(context_key, value):
    possible_values = OPTIONS_FOR_FIELD[context_key]

    v = np.zeros(len(possible_values))
    v[possible_values.index(value)] = 1
    return v
