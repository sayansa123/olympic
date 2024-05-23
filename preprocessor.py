import pandas as pd

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

def preprocess(df, region_df):
    df = df[df['Season']=='Summer']
    df = df.merge(region_df, on='NOC', how='left')
    df = df.drop_duplicates()
    temp = pd.get_dummies(df['Medal'], dtype=int)
    df = pd.concat([df , temp], axis=1)
   
    return df
    