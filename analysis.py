import numpy as np
import pandas as pd
from constants import *

# File used for doing some offline manual analysis
# Ignore...

def load_runid(run_id):
    dat = pd.DataFrame.from_csv('data/'+str(run_id)+'.csv',index_col=False)
    dat = dat.replace(np.nan,'NA', regex=True)
    return dat






if __name__ == '__main__':
    data = []
    for run_id in range(535):
        try:
            data.append(load_runid(run_id))
        except:
            print run_id, "fail"

    df = pd.concat(data)




    #suc = df[df['Success'] == 1]
    #en = df[df['Language'] == 'NL']
    #os = df[df['Agent'] == 'Linux']
    #ad = en[en['AdType'] == 'skyscraper']
    #hd = df[df['Header']== 5]

    #df = os




    #for field_name, types in OPTIONS_FOR_FIELD.iteritems():
    field_name = 'Language'
    types = OPTIONS_FOR_FIELD[field_name]

    for t in types: #osx, win,
        df_y = df[df[field_name] == t]

        for field_name_y, types_y in OPTIONS_FOR_FIELD.iteritems():
            if field_name == field_name_y:
                continue
            print '------\n',str(field_name)+'='+str(t), field_name_y

            for val in types_y:
                print val, df_y[df_y[field_name_y]==val]['Reward'].mean(axis=0)
                #print val, 'std', df[df[field_name_y]==val]['Reward'].std(axis=0)
                print '---'


    #for color in AD_TYPES:
    #    print color, df[df['AdType']==color]['Reward'].mean(axis=0)
    #    print color, 'std', df[df['AdType']==color]['Reward'].std(axis=0)
    #    print '---'

    #for color in HEADER_TYPES:
    #    print color, df[df['Header']==color]['Reward'].mean(axis=0)
    #    print color, 'std', df[df['Header']==color]['Reward'].std(axis=0)
    #    print '---'

    res, _ = np.histogram(df['Price'],bins=50)
    meuk = res * np.array(range(1,51))

    for i,j in zip(meuk,res):
        print str(i)+','+str(j)

    quit()
