import pandas as pd
import os

jfjb_path = os.listdir('H:/JFJB/JFJB_by_year')
jfjb_list = []
for one_year in jfjb_path:
    if ".csv" in one_year:
        print(one_year)
        jfjb_list.append(pd.read_csv(os.path.join('H:/JFJB/JFJB_by_year',one_year)))
jfjb_df = pd.concat(jfjb_list,ignore_index = True)
os.mkdir('./data')
jfjb_df.to_csv('./data/JFJB_combine.py',index = False,encoding = 'utf-8-sig')
