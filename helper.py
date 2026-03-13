import pandas as pd
import numpy as np
# import app
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False).reset_index()

    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold']=medal_tally['Gold'].astype('int')
    medal_tally['Silver']=medal_tally['Silver'].astype('int')
    medal_tally['Bronze']=medal_tally['Bronze'].astype('int')
    medal_tally['total']=medal_tally['total'].astype('int')

    return medal_tally

def country_year_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country=sorted(df['region'].dropna().unique().tolist())
    country.insert(0,'Overall')

    return years,country

def fetch_medal_tally(df,year,country):
    flag=0
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    if year=='Overall' and country=='Overall':
        temp_df=medal_df
    elif year=='Overall' and country!='Overall':
        flag=1
        temp_df=medal_df[medal_df['region']==country]
    elif year!='Overall' and country=='Overall':
        temp_df=medal_df[medal_df['Year']==int(year)]
    elif year!='Overall' and country!='Overall':
        temp_df=medal_df[(medal_df['Year']==int(year)) & (medal_df['region']== country)]

    if flag==1:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['total']=x['Gold']+x['Silver']+x['Bronze']

    x['Gold']=x['Gold'].astype('int')
    x['Silver']=x['Silver'].astype('int')
    x['Bronze']=x['Bronze'].astype('int')
    x['total']=x['total'].astype('int')

    
    return x

def participating_nation_over_time(df,season):
    # season = st.selectbox("Select Season", ["Summer", "Winter"])
    filtered_df = df[df['Season'] == season]
    # summer_df = df[df['Season'] == 'Summer']
    # nation_over_time=filtered_df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index(name='Nations').rename(columns={'index':'Year'}).sort_values('Year').reset_index(drop=True)
    nation_over_time = (
    filtered_df.groupby('Year')['region']
               .nunique()
               .reset_index(name='Nations')
               .sort_values('Year')
)

    return nation_over_time

def events(df):
    # event_df=df[df['Event']]
    event = (
    df.drop_duplicates(['Event','Year'])
      .groupby('Year')
      .size()
      .reset_index(name='Games')
      .sort_values('Year')
      .reset_index(drop=True))
    return event


def athletes(df):
    athlete=(
        df.drop_duplicates(['Year','Name']).groupby('Year').size().reset_index(name='Athletes').sort_values('Year').reset_index(drop=True)
    )
    return athlete

def most_successful(df,sport):
    temp_df=df.dropna(subset=['Medal'])

    if sport!='Overall':
        temp_df=temp_df[temp_df['Sport']==sport]

    return temp_df['Name'].value_counts().reset_index().rename(columns={'count':"Medals"}).head(15).merge(df,left_on='Name',right_on='Name',how='left')[['Name','Medals','Sport','region']].drop_duplicates('Name')


def yearwise_medal_tally(df,country):

    temp_df=df.dropna(subset=['Medal'])
    temp_df=temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    new_df=temp_df[temp_df['region']==country]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()
    

    return final_df  

def heatmap_country_tally(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df=temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    new_df=temp_df[temp_df['region']==country]
    if new_df.empty:
        print(new_df.shape)

    pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df,country):
    temp_df=df.dropna(subset=['Medal'])

    temp_df=temp_df[temp_df['region']==country]


    return temp_df['Name'].value_counts().reset_index().rename(columns={'count':"Medals"}).head(15).merge(df,left_on='Name',right_on='Name',how='left')[['Name','Medals','Sport','region']].drop_duplicates('Name')

def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name','region']).copy()
    athlete_df['Medal'] = athlete_df['Medal'].fillna('No Medal')

    if sport != 'Overall':
        return athlete_df[athlete_df['Sport'] == sport]
    else:
        return athlete_df
    
def men_v_women(df):
    new_athlete_df=df.drop_duplicates(subset=['Name','region'])

    new_athlete_df=new_athlete_df[new_athlete_df['Season']=='Summer']

    men=new_athlete_df[new_athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women=new_athlete_df[new_athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()

    final=men.merge(women,on='Year',how='left')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)

    final.fillna(0,inplace=True)

    return final





