from collections import OrderedDict
def print_weights(bias, weights):
    weight_labels = ['age', 'OSX', 'Windows', 'Linux', 'mobile', 'Google', 'Bing', 'NA ref', 'EN', 'NL', 'GE', 'NA lang', 'price', 'productid', 'green', 'blue', 'red', 'black', 'white', 'skyscraper', 'square', 'banner', '5', '15', '35', 'price_sq']

    for i, x in enumerate(weight_labels):
        print "%s: %.5f" % (x, weights[i])

    dic = OrderedDict()

    x = len(weight_labels)
    for i in range(0, len(weight_labels)):
        for j in range(i+1, len(weight_labels)):
            key = weight_labels[i] + "," + weight_labels[j]
            dic[key] = weights[x]

            #print "%s, %s: %.5f" % (weight_labels[i], weight_labels[j], self.weights[x])
            x += 1

    foo = OrderedDict(sorted(dic.iteritems(), key=lambda x: x[1]))

    for x in foo:
        if x == "price":
            print x, foo[x]

    print "Bias: %.5f" % bias
