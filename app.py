import streamlit as st
import numpy as np
import pandas as pd
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df=preprocessor.preprocess(df,region_df)

st.sidebar.title('Olympics Analysis')
user_menue = st.sidebar.radio(
    'Select an option',
    ('Medel Tally', 'Overall Analysis','Country Wise Analysis','Athlete Wise Analysis')
)

if user_menue == 'Medel Tally':
    st.sidebar.header('Medal Tally')

    year, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year', year)
    selected_country = st.sidebar.selectbox('Select Country', country)

    if selected_country=='Overall' and selected_year=='Overall':
        st.title('Overall Tally')
    if selected_country=='Overall' and selected_year!='Overall':
        st.title(f'Year: {selected_year} ')
    if selected_country!='Overall' and selected_year=='Overall':
        st.title(f'Country: {selected_country}')
    if selected_country!='Overall' and selected_year!='Overall':
        st.title(f'{selected_country} in Year: {selected_year}')
    
    medal_tally = helper.fetch_medal_tallly(df, selected_country, selected_year)
    st.table(medal_tally)

if user_menue == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('City')
        st.title(cities)
    with col3:
        st.header('Storts')
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Atheletes')
        st.title(athletes)
    with col3:
        st.header('Nation')
        st.title(nations)

    st.header('')
    st.header('')
    nations_over_time = helper.nations_over_time(df,'region')
    fig, ax = plt.subplots()
    sns.lineplot(data=nations_over_time, x='Year', y='region', ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Countries")
    ax.set_title("Nations Participating in the Olympics Over Time")
    st.pyplot(fig)


    st.header('')
    st.header('')
    events_over_time = helper.events_over_time(df,'Event')
    fig, ax = plt.subplots()
    sns.lineplot(data=events_over_time, x='Year', y='Event', ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Events")
    ax.set_title("Total Events in the Olympics Over Time")
    st.pyplot(fig)


    st.header('')
    st.header('')
    events_over_time = helper.events_over_time(df,'Name')
    fig, ax = plt.subplots()
    sns.lineplot(data=events_over_time, x='Year', y='Name', ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Athletes")
    ax.set_title("Total Athletes in the Olympics Over Time")
    st.pyplot(fig)


    st.header('')
    st.header('')
    st.title('No of events over time (Every Sport)')
    x = helper.event_per_year_every_sport(df)
    fig, ax = plt.subplots(figsize=(20,20))
    sns.heatmap(x, annot=True)
    st.pyplot(fig)
    

    st.title('Most Successfull Athletics')
    L = np.sort(df['Sport'].drop_duplicates().unique()).tolist()
    L.insert(0,'Overall')
    sports = st.selectbox('Soprts', L)
    x = helper.most_successfull(df, sports)
    st.table(x)



if user_menue == 'Country Wise Analysis':
    st.sidebar.title('Country Wise Analysis')
    L = np.sort(df['region'].drop_duplicates().dropna().unique()).tolist()
    country = st.sidebar.selectbox('Select a country', L)
    
    x = helper.country_wise_medal_tally(df, country)
    fig, ax = plt.subplots()
    sns.lineplot(data=x, x='Year', y='Medal', ax=ax)
    st.pyplot(fig)


    pt = helper.good_performance(df, country)
    fig, ax = plt.subplots(figsize=(20,20))
    sns.heatmap(pt, annot=True)
    st.pyplot(fig)


    st.title('Most Successfull Athletics Country Wise')
    x = helper.most_successfull_country_wise(df, country)
    st.table(x)

if user_menue=='Athlete Wise Analysis':
    st.sidebar.title('Athlete Wise Analysis')
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    mm=athlete_df
    mm['Age']=athlete_df['Age'].dropna()
    fig, ax = plt.subplots()
    # fig, ax = plt.subplots(figsize=(30,20))
    # sns.kdeplot(mm[mm['Medal']=='Gold'][['Age']])
    # sns.kdeplot(mm[mm['Medal']=='Silver'][['Age']])
    # sns.kdeplot(mm[mm['Medal']=='Bronze'][['Age']])
    gold_ages = mm[mm['Medal'] == 'Gold']['Age']
    silver_ages = mm[mm['Medal'] == 'Silver']['Age']
    bronze_ages = mm[mm['Medal'] == 'Bronze']['Age']
    data = pd.DataFrame(
        {
            'Age': np.concatenate([gold_ages, silver_ages, bronze_ages]),
            'Medal':['Gold'] * len(gold_ages) + 
                    ['Silver'] * len(silver_ages) + 
                    ['Bronze'] * len(bronze_ages)
        },
    )
    sns.kdeplot(x='Age', hue='Medal', data=data, shade=True, palette='bright')
    plt.title('Age Distribution by Medal')
    plt.xlabel('Age')
    plt.ylabel('Density')
    st.pyplot(fig)



    # age vs sport
    sport = df['Sport'].drop_duplicates().dropna().tolist()
    L=[]
    name=[]
    for i in sport:
        nn=df[df['Sport']==i]
        L.append(df[df['Medal']=='Gold'][['Age']].dropna())
        name.append(i)
    fig, ax = plt.subplots()
    plt.title('Age Distribution on Sports by (w.r.t. Gold)')
    sns.kdeplot(x='Age', hue='Sport', data=df, common_norm=False)
    st.pyplot(fig)


    L = np.sort(df['Sport'].drop_duplicates().unique()).tolist()
    L.insert(0,'Overall')
    sports = st.selectbox('Select Soprts', L)
    temp_df = helper.weight_v_height(df, sports)
    fig, ax = plt.subplots()
    plt.title('Height vs Weight')
    sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex')
    st.pyplot(fig)



    final = helper.men_vs_woman(df)
    fig, ax = plt.subplots()
    plt.title('Male vs Female')
    sns.lineplot(data=final, x='Year', y='Male', label='Male', color='blue')
    sns.lineplot(data=final, x='Year', y='Female',label='Female', color='red')
    st.pyplot(fig)