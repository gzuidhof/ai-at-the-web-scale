from collections import OrderedDict
from constants import *

def print_weights(bias, weights):
    weight_labels = ['age'] + AGENTS + REFERERS + LANGUAGES + ['price','productid'] + COLOR_TYPES + AD_TYPES + HEADER_TYPES + ['price_sq']
    weight_labels = [str(x) for x in weight_labels]

    for i, x in enumerate(weight_labels):
        print "%s: %.5f" % (x, weights[i])

    return

    dic = OrderedDict()

    x = len(weight_labels)
    for i in range(0, len(weight_labels)):
        for j in range(i+1, len(weight_labels)):
            key = weight_labels[i] + "," + weight_labels[j]
            dic[key] = weights[x]

            x += 1

    # Order by weight
    foo = OrderedDict(sorted(dic.iteritems(), key=lambda x: x[1]))

    for x in foo:
        print x, foo[x]

    print "Bias: %.5f" % bias
