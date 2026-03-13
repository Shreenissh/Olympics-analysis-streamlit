import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df=preprocessor.preprocess()
st.sidebar.title('Olympics Analysis')

user_menu=st.sidebar.radio(

    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')

)


# st.subheader("Country-wise Medal Tally")

if user_menu=='Medal Tally':
    # st.header("Medal Tally")
    years,country=helper.country_year_list(df)

    selected_year=st.sidebar.selectbox("Select your year",years)
    selected_country=st.sidebar.selectbox("Select your country",country)
    
    # st.dataframe(df)

    # st.title("Medal Tally")
    


    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year=='Overall' and selected_country=='Overall':
        st.title('Overall Tally')

    elif selected_year!='Overall' and selected_country=='Overall':
        st.title('Medal Tally in'+ str(selected_year))

    elif selected_year=='Overall' and selected_country!='Overall':
        st.title('Medal Tally for'+ selected_country)

    elif selected_year!='Overall'and selected_country!='Overall':
        st.title(f"Medal Tally for {selected_country} in {selected_year}")
    st.dataframe(medal_tally)


if user_menu=='Overall Analysis':
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]

    st.title("Top statistics")

    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    season = st.selectbox("Select Season", ["Summer", "Winter"])
    nation_over_time=helper.participating_nation_over_time(df,season)
    st.title("Participating nations over years")
    
    fig=px.line(nation_over_time,x="Year",y='Nations')
    st.plotly_chart(fig)


    st.title("Games played over years")
    event_over=helper.events(df)

    fig1=px.line(event_over,x="Year",y='Games')
    st.plotly_chart(fig1)

    athletes_over=helper.athletes(df)

    fig2=px.line(athletes_over,x='Year',y='Athletes')
    st.plotly_chart(fig2)

    st.title("No of Events over time(Every Sport)")
    fig3,ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig3)


    st.title('Most successful Athletes')
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport=st.selectbox("Select Sport",sport_list)


    x=helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu=='Country-wise Analysis':
    years, country = helper.country_year_list(df)
    st.sidebar.title(f'Select the country')
    country_select = st.sidebar.selectbox('select',country)
    country_df=helper.yearwise_medal_tally(df,country_select)
    st.title("Medal tally over the years")
    fig4=px.line(country_df,x='Year',y='Medal')
    
    st.plotly_chart(fig4)
    st.title(country_select+" " +' excels in the following sports')
    

    pt=helper.heatmap_country_tally(df,country_select)
    if pt is not None and not pt.empty:
        fig5,ax=plt.subplots(figsize=(20,20))
        sns.heatmap(pt,annot=True,ax=ax)
        st.pyplot(fig5)
    else:
        st.warning("No medal data available for this country")

    
    st.title('Top 10 athletes of your country')
    top10df=helper.most_successful_countrywise(df,country_select)
    st.table(top10df)


if user_menu=='Athlete wise Analysis':
    athlete_df=df.drop_duplicates(subset=['Name',"region"])
    x1=athlete_df['Age'].dropna()
    x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()

    fig6 = ff.create_distplot(
    [x1, x2, x3, x4],
    ['All Athletes','Gold','Silver','Bronze'],
    show_hist=False,
    show_rug=False)
    st.title('Probablity to win a medal at a particular age')

    st.plotly_chart(fig6)

    x=[]
    name=[]
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df=athlete_df[athlete_df['Sport']==sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)

    fig7=ff.create_distplot(x,name,show_hist=False,show_rug=False)
    st.title('Sports best for age')
    st.plotly_chart(fig7)



    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox("Select Sport", sport_list)

    temp_df = helper.weight_v_height(df, selected_sport).copy()

    # Clean data
    temp_df = temp_df.dropna(subset=['Weight', 'Height'])
    temp_df['Medal'] = temp_df['Medal'].fillna('No Medal')

    fig8 = px.scatter(
        temp_df,
        x='Weight',
        y='Height',
        color='Medal',
        symbol='Sex',
        hover_name='Name',
        opacity=0.8,
        title=f"Weight vs Height - {selected_sport}",
    )

    fig8.update_layout(
        xaxis_title="Weight (kg)",
        yaxis_title="Height (cm)",
        legend_title="Legend",
        template="plotly_white"
    )

    st.plotly_chart(fig8, use_container_width=True)


    final=helper.men_v_women(df)
    fig9=px.line(final,x="Year",y=['Male','Female'])
    st.plotly_chart(fig9)


    


    

    

