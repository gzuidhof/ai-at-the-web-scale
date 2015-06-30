import numpy as np
import pandas as pd
from constants import *

def load_runid(run_id):
    dat = pd.DataFrame.from_csv('data/'+str(run_id)+'.csv',index_col=False)
    dat = dat.replace(np.nan,'NA', regex=True)
    return dat






if __name__ == '__main__':
    data = []
    for run_id in range(490):
        try:
            data.append(load_runid(run_id))
        except:
            print run_id, "fail"

    df = pd.concat(data)


    #print rid0.mean(axis=0)
    #for product in PRODUCT:
        #print product, df[df['Product']==product].mean(axis=0)['Reward']
    for color in COLOR_TYPES:
        print color, df[df['Color']==color]['Reward'].mean(axis=0)
        print color, 'std', df[df['Color']==color]['Reward'].std(axis=0)
        print '---'

    for ad in AD_TYPES:
        print ad, df[df['AdType']==ad]['Reward'].mean(axis=0)
        print ad, 'std', df[df['AdType']==ad]['Reward'].std(axis=0)
        print '---'

    for hdt in HEADER_TYPES:
        print hdt, df[df['Header']==hdt]['Reward'].mean(axis=0)
        print hdt, 'std', df[df['Header']==hdt]['Reward'].std(axis=0)
        print '---'

    for agent in AGENTS:
        print agent, df[df['Agent']==agent]['Reward'].mean(axis=0)
        print agent, 'std', df[df['Agent']==agent]['Reward'].std(axis=0)
        print agent, 'count', len(df[df['Agent']==agent])
        print '---'

    for ref in REFERERS:
        print ref, df[df['Referer']==ref]['Reward'].mean(axis=0)
        print ref, 'std', df[df['Referer']==ref]['Reward'].std(axis=0)
        print ref, 'count', len(df[df['Referer']==ref])
        print '---'

    for lan in LANGUAGES:
        print lan, df[df['Language']==lan]['Reward'].mean(axis=0)
        print lan, 'std', df[df['Language']==lan]['Reward'].std(axis=0)
        print lan, 'count', len(df[df['Language']==lan])
        print '---'
        #
