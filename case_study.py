#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pandas import Series, DataFrame
from plotly.subplots import make_subplots
from urllib.request import urlopen
import json
import re
import streamlit as st
import plotly.io as pio
from streamlit_option_menu import option_menu
st.set_page_config(layout="wide")

# In[2]:
covid_raw=pd.read_csv(r"C:\Users\Harry Xu\Desktop\data\covid_19_clean_complete.csv")
covid=covid_raw.copy()
covid_full=pd.read_csv(r"C:\\Users\\Harry Xu\\Desktop\\data\\worldometer_data.csv")

covid=covid.groupby(['Country/Region','Date','WHO Region'])[['Confirmed','Deaths','Recovered','Active']].sum().reset_index()





covid['Date']=pd.to_datetime(covid['Date'])
covid['Months']=covid['Date'].dt.month
covid['Season']=pd.cut(covid['Months'],bins=[1,3,6,9],right=False,labels=['Winter','Spring','Summer'])
covid['Risk_level']=pd.cut(covid['Confirmed'],bins=[0,51,101,99999],right=False,labels=['low risk','medium risk','high risk'])
covid['Month_Name']=covid['Date'].dt.strftime('%B')
covid_display=covid.copy()
covid_display['Date']=covid_display['Date'].astype('str')
covid_total=pd.read_csv(r"C:\Users\Harry Xu\Desktop\data\country_wise_latest.csv")
covid_total.rename({'Confirmed':'Total_Confirmed','Deaths':'Total_Deaths','Recovered':'Total_Recovered','Active':'Total Active'},inplace=True,axis=1)
covid_total.columns=covid_total.columns.str.replace('/','').str.replace(' ','_').str.replace('%','percentage')
covid_total.rename({'Country_Region':'Country/Region','WHO_Region':'WHO Region'},inplace=True,axis=1)


g=covid.groupby(['WHO Region','Date','Months','Month_Name'])[['Confirmed','Deaths','Recovered','Active']].sum().reset_index()
g['Season']=pd.cut(g['Months'],bins=[1,3,6,9],right=False,labels=['Winter','Spring','Summer'])





with st.sidebar: 
	selected = option_menu(
		menu_title = 'Navigation Pane',
		options = ['Abstract', 'Background Information', 'Data Cleaning','Exploratory Analysis','Data Analysis', 'Conclusion', 'Bibliography'],
		menu_icon = 'arrow-down-right-circle-fill',
		icons = ['bookmark-check', 'book', 'box', 'map', 'boxes', 'bar-chart', 
		'check2-circle'],
		default_index = 0,
		)
if selected=='Abstract':
    st.title("Covid-19 Abstract")
    st.markdown("The covid dataset demonstrates an overview of this pandemic in different countries from Janurary to July in 2020,throughout the time when covid-19 is the most prevalent disease.")
    st.markdown("These data records the number confirmed,death and recovered case of 187 countries and regions along with the date of recording, which enable us to compare the trends of confirmed,death and recovered with various factors and analyse the patterns so as to give reasonable conclusions")
    st.markdown("More specifically, this case study will look into different season, different WHO Region,population and situation in three big countries.")
    
    
if selected=="Background Information":
    st.title("Background Information")
    st.caption("The dataset is downloaded from https://www.kaggle.com/datasets/imdevskp/corona-virus-report")
    st.markdown("This global pandemic,Covid-19,originally started from Wuhan,China in December 2019,spread to Asia and then the whole world in an extremely rapid pace. 2020 is the year when the pandemic came into the worst degree. As this disease had already eased in most counries nowadays, it is still essential to look back and learn how the disease developed in a such stonishing level through numbers and datas.")
    st.markdown("The start date of this dataframe is 2020-01-22	and it ends with 2020-07-27. Although it only covers the data of just half year, it's enough for us to see an noticeable tendency and make analysis")
    code='''covid_raw=pd.read_csv(r"C:\\Users\\Harry Xu\\Desktop\\data\\covid_19_clean_complete.csv")'''
    code1='''covid_full=pd.read_csv(r"C:\\Users\\Harry Xu\\Desktop\\data\\worldometer_data.csv")'''
    st.code(code,language='python')
    st.dataframe(covid_raw.head(10))
    st.markdown("We also have another supplementary dataset about the sum of each variables including total confirmed, total death,and total recovered.")
    st.code(code1,language='python')
    st.dataframe(covid_full.head(10))
    
    
    
    
if selected=="Data Cleaning":
    st.title('Data Cleaning')
    st.markdown("In order to conduct analysis smoothly, it is crucial to remove or replace any incorrect or missing values. Through data cleaning, not only the dataset will become easier to interpret, the process also help us to familarize with the information contained in it.")
    st.markdown("Luckily, the two dataframs already have no anomlous values, whereas there are still a few columns that are maily consisted of NaN values, which stands for missing values, therefore they need to be dropped.")
    st.markdown("For the covid raw dataset, we need to first deal with missing values. Through observation we can see all the columns are full except for the 'Province/State' column. This column contains too much missing values so it's appropriated to delete it")
    st.markdown("Here comes an issue, if we use scatter graphs to plot time against cases, we will come up with a very messy graph. This is beacause for the same country like China, each province/state contains differnent number of cases in one day, resulting in points overlaying. So we need to work out the total number of cases of a particular country in every day. The groupby alse drops unwanted columns like 'Province/State' that has too many missing values.")
    
    code_insert='''covid=covid.groupby(['Country/Region','Date','WHO Region'])[['Confirmed','Deaths','Recovered','Active']].sum().reset_index()'''
    
    st.code(code_insert,language='python')
    st.markdown("For the last part, it would be useful for our analysis if we rank the number of confirmed from low to high risk")
    st.code('''covid['Risk_level']=pd.cut(covid['Confirmed'],bins=[0,51,101,99999],right=False,labels=['low risk','medium risk','high risk'])''',language='python')
    st.markdown("Next step is to create more variables. One variable is Month. We can extract Month information from the date column in which we convert the values to datetime objects. From date we can also spilt them into different intervals to form Season variables")
    code3='''covid['Date']=pd.to_datetime(covid['Date'])
covid['Months']=covid['Date'].dt.month
covid['Season']=pd.cut(covid['Months'],bins=[1,3,6,9],right=False,labels=['Winter','Spring','Summer'])
covid['Month_Name']=covid['Date'].dt.strftime('%B')'''
    st.code(code3,language='python')
    st.dataframe(covid_display.head(10))
    st.markdown(f"Number of Rows: {covid.shape[0]}")
    st.markdown(f"Number of Columns: {covid.shape[1]}")
    
if selected=="Exploratory Analysis":
    st.title('Exploratory Analysis')
    st.markdown("In order to see the patter of the confirmed,death and recovered vary between countries and WHO Regions and how they change with time, graphs are a straightforward way of demonstarting these data so that we get the chance to understand them better")
    st.header('Exploring countries')
    col1,col2=st.columns([3,5])
    country_option=col1.selectbox('Select a country',covid['Country/Region'].unique())
    
    case_option=col1.selectbox('Select cases',['Confirmed','Deaths','Recovered'])
    
    fig1=px.line(covid[covid['Country/Region']==country_option],x="Date",
            y=covid.loc[covid['Country/Region']==country_option,case_option],hover_name='Date',
            title=f"{case_option} cases in {country_option} by date",height=800,width=730)
    
    col2.plotly_chart(fig1)
    col1.markdown("For initial exploration of the dataset, we can fist view the overall trend of the pandemic of each country over this period of time by line graphs before going into each factor.")
    col1.markdown("Most of the countries show an increasing tendency for all three variables, which means the disease is very infectous but isn't so lethal.")

    col1.markdown("We can have more visual effect is we use histogram that help us to see exactly the number of case in certain point of time")
    col1.markdown(" ")
    col1.markdown(" ")
    col1.markdown(" ")
    col1.markdown(" ")
    
    col_submit,col_submit_chart=st.columns([3,5])
    col_submit.markdown("Select different countries and different cases to compare. Hit the submit button to display the line graph of different countires")
    with st.form("Submit up to for countires"):
        country_option2=col_submit.multiselect('Select up to 4 country',covid['Country/Region'].unique(),key=2,max_selections=4,default=['Afghanistan'])
        case_selection=col_submit.selectbox('Select cases',('Confirmed','Deaths','Recovered'),key=3)
        submitted=st.form_submit_button("Submit to compare between different countries")
        if submitted:
            fig6=px.line(covid[covid['Country/Region'].isin(country_option2)],x='Date',y=case_selection,
                           facet_col='Country/Region',height=450,width=770,facet_col_wrap=2,facet_col_spacing=0.06,color='Country/Region')
            fig6.update_yaxes(matches=None,showticklabels=True,showgrid=True)
            col_submit_chart.plotly_chart(fig6)
    

    col3,col4=st.columns([3,5])
    col3.subheader('Using histogram to visualize')
    
    country_option1=col3.multiselect('Select up to 4 country',covid['Country/Region'].unique(),key=0,max_selections=4,default=['Afghanistan'])
    
    case_option1=col3.selectbox('Select cases',('Confirmed','Deaths','Recovered'),key=1)
    
    hist=px.histogram(covid.loc[covid['Country/Region'].isin(country_option1),[case_option1,'Country/Region','Date']],x='Date',y=case_option1,text_auto=True, height=800,width=730,facet_col='Country/Region',facet_col_wrap=2,facet_col_spacing=0.06,template='simple_white')
    
    hist.update_traces(marker_line_width=2, texttemplate="%{y:.3s}")
    hist.update_yaxes(matches=None,showticklabels=True,showgrid=True,gridcolor='black')
    col4.plotly_chart(hist)
    col3.markdown("Here we use facet histogram graphs to enable us to select mutiple countries and compare with their trend. It is very common that the number of cases peaks around July, which we will continue analysing in the 'Season' variable.")
    col3.markdown(" ")
    col3.markdown(" ")
    col3.markdown(" ")
    col3.markdown(" ")
    col3.markdown(" ")
    col3.markdown(" ")
    
    
    col_box1,col_box2=st.columns([3,5])
    col_box1.subheader("Box plot showing variation of cases in month")
    country_box=col_box1.selectbox('Select a country',covid['Country/Region'].unique(),key=8)
    case_option_box=col_box1.selectbox('Select cases',('Confirmed','Deaths','Recovered'),key=13)
    col_box1.markdown("These box plots illustrate all the unique values of cases recorded in the country in each specific month. It allows us to see the interquartile range in each month and identify the month when the pandemic had the biggest increase or decrease.")
    box1=px.box(covid.loc[covid['Country/Region']==country_box],x="Month_Name",
        y=case_option_box,hover_name='Date',hover_data=['Confirmed'],width=750)
    col_box2.plotly_chart(box1)
    
    map_col1,map_col2=st.columns([10,15])
    map_col1.subheader("Variation of cases over month on a map")
    map_select=map_col1.selectbox('Select cases',('Confirmed','Deaths','Recovered'),key=12)
    map_groupby=covid.groupby(['Country/Region','Months','Month_Name'])[["Confirmed","Deaths","Recovered"]].sum().reset_index()
    #map_groupby=pd.concat([map_groupby,pd.Series(['US1','1','January',map_groupby['Confirmed'].max(),map_groupby['Deaths'].max(),map_groupby['Recovered'].max()])])
    
    if map_select=='Confirmed':
        map_1=px.choropleth(map_groupby,color=map_select,locations='Country/Region',animation_frame='Month_Name',locationmode='country names'
                   ,color_continuous_scale=px.colors.sequential.Purples,projection='orthographic',width=700,height=700,range_color=[0,map_groupby['Confirmed'].max()])
        #map_1.update_traces(zmax=map_groupby[map_select].max(),zmin=0,zmid=map_groupby[map_select].max()/2)
        map_col2.plotly_chart(map_1)
    elif map_select=='Deaths':
        map_2=px.choropleth(map_groupby,color=map_select,locations='Country/Region',animation_frame='Month_Name',locationmode='country names'
                   ,color_continuous_scale=px.colors.sequential.Reds,projection='orthographic',width=700,height=700,range_color=[0,map_groupby['Deaths'].max()])
        #map_2.update_traces(zmax=map_groupby[map_select].max(),zmin=0,zmid=map_groupby[map_select].max()/2)
        map_col2.plotly_chart(map_2)
    elif map_select  =='Recovered':
        map_3=px.choropleth(map_groupby,color=map_select,locations='Country/Region',animation_frame='Month_Name',locationmode='country names'
                   ,color_continuous_scale=px.colors.sequential.Blues,projection='orthographic',width=700,height=700,range_color=[0,map_groupby['Recovered'].max()])
        #map_3.update_traces(zmax=map_groupby[map_select].max(),zmin=0,zmid=map_groupby[map_select].max()/2)
        map_col2.plotly_chart(map_3)
    map_col1.markdown("Scroll the frame to see the variation. Asia's color is becoming lighter through time and Americas and South-Americas' color is deepening on a larger scale")
    
    st.header('Exploring WHO Regions')
    col_check,col_check_chart=st.columns([10,15])
    col_check.caption('Check the boxes to display allotted data')
    regions=[]
    check_option=col_check.selectbox('Select cases',['Confirmed','Deaths','Recovered'],key=7)
    EM=col_check.checkbox('Eastern Mediterranean')
    E=col_check.checkbox('Europe')
    Af=col_check.checkbox('Africa')
    Am=col_check.checkbox('Americas')
    WP=col_check.checkbox('Western Pacific')
    SEA=col_check.checkbox('South-East Asia')
    if EM:
        regions.append('Eastern Mediterranean')
    if E:
        regions.append('Europe')
    if Af:
        regions.append('Africa')
    if Am:
        regions.append('Americas')
    if WP:
        regions.append('Western Pacific')
    if SEA:
        regions.append('South-East Asia')
    line_checkbox=px.line(g[g['WHO Region'].isin(regions)],x='Date',y=check_option,height=590,width=800,color='WHO Region')
    line_checkbox.add_hline(y=23566,line_dash="dot",
              annotation_text="total mean value",
              annotation_position="top left")
    col_check_chart.plotly_chart(line_checkbox)
    col_check.markdown("By selecting all regions, it is not difficult to notice that all regions shared a similiar trend of which their cases increased rapidly at first and remain stable after rapid growth. This phenomena indicates that the virus attenuated over time and became less infectious. But still, all regions showed an overall rising tendency.")
    
    
    col_hist_WHO1,col_hist_WHO2=st.columns([10,15])
    col_hist_WHO1.subheader("Number of Case in Different WHO Regions in Each Month")
    with st.form("Submit"):
        WHO_option=col_hist_WHO1.selectbox('Select cases',['Confirmed','Deaths','Recovered'],key=15)
        WHO_mutiselect=col_hist_WHO1.multiselect('Select WHO Regions',covid['WHO Region'].unique(), default=['Eastern Mediterranean'])
        submitted=st.form_submit_button("Submit to compare between different WHO Regions")
        checkbox_log1=col_hist_WHO1.checkbox("Display Log Scale",key=20)
        log_y1=False
        if checkbox_log1:
            log_y1=True
        if submitted:
            hist_group=px.histogram(g[g['WHO Region'].isin(WHO_mutiselect)],x='Month_Name',y=WHO_option,color='WHO Region',barmode='group',width=800,height=590,log_y=log_y1)
            col_hist_WHO2.plotly_chart(hist_group)
    col_hist_WHO1.markdown("Select single WHO Region to see their value in each month, or select multiple regions to compare their difference. All regions show a contineous increasing trend through the seven months.")
    
    col_month1,col_month2=st.columns([10,15])
    col_month1.subheader("Scatter distribution in Each Month")
    with st.form("Submit Months"):
        month_option=col_month1.selectbox('Select a month',covid['Month_Name'].unique())
        month_case=col_month1.selectbox('Select cases',['Confirmed','Deaths','Recovered'],key=16)
        WHO_mutiselect1=col_month1.multiselect('Select WHO Regions',covid['WHO Region'].unique(), default=['Eastern Mediterranean'],key=21)
        submitted1=st.form_submit_button("Submit to see variation of the scatter")
        checkbox_log=col_month1.checkbox("Display Log Scale")
        log_y=False
        if checkbox_log:
            log_y=True
        if submitted1:
            scatter_month=px.scatter(g[(g['Month_Name']==month_option)&g['WHO Region'].isin(WHO_mutiselect1)],x='Date',y=month_case,color='WHO Region',size_max=20,width = 800, height = 580,opacity=0.7,log_y=log_y)
            scatter_month.update_traces(marker_size=12)
            if log_y:
                scatter_month.update_yaxes(dtick=0.25,tickformat=".3s")
            col_month2.plotly_chart(scatter_month)
    col_month1.markdown("In January there was only three regions that had all three cases, whereas all regions grew to a high figure when it comes to July.")
    
    
    col_season1,col_season2=st.columns([10,15])
    col_season1.subheader("Situations of WHO Regions in different Seasons")
    with st.form("Submit Season"):
        WHO_season_option=col_season1.multiselect('Select WHO Regions',covid['WHO Region'].unique(), default=['Eastern Mediterranean'],key=22)
        season_case=col_season1.selectbox('Select cases',['Confirmed','Deaths','Recovered'],key=17)
        submitted_2=st.form_submit_button("Submit to see the number of cases in each season")
        if submitted_2:
            WHO_season=px.histogram(covid[covid['WHO Region'].isin(WHO_season_option)],x='Season',y=season_case,facet_col='WHO Region',facet_col_wrap=2,height=1000,color='Season',facet_col_spacing=0.1)
            WHO_season.update_yaxes(matches=None,showticklabels=True,showgrid=True)
            WHO_season.update_xaxes(showticklabels=True,showgrid=True,tickangle=25)
            WHO_season.for_each_annotation(lambda a: a.update(text=f'<b>{a.text.split("=")[-1]}</b>',font_size=14))
            
            col_season2.plotly_chart(WHO_season)
    col_season1.markdown("It is obvious that winter is the most common season has the most cases.")
    
    
    
    
    

    
if selected=="Data Analysis":
    st.title("Data Analysis")
    st.header("Comparing three most populated counties")
    st.markdown("Let's start with three most representative countries as they have the most population, making their pattern clearer and easier to compare and evaluate. The countries are China,India and USA")
    st.markdown("")
    st.subheader('Growth of cases by date')
    
    col5,col6,col7=st.columns([4,5,5])
    countries_3=pd.array(['India','US','China'],dtype=str)

    
    col5.markdown("Here the trends are very obvious. For confirmed cases, US and India had lines that are very alike: they all had a low figure at first and stayed relatively stable between Feburary and March, and afterward there was a sudden and sharp increase on number of confirmed. China had a distinct pattern, starting with a high figure at the beginnining but remained constant after March. The histogram next to it can make values clearer.Fluctuations and constant values can be seen directly, to which they correspond the same trend in the line graphs. The histograms show the sum of cases in 12 days across the period. US had a maximum of about 46 million in 12 days in July; India reached its maximum at about the same time with a number of 12.2 million cases. China had a smaller number of 1.19 million cases, but it was also in July")
    col5.markdown("")
    col5.markdown("")
    col5.markdown("")
    col5.markdown("For Death cases, they also followed pretty much the same pattern as confirmed cases, in which US and India continues to grow and China remaining stable after starting with a high number of cases. One thing to notice is that US and India appeared to have deaths cases in March, whereas China had already 42.9 thousands of deaths in March. On the whole, US had the biggest number of death cases after March 29th, and India had the second largest fgure after May 31th. Before these two dates China was the biggest and the second biggest respectively")
    col5.markdown("")
    col5.markdown("")
    col5.markdown("")
    col5.markdown("")
    col5.markdown("Recovered cases again repeated the trends. To summerize, China was the first country to have the pandemic, and then came US with India came last. China was also the first one to have control on the virus due to its stable line and figure")
    col5.markdown("")
    col5.markdown("")
    col5.markdown("")
    col5.markdown(" It is noticeable that all the three types of cases reached peaks between June and August, but a single histogram can't let us observe clearly the exact month that the case became maximum. In order to know their growth over month, an animation frame can be used.")
    
    
    
    
    
    scatter1=px.line(covid.loc[covid['Country/Region'].isin(countries_3)],x="Date",
            y="Confirmed",color="Country/Region",log_y=True,title='<b>Confirmed Cases in India,US and China against date</b>',
            height=400,width=450,template='simple_white',labels={'Confirmed':'<b>Number of Confirmed Cases</b>','Country/Region':'<b>Country</b>','Date':'<b>Date</b>'})
    
    fig6_1=px.histogram(covid[covid['Country/Region'].isin(countries_3)],x='Date',y='Confirmed',
                           facet_col='Country/Region',log_y=True,height=400,width=500,facet_col_wrap=1,labels={'Confirmed':'','Country/Region':'<b>Country</b>','Date':'<b>Date</b>'},template='simple_white',color='Country/Region')
    fig6_1.update_traces(marker_line_color='black',marker_line_width=1,texttemplate="%{y:.3s}")
    fig6_1.update_yaxes(title='')
    fig6_1.for_each_annotation(lambda a: a.update(text=f'<b>{a.text.split("=")[-1]}</b>',font_size=14))
    fig6_1.add_annotation(x=-0.11,y=0.4,text="<b>Total Confirmed Cases Every 12 Days</b>", textangle=-90, xref="paper", yref="paper",font_size=14
)
    

    col6.plotly_chart(scatter1)
    col7.plotly_chart(fig6_1)
    
    
    scatter2=px.line(covid.loc[covid['Country/Region'].isin(countries_3)],x="Date",
            y="Deaths",color="Country/Region",log_y=True,title='<b>Covid Deaths in India,US and China against date</b>',
            height=400,width=450,template='simple_white',labels={'Deaths':'<b>Number of Deaths</b>','Country/Region':'<b>Country</b>','Date':'<b>Date</b>'})
    
    fig6_2=px.histogram(covid[covid['Country/Region'].isin(countries_3)],x='Date',y='Deaths',
                           facet_col='Country/Region',log_y=True,height=400,width=500,facet_col_wrap=1,labels={'Deaths':'<b>Number of Deaths</b>','Country/Region':'<b>Country</b>','Date':'<b>Date</b>'},template='simple_white',color='Country/Region')
    fig6_2.update_traces(marker_line_color='black',marker_line_width=1,texttemplate="%{y:.3s}")
    fig6_2.update_yaxes(title='')
    fig6_2.for_each_annotation(lambda a: a.update(text=f'<b>{a.text.split("=")[-1]}</b>',font_size=14))
    fig6_2.add_annotation(x=-0.09,y=0.4,text="<b>Total Death Cases Every 12 Days</b>", textangle=-90, xref="paper", yref="paper",font_size=14
)
    col6.plotly_chart(scatter2)
    col7.plotly_chart(fig6_2)
    
    
    scatter3=px.line(covid.loc[covid['Country/Region'].isin(countries_3)],x="Date",
            y="Recovered",color="Country/Region",log_y=True,title='<b>Recovered Cases in India,US and China against date</b>',
            height=400,width=450,template='simple_white',labels={'Recovered':'<b>Number of Recovered Cases</b>','Country/Region':'<b>Country</b>','Date':'<b>Date</b>','Date':'<b>Date</b>'})
    fig6_3=px.histogram(covid[covid['Country/Region'].isin(countries_3)],x='Date',y='Recovered',
                           facet_col='Country/Region',log_y=True,height=400,width=500,facet_col_wrap=1,labels={'Deaths':'','Country/Region':'<b>Country</b>','Date':'<b>Date</b>'},template='simple_white',color='Country/Region')
    fig6_3.update_traces(marker_line_color='black',marker_line_width=1,texttemplate="%{y:.3s}")
    fig6_3.update_yaxes(title='')
    fig6_3.for_each_annotation(lambda a: a.update(text=f'<b>{a.text.split("=")[-1]}</b>',font_size=14))
    fig6_3.add_annotation(x=-0.09,y=0.4,text="<b>Total Recovered Cases Every 12 Days</b>", textangle=-90, xref="paper", yref="paper",font_size=14
)
    col6.plotly_chart(scatter3)
    col7.plotly_chart(fig6_3)
    
   

    
    

    
    
    hist_animation_dict={'Confirmed':[0,90000000],'Deaths':[0,4000000],'Recovered':[0,30000000]}
    col8,col9,col10=st.columns([4,5,5])
    hist_animation_option=col8.selectbox("Select a case",['Confirmed','Deaths','Recovered'],key=0)
    hist_animation=px.histogram(covid[(covid['Country/Region'].isin(countries_3))],color='Country/Region',x='Country/Region',
             y=hist_animation_option,width=450,height=450,animation_frame='Month_Name',range_y=hist_animation_dict[hist_animation_option],labels={'Country/Region':'<b>Country</b>'},title=f"<b>Number of {hist_animation_option} in Three Countries for Each Month</b>")
    hist_animation.update_yaxes(title='')
    hist_animation.add_annotation(x=-0.1,y=0.29,text=f"<b>Number of {hist_animation_option} in One Month", textangle=-90, xref="paper", yref="paper",font_size=14
)
    hist_total=px.histogram(covid[(covid['Country/Region'].isin(countries_3))],color='Country/Region',x='Country/Region',
             y=hist_animation_option,width=430,height=430,title=f"<b>Total Number of {hist_animation_option} in Three Countries</b>",labels={'Country/Region':'<b>Country</b>'})
    hist_total.update_yaxes(title='')
    hist_total.add_annotation(x=-0.12,y=0.4,text=f"<b>Total Number of {hist_animation_option}</b>", textangle=-90, xref="paper", yref="paper",font_size=14
)
    col8.markdown("let's see how the cases varies with month. The first graph in the right illustrates the total cases, and the one next to it shows their growth over each month. It is obvious that at the start of 2020, over a period of 3 months from January to March, all three countries remained a very low figure. The most siginificant rise happened around or after May, esperically for US. China, however, stayed a relatively low and stable figure compared to the other two.")
    col9.plotly_chart(hist_total)
    col10.plotly_chart(hist_animation)
    
    
    
    st.subheader("Box plot showing special values")
    st.markdown("Box graphs enable us to visualize important values in the dataframe, including maximum, minimum, median values and 25 and 75 percentile. Below are two groups of charts, one is for comparison between countries and the other is for close observation. China, dispite having many outliers, had its cases mostly concentrated in a small range. ")
    box_col1,box_col2,box_col3=st.columns([10,10,8])
    
    box_col3.markdown("")
    box_col3.markdown("")
    box_option2_1=box_col3.selectbox('Select a country',['India','US','China'],key=9)
    box_col3.markdown("Through comparison, it is evident that US has the longest interquartile range. Its maximum value is 4.29 million and its median value is 924k, and US doesn't have any outliers. India, however, has a lot outliers with a maximum number of 1.4 million and it has a median of 25.4k, which is a much smaller figure compared with the US. China also has many outliers, but they all scatter in a very small range and that is why they almost cannot be observed with the same scale as the US. Selecting China gives a much clearer image of maximum 86k. Unlike India's outliers that locate on top of the box, China's outliers are all below the lower fence.")

    box_col3.markdown("")
    box_col3.markdown("")
    box_col3.markdown("")
    box_col3.markdown("")
    box_col3.markdown("")
    box_col3.markdown("")

    box_con=px.box(covid[covid['Country/Region']==box_option2_1],y='Confirmed',width=400,height=500,color='Country/Region',color_discrete_map={'China':'#636EFA','India':'#EF553B','US':'#00CC96'},labels={'Confirmed':'<b>Confirmed</b>'})
    box_con.update_layout(showlegend=False)
    box_col2.plotly_chart(box_con)
    box_option2_2=box_col3.selectbox('Select a country',['India','US','China'],key=10)
    box_col3.markdown("For Deaths, US is still the has the longest interquartile range and has a maximum figure of 4.29 million cases and doesn't have any outliers as well. India has a maximum value of 33.4k and  India's outliers of deaths are more closely packed than the outliers of India's confirmed cases. China has a maximum value of 4656, which interstingly locates in a position in close proximity to its 75th percentile.")
    box_col3.markdown("")
    box_col3.markdown("")
    box_col3.markdown("")
    box_col3.markdown("")
    box_col3.markdown("")
    box_col3.markdown("")
    box_col3.markdown("")
    box_col3.markdown("")
    box_col3.markdown("")
    box_col3.markdown("")
    box_col3.markdown("")
    box_dea=px.box(covid[covid['Country/Region']==box_option2_2],y='Deaths',width=400,height=500,color='Country/Region',color_discrete_map={'China':'#636EFA','India':'#EF553B','US':'#00CC96'},labels={'Deaths':'<b>Deaths</b>'})
    box_dea.update_layout(showlegend=False)
    box_col2.plotly_chart(box_dea)
    box_option2_3=box_col3.selectbox('Select a country',['India','US','China'],key=11)
    box_re=px.box(covid[covid['Country/Region']==box_option2_3],y='Recovered',width=400,height=500,color='Country/Region',color_discrete_map={'China':'#636EFA','India':'#EF553B','US':'#00CC96'},labels={'Recovered':'<b>Recovered</b>'})
    box_re.update_layout(showlegend=False)
    box_col2.plotly_chart(box_re)
    box_col3.markdown("Overall, recovered cases follow the same pattern as confirmed and deaths. One thing to notice is that US's recovered cases have a median value located in a much lower position and India's recovered cases have outliers scattered futher apart instead of being close to each other like confirmed and deaths.")
    
    box2=px.box(covid[covid['Country/Region'].isin(countries_3)],x='Country/Region',y='Confirmed',color='Country/Region',width=400,height=500,labels={'Country/Region':'','Confirmed':'<b>Confirmed</b>'},title="")
    box2.update_layout(showlegend=False)
    box3=px.box(covid[covid['Country/Region'].isin(countries_3)],x='Country/Region',y='Deaths',color='Country/Region',width=400,height=500,labels={'Country/Region':'','Deaths':'<b>Deaths</b>'})
    box3.update_layout(showlegend=False)
    box4=px.box(covid[covid['Country/Region'].isin(countries_3)],x='Country/Region',y='Recovered',color='Country/Region',width=400,height=500,labels={'Country/Region':'','Recovered':'<b>Recovered</b>'})
    box4.update_layout(showlegend=False)
    box_col1.plotly_chart(box2)
    box_col1.plotly_chart(box3)
    box_col1.plotly_chart(box4)
    
    
    
    
    
    
    
    
    
    
    
    st.header("Specific factors for WHO Regions")
    st.header("The Risk Levels in Three Regions")
    st.markdown("After knowing the overall situation of the three countries, let's first outline the situation of WHO Regions in different seasons. The analysis will be bases on three regions that has the most, the least and the median value, which is Americas, Western Pacific and Eastern Mediterranean")
    col_risk1,col_risk2=st.columns([10,15])
    col_risk1.subheader("Americas")
    col_risk1.markdown("Risk_Level is divided into three sections where low risk stands for a region having less than 50 confirmed cases recorded a day;medium risk is when confirmed cases recorded a day is bigger than 50 but smaller than 100;a region is considered highly risky when it had over 100 confirmed cases recorded a day. Through the histogram, while low-level risk hold the strongest position among the three standards in the first three month, medium risk stays the lowest figure across the whole time, and high risk becomes the most recorded since April, with a peak number of 672 counts in May.")
    fig_risk1=px.histogram(covid[covid['WHO Region']=='Americas'],x='Month_Name',color='Risk_level',barmode='group',height=500,width=800,title="<b>The Amount of Low,Median,and High Risk Levels in Americas in Each Month</b>",labels={'count':'Number of Recorded Low,High,and Median Risk Levels','Month_Name':'<b>Month</b>','Risk_level':'<b>Risk_Level</b>'})
    fig_risk1.update_yaxes(title_text="<b>Number of Recorded Low,High,and Median Risk Levels</b>")
    col_risk2.plotly_chart(fig_risk1)
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.subheader("Western Pacific")
    fig_risk2=px.histogram(covid[covid['WHO Region']=='Western Pacific'],x='Month_Name',color='Risk_level',barmode='group',height=500,width=800,title="<b>The Amount of Low,Median,and High Risk Levels in Western Pacific in Each Month</b>",labels={'count':'Number of Recorded Low,High,and Median Risk Levels','Month_Name':'<b>Month</b>','Risk_level':'<b>Risk_Level</b>'})
    fig_risk2.update_yaxes(title_text="<b>Number of Recorded Low,High,and Median Risk Levels</b>")
    col_risk2.plotly_chart(fig_risk2)
    col_risk1.markdown("Western Pacific has the least number of confirmed cases among all six regions, and its pattern behaves similarily with Americas. However, unlike Ameicas where thre are no medium and high risks recorded in Janurary and Feburary, western Pacific appears to have regions that are highly risky in Janurary and all three levels of risks emerging in Feburary. The number of medium risks keeps a low figure and is zero in Janurary, April and June. Its low risk count reaches a maximum number of 393 in Feburary, and June is the month when most high risks are recorded.")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")
    col_risk1.markdown("")

    
    
    col_risk1.subheader("Eastern Mediterranean")
    fig_risk3=px.histogram(covid[covid['WHO Region']=='Eastern Mediterranean'],x='Month_Name',color='Risk_level',barmode='group',height=500,width=800,title="<b>The Amount of Low,Median,and High Risk Levels in Eastern Mediterranean in Each Month</b>",labels={'count':'Number of Recorded Low,High,and Median Risk Levels','Month_Name':'<b>Month</b>','Risk_level':'<b>Risk_Level</b>'})
    col_risk2.plotly_chart(fig_risk3)
    col_risk1.markdown("Situations in Eastern Mediterranean resembles Western Pacific: their low risk reaches highest point in Feburary and their medium risk figure reaches maximum in March and their high risk recorded the highest figure in May. The Region don't have records of medium and high risks in Janurary and don't have low and medium risks in June and July. Unexpectedly, while other two region all have medium risk being recorded the least times regardless wich month, Eastern Mediterranean's counts of meidum risks is greater than low risks in May.")
    
    
    
    
    
    col11,col12=st.columns([5,5])
    fig10=px.line(g[g['WHO Region']=='Americas'],x='Date',y='Confirmed',facet_col='Season',color='Season',facet_col_spacing=0.03)
    fig10.update_yaxes(matches=None)
    fig10.update_xaxes(matches=None)
    fig10.update_layout(xaxis=dict(tickformat="%b %d"),xaxis2=dict(tickformat="%b %d"),xaxis3=dict(tickformat="%b %d"),showlegend=False)
    
    
    
    
    
    
    
    
    
    
    sunburst=px.sunburst(covid,path=['WHO Region','Country/Region'],values='Confirmed',color='WHO Region')
    sunburst.update_traces(textinfo='percent parent+label')
    
    
    
    

    

    fig5=px.histogram(covid[(covid['Country/Region'].isin(countries_3)) & (covid['Confirmed']<50000)],x='Confirmed',color='Country/Region',
                 nbins=10,width=450,height=800,barmode='group',barnorm='percent')
    fig5.update_yaxes(title_text='')



    # In[12]:


    fig6=px.histogram(covid[covid['Country/Region'].isin(countries_3)],x='Date',y='Confirmed',
                           facet_col='Country/Region',log_y=True)
    fig6.update_traces(marker_line_color='black',marker_line_width=1)



    # In[13]:


    fig7=px.pie(covid,values='Deaths',names="WHO Region")
    fig7.update_traces(textposition='inside', textinfo='percent+label')


    # In[14]:




    # In[15]:


    fig8=px.histogram(covid[covid['Confirmed']<=9999],x='Date',y='Confirmed',color='WHO Region',barmode='overlay',
                 color_discrete_sequence=px.colors.qualitative.Light24
                 ,opacity=0.5)



    # In[16]:


    fig9=px.histogram(covid,x='Season',y='Confirmed',text_auto=True)



    # In[17]:


    WHO_season=px.histogram(covid,x='Season',y='Confirmed',facet_col='WHO Region',width=1300, height=500)
    WHO_season.update_xaxes(tickangle=25)


    # In[18]:


    fig10=make_subplots(rows=1,cols=3,subplot_titles=("Winter pandemic","Spring pandemic",'Summer pandemic'))
    for k,v in {'Winter':1,'Spring':2,'Summer':3}.items():
        fig10.add_trace(go.Scatter(x=covid.loc[(covid['Country/Region']=='US')&(covid['Season']==k),'Date'],
                                   y=covid.loc[(covid['Country/Region']=='US')&(covid['Season']==k),'Confirmed'],name=k),row=1,col=v)




    # In[19]:


    maps_1=px.choropleth(covid.groupby(['Country/Region','Months'])['Confirmed'].sum().reset_index(),
                         locations='Country/Region',animation_frame='Months',locationmode='country names',color='Confirmed',color_continuous_scale=px.colors.sequential.PuRd)



    # In[20]:


    WHO=covid.groupby(['WHO Region','Country/Region'])[['Confirmed','Deaths','Recovered']].agg([np.min,np.max,np.mean])
    
    
    
if selected=="Conclusion":
    st.title("Conclusion")
    
    
    
    
if selected=="Bibliography":
    st.title("Bibliography")


