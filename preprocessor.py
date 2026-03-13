import pandas as pd
import os

def preprocess():
    
    base = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(base, 'athlete_events.csv'))
    region_df = pd.read_csv(os.path.join(base, 'noc_regions.csv'))

    df=df[df['Season']=='Summer']

    df=df.merge(region_df,on='NOC',how='left')

    df.drop_duplicates(inplace=True)

    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)

    return df