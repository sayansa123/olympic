import numpy as np

'''
def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['total']=medal_tally['Gold']+medal_tally['Bronze']+medal_tally['Silver']

    return medal_tally
'''
def country_year_list(df):
    years = np.sort(df['Year'].unique()).tolist()
    years.insert(0,'Overall') 
    country = np.sort(df['region'].dropna().unique()).tolist()
    country.insert(0,'Overall')
    return years,country

def fetch_medal_tallly(df,country, year):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if country == 'Overall' and year == 'Overall':
        temp_df = medal_df 
    if country == 'Overall' and year != 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]
    if country != 'Overall' and year == 'Overall':
        flag=1
        temp_df = medal_df[medal_df['region'] == country]
    if country != 'Overall' and year != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == year)]
    
    if flag==1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Bronze'] + x['Silver']
    return x

def nations_over_time(df, region):
    nations_over_time = df.drop_duplicates(subset=['Year',region])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'count':region}, inplace=True)
    return nations_over_time

def events_over_time(df, event):
    event_over_time = df.drop_duplicates(subset=['Year',event])['Year'].value_counts().reset_index().sort_values('Year')
    event_over_time.rename(columns={'count':event}, inplace=True)
    return event_over_time

def athletes_over_time(df,athletes):
    athletes_over_time = df.drop_duplicates(subset=['Year',athletes])['Year'].value_counts().reset_index().sort_values('Year')
    athletes_over_time.rename(columns={'count':athletes}, inplace=True)
    return athletes_over_time

def event_per_year_every_sport(df):
    x = df.drop_duplicates(subset=['Year','Sport','Event'])
    x2 = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
    return x2

def most_successfull(df, sport):
    temp_df = df.dropna(subset=['Medal']) 
    if sport!='Overall':
        temp_df = temp_df[temp_df['Sport']==sport]
    temp_df2 = temp_df.groupby('Name')['Medal'].count().sort_values(ascending=False).reset_index().head(20)
    temp_df3 = temp_df2.merge(df, on='Name', how='left')[['Name','Medal_x','Sport','region']].drop_duplicates()
    temp_df3.rename(columns={'Medal_x':'Total_Medal'}, inplace=True)
    return temp_df3

def country_wise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    temp_df = temp_df[temp_df['region']==country]
    temp_df = temp_df.groupby('Year')['Medal'].count().reset_index()
    return temp_df

def good_performance(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successfull_country_wise(df, country):
    temp_df = df.dropna(subset=['Medal']) 
    temp_df = temp_df[temp_df['region']==country]
    temp_df2 = temp_df.groupby('Name')['Medal'].count().sort_values(ascending=False).reset_index().head(20)
    temp_df3 = temp_df2.merge(df, on='Name', how='left')[['Name','Medal_x','Sport']].drop_duplicates()
    temp_df3.rename(columns={'Medal_x':'Total_Medal'}, inplace=True)
    return temp_df3

def weight_v_height(df, Sport):
    nn = df.drop_duplicates(subset=['Name','region'])
    nn.dropna(subset=['Medal'], inplace=True)
    if Sport=='Overall':
        return nn
    oo = nn[nn['Sport']==Sport]
    return oo

def men_vs_woman(df):
    pp = df.drop_duplicates(subset=['Name','region'])
    man = pp[pp['Sex']=='M'].groupby('Year')['Name'].count().reset_index()
    woman = pp[pp['Sex']=='F'].groupby('Year')['Name'].count().reset_index()
    final = man.merge(woman, on='Year', how='left')
    final.rename(
        columns={
            'Name_x':'Male',
            'Name_y':'Female'
        }, inplace=True
    )
    final.fillna(0, inplace=True)
    return final