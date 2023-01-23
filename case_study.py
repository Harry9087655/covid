#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
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
covid['Risk_level']=pd.cut(covid['Confirmed'],bins=[0,51,101,99999],right=False,labels=['Low Risk','Medium Risk','High Risk'])
covid['Month_Name']=covid['Date'].dt.strftime('%B')
covid_display=covid.copy()
covid_display['Date']=covid_display['Date'].astype('str')
covid_total=pd.read_csv(r"C:\Users\Harry Xu\Desktop\data\country_wise_latest.csv")
covid_total.rename({'Confirmed':'Total_Confirmed','Deaths':'Total_Deaths','Recovered':'Total_Recovered','Active':'Total Active'},inplace=True,axis=1)
covid_total.columns=covid_total.columns.str.replace('/','').str.replace(' ','_').str.replace('%','percentage')
covid_total.rename({'Country_Region':'Country/Region','WHO_Region':'WHO Region'},inplace=True,axis=1)


g=covid.groupby(['WHO Region','Date','Months','Month_Name'])[['Confirmed','Deaths','Recovered','Active']].sum().reset_index()
g['Season']=pd.cut(g['Months'],bins=[1,3,6,9],right=False,labels=['Winter','Spring','Summer'])
avg_groupby=covid.groupby(['WHO Region','Months','Month_Name'])[['Confirmed','Deaths','Recovered']].mean().reset_index()
avg_groupby['Real Confirmed']=avg_groupby['Confirmed']-avg_groupby['Recovered']
avg_groupby['Real Confirmed Percentage']=avg_groupby['Real Confirmed']/avg_groupby['Confirmed']
avg_groupby['Real Confirmed Percentage']=avg_groupby['Real Confirmed Percentage'].fillna(0)



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
    st.markdown("More specifically, this case study will look into situation in three big countries and different WHO Regions.")
    
    
if selected=="Background Information":
    st.title("Background Information")
    st.markdown("This global pandemic,Covid-19,originally started from Wuhan,China in December 2019,spread to Asia and then the whole world in an extremely rapid pace. 2020 is the year when the pandemic came into the worst degree. As this disease had already eased in most counries nowadays, it is still essential to look back and learn how the disease developed in a such stonishing level through numbers and datas.")
    st.markdown("Since the outbreak of this pandemic in 2019, this virus had been continually evolving and adapting, and so did we. Recently, the virus has already evovled into multiple trees of variants, in which the most prevailing one was the Omicron Variant. It was reported that 'In early 2023, a new rising Omicron subvariant called XBB.1.5 appears to be the most transmissible strain of the virus so far<sup>1</sup>', and although it remains less deadly as previous variants,'the Omicron variant has been found to carry a higher risk of reinfection compared to other variants<sup>2</sup>', signalling a greater potential of spreading among children and elderly people. It is important not to disregard these new variants. However, situations do not seem better nowadays, given that 'Cases are also believed to be rising with people spending more time in doors and attending recent holiday gatherings, with fewer wearing masks and taking other mitigation measures<sup>1</sup>.' In order to predict what may happen in the following months, I found this datafram that covers the information of covid in seven months from 2020-01-22 to 2020-07-27. Despite having only seven months, it's enough for us to see an noticeable tendency and make analysis. And then we may know what kind of pattern the pandemic may vary in differnt regions.",unsafe_allow_html=True)
    st.markdown("At the beginning two years of this pandemic killed nearly 15 million people and was awfully dreadful and leathal to humans, espeically in 2020. The fist vaccine that had 94% efficacy was put into use in December,2020, which first gave us the opportunity to confront this virus<sup>3</sup>. But before then, the disease contained too much uncertainty and brought panic. Nevertheless, 'Breakthrough infections are possible with the Omicron variant even if you’re fully vaccinated.<sup>2</sup>'",unsafe_allow_html=True)
    st.markdown("Luckily, covid at present is no bigger than a cold or a fever and it become less infectious. In a recent survey from World Health Orgainzation, it was reported that 'nearly 2.9 million new cases and over 11 000 deaths were reported in the week of 2 to 8 January 2023. This represents a reduction in weekly cases and deaths of 9% and 12%, respectively<sup>4</sup>.' Although the figure still sounds big, through the following analysis, we will be able to see how worse the situation was in major regions or countries.",unsafe_allow_html=True)
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
            title=f"<b>{case_option} cases in {country_option} by date</b>",height=800,width=730)
    fig1.update_yaxes(title_text=f"<b>Number of {case_option}</b>")
    fig1.update_xaxes(title_text='<b>Date</b>')
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
                           facet_col='Country/Region',height=450,width=770,facet_col_wrap=2,facet_col_spacing=0.06,color='Country/Region',labels={'Country/Region':'<b>Country/Region</b>','Confirmed':'<b>Number of Confirmed</b>','Deaths':'<b>Number of Deaths','Recovered':'<b>Number of Recovered</b>'})
            fig6.for_each_annotation(lambda a: a.update(text=f'<b>{a.text.split("=")[-1]}</b>',font_size=14))
            col_submit_chart.plotly_chart(fig6)
    

    col3,col4=st.columns([3,5])
    col3.subheader('Using histogram to visualize')
    
    country_option1=col3.multiselect('Select up to 4 country',covid['Country/Region'].unique(),key=0,max_selections=4,default=['Afghanistan'])
    
    case_option1=col3.selectbox('Select cases',('Confirmed','Deaths','Recovered'),key=1)
    
    hist=px.histogram(covid.loc[covid['Country/Region'].isin(country_option1),[case_option1,'Country/Region','Date']],x='Date',y=case_option1,text_auto=True, height=800,width=730,facet_col='Country/Region',facet_col_wrap=2,facet_col_spacing=0.06,template='simple_white',color='Country/Region',labels={'Confirmed':'','Deaths':'','Recovered':'','Country/Region':'<b>Country/Region</b>','Date':'<b>Date</b>'},title=f"<b>Number of {case_option1} in Different Countries by Date</b>")
    hist.update_yaxes(title_text='')
    hist.update_layout(title_x=0.5)
    hist.for_each_annotation(lambda a: a.update(text=f'<b>{a.text.split("=")[-1]}</b>',font_size=14))
    hist.add_annotation(x=-0.08,y=0.5,text=f"<b>Total Number of {case_option1}</b>", textangle=-90, xref="paper", yref="paper",font_size=18)
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
    box1=px.box(covid.loc[covid['Country/Region']==country_box],x="Month_Name",title='<b>Box Plot in Each Month</b>',
        y=case_option_box,hover_name='Date',hover_data=['Confirmed'],width=750,labels={'Confirmed':'<b>Number of Confirmed</b>','Month_Name':'<b>Month</b>'})
    col_box2.plotly_chart(box1)
    
    map_col1,map_col2=st.columns([10,15])
    map_col1.subheader("Variation of cases over month on a map")
    map_select=map_col1.selectbox('Select cases',('Confirmed','Deaths','Recovered'),key=12)
    map_groupby=covid.groupby(['Country/Region','Months','Month_Name'])[["Confirmed","Deaths","Recovered"]].sum().reset_index()
    #map_groupby=pd.concat([map_groupby,pd.Series(['US1','1','January',map_groupby['Confirmed'].max(),map_groupby['Deaths'].max(),map_groupby['Recovered'].max()])])
    
    if map_select=='Confirmed':
        map_1=px.choropleth(map_groupby,color=map_select,locations='Country/Region',animation_frame='Month_Name',locationmode='country names'
                   ,color_continuous_scale=px.colors.sequential.Purples,projection='orthographic',width=700,height=700,range_color=[0,map_groupby['Confirmed'].max()],labels={'Month_Name':'Month','Confirmed':'<b>Confirmed</b>'})
        #map_1.update_traces(zmax=map_groupby[map_select].max(),zmin=0,zmid=map_groupby[map_select].max()/2)
        map_col2.plotly_chart(map_1)
    elif map_select=='Deaths':
        map_2=px.choropleth(map_groupby,color=map_select,locations='Country/Region',animation_frame='Month_Name',locationmode='country names'
                   ,color_continuous_scale=px.colors.sequential.Reds,projection='orthographic',width=700,height=700,range_color=[0,map_groupby['Deaths'].max()],labels={'Month_Name':'Month','Deaths':'<b>Deaths</b>'})
        #map_2.update_traces(zmax=map_groupby[map_select].max(),zmin=0,zmid=map_groupby[map_select].max()/2)
        map_col2.plotly_chart(map_2)
    elif map_select  =='Recovered':
        map_3=px.choropleth(map_groupby,color=map_select,locations='Country/Region',animation_frame='Month_Name',locationmode='country names'
                   ,color_continuous_scale=px.colors.sequential.Blues,projection='orthographic',width=700,height=700,range_color=[0,map_groupby['Recovered'].max()],labels={'Month_Name':'Month','Recovered':'<b>Recovered</b>'})
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
    check_log=col_check.checkbox("Display Log Scale",key=25)
    logy=False
    if check_log:
        logy=True
    line_checkbox=px.line(g[g['WHO Region'].isin(regions)],x='Date',y=check_option,height=590,width=800,color='WHO Region',labels={'Date':'<b>Date</b>','Confirmed':'<b>Confirmed</b>','WHO Region':'<b>WHO Region</b>'},log_y=logy,title=f'<b>Number of {check_option} in Different WHO Regions')
    line_checkbox.update_layout(title_x=0.5)
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
            hist_group=px.histogram(g[g['WHO Region'].isin(WHO_mutiselect)],x='Month_Name',y=WHO_option,color='WHO Region',barmode='group',width=800,height=590,log_y=log_y1,labels={'Month_Name':'<b>Month</b>','WHO Region':'<b>WHO Region</b>'},title=f'<b>Number of {WHO_option} in Different WHO Regions by Months</b>')
            hist_group.update_yaxes(title_text='<b>Number of Confirmed</b>')
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
            scatter_month=px.scatter(g[(g['Month_Name']==month_option)&g['WHO Region'].isin(WHO_mutiselect1)],x='Date',y=month_case,color='WHO Region',size_max=20,width = 800, height = 580,opacity=0.7,log_y=log_y,title=f'<b>Scatter of {month_case} of Different WHO Regions by Date</b>',labels={'Confirmed':'<b>Number of Confirmed</b>','Date':'<b>Date</b>'})
            scatter_month.update_traces(marker_size=12)
            if log_y:
                scatter_month.update_yaxes(dtick=0.25,tickformat=".3s")
            col_month2.plotly_chart(scatter_month)
    col_month1.markdown("In January there was only three regions that had all three cases, whereas all regions grew to a high figure when it comes to July.")
    
    
    col_season1,col_season2=st.columns([12,15])
    col_season1.subheader("Situations of WHO Regions in different Seasons")
    season_case=col_season1.selectbox('Select cases',['Confirmed','Deaths','Recovered'],key=17)
    WHO_season=px.histogram(covid,x='Season',y=season_case,facet_col='WHO Region',facet_col_wrap=2,height=1000,color='Season',facet_col_spacing=0.1,title=f'<b>Number of {season_case} in Each Season</b>',labels={'Season':'<b>Season</b>'})
    WHO_season.update_yaxes(matches=None,showticklabels=True,showgrid=True,title_text='')
    WHO_season.update_xaxes(showticklabels=True,showgrid=True,tickangle=25)
    WHO_season.for_each_annotation(lambda a: a.update(text=f'<b>{a.text.split("=")[-1]}</b>',font_size=14))
    WHO_season.update_layout(yaxis=dict(title_text=f'<b>Total Number of {season_case}'),
                             yaxis3=dict(title_text=f'<b>Total Number of {season_case}'),
                             yaxis5=dict(title_text=f'<b>Total Number of {season_case}'),)      
    col_season2.plotly_chart(WHO_season)
    col_season1.markdown("It is obvious that Summer is the most common season has the most cases. In all regions except Western Pacific, Summer's figure is four or more times bigger than Spring.")
    
    
    
    
    

    
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
             y=hist_animation_option,width=450,height=450,animation_frame='Month_Name',range_y=hist_animation_dict[hist_animation_option],labels={'Country/Region':'<b>Country</b>','Month_Name':'Month'},title=f"<b>Number of {hist_animation_option} in Three Countries for Each Month</b>")
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
    fig_risk2.update_yaxes(title_text="<b>Number of Confirmed Cases</b>")
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
    fig_risk3.update_yaxes(title_text="<b>Number of Confirmed Cases</b>")
    col_risk2.plotly_chart(fig_risk3)
    col_risk1.markdown("Situations in Eastern Mediterranean resembles Western Pacific: their low risk reaches highest point in Feburary and their medium risk figure reaches maximum in March and their high risk recorded the highest figure in May. The Region don't have records of medium and high risks in Janurary and don't have low and medium risks in June and July. Unexpectedly, while other two region all have medium risk being recorded the least times regardless wich month, Eastern Mediterranean's counts of meidum risks is greater than low risks in May.")
    
    
    
    
    st.header("Comparing the Mean Number of Confirmed and Recovered in Three Regions")
    col_line1,col_line2=st.columns([10,15])
    col_line1.subheader('Americas')
    col_line1.markdown("The graph beside depicts the average number of confirmed cases in each month by lines and the average number of deaths in each month by bars. Americas has a very smooth growth of the average confirmed cases over the seven months, and the same phenomena appears on recovered cases. Americas' average number of confirmed and recovered are the highest among all regions, with the most significant rise of the confirmed cases from 115k in June to 202k in July and the recovered cases from 44k in June to 97k in July. Although throughtout this period of time, confirmed cases continue to stay two or more times bigger than recovered cases as both of them increase by twofold in consective months.")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    line3=go.Figure()
    line3.add_trace(go.Scatter(x=avg_groupby.loc[avg_groupby['WHO Region']=='Americas','Month_Name'],
                           y=avg_groupby.loc[avg_groupby['WHO Region']=='Americas','Confirmed'], mode='lines+markers',
                           line_color='crimson',name='Confirmed'))
    line3.add_trace(go.Bar(x=avg_groupby.loc[avg_groupby['WHO Region']=='Americas','Month_Name'],
                           y=avg_groupby.loc[avg_groupby['WHO Region']=='Americas','Recovered'],marker_color='steelblue',
                      name='Recovered'))
    line3.update_layout(autosize=False,width=800,height=500,title_text='<b>Average Number of Confirmed and Recovered Cases in Americas</b>')
    line3.update_xaxes(title_text='<b>Month</b>')
    line3.update_yaxes(title_text='<b>Number of Cases</b>')
    col_line2.plotly_chart(line3)
    col_line1.subheader("Western Pacific")
    col_line1.markdown("Western Pacific is a lot distinct from the other two. Western Pacific's line of Confirmed has a relatively steady gradient and is growing less intensely as Americas. Howevr, before May, Western Pacific's figures of Confirmed and Recovered stay the highest. The most prominet growth of the recovered cases in Western Pacific is between Feburary and March when the number jumps by fivefold from 780 to 4000. By contrast, confirmed cases don't have such a big leap, and it only increases 2000 more cases. After March, the amount of increase stays constant around 2000 and so do the confirmed cases.")
    line4=go.Figure()
    line4.add_trace(go.Scatter(x=avg_groupby.loc[avg_groupby['WHO Region']=='Western Pacific','Month_Name'],
                           y=avg_groupby.loc[avg_groupby['WHO Region']=='Western Pacific','Confirmed'], mode='lines+markers',
                          line_color='crimson',name='Confirmed'))
    line4.add_trace(go.Bar(x=avg_groupby.loc[avg_groupby['WHO Region']=='Western Pacific','Month_Name'],
                           y=avg_groupby.loc[avg_groupby['WHO Region']=='Western Pacific','Recovered'],
                      marker_color='steelblue',name='Recovered'))
    line4.update_layout(autosize=False,width=800,height=500,title_text='<b>Average Number of Confirmed and Recovered Cases in Western Pacific</b>')
    line4.update_xaxes(title_text='<b>Month</b>')
    line4.update_yaxes(title_text='<b>Number of Cases</b>')
    col_line2.plotly_chart(line4)
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.markdown("")
    col_line1.subheader("Eastern Mediterranean")
    col_line1.markdown("Eastern Mediterranean has the lowest figures in three regions, yet its paths are very analogous to Americas'. The confirmed line becomes steeper over months, and recovered cases increases by twofold or more. Average number of recovered cases in March is 267, which then bursts into 2555 in April, and similar trend also appears in Americas. Unlike confirmed cases that gain increasing percentage of increase in figure, percentage of rise of recovered cases reduces over month: from March to April the increase is tenfold, from April to May the increase is threefold, and from June to July the increase in twofold.")
    line5=go.Figure()
    line5.add_trace(go.Scatter(x=avg_groupby.loc[avg_groupby['WHO Region']=='Eastern Mediterranean','Month_Name'],
                           y=avg_groupby.loc[avg_groupby['WHO Region']=='Eastern Mediterranean','Confirmed'], mode='lines+markers',
                          line_color='crimson',name='Confirmed'))
    line5.add_trace(go.Bar(x=avg_groupby.loc[avg_groupby['WHO Region']=='Eastern Mediterranean','Month_Name'],
                           y=avg_groupby.loc[avg_groupby['WHO Region']=='Eastern Mediterranean','Recovered'],
                      marker_color='steelblue',name='Recovered'))
    line5.update_layout(autosize=False,width=800,height=500,title_text='<b>Average Number of Confirmed and Recovered Cases in Eastern Mediterran</b>')
    line5.update_xaxes(title_text='<b>Month</b>')
    line5.update_yaxes(title_text='<b>Number of Cases</b>')
    col_line2.plotly_chart(line5)
    
    

    
    
    
    
    st.header("Percentage of Confirmed Cases as Real Confirmed")
    st.markdown("Above we see the variation of confirmed cases and recovered cases. Although confirmed cases always keep a rising tendency, but actually we can understand the situation better through real confirmed. Real Confirmed is Confirmed minus Recovered, which stands for the number of patients who still have that disease in that certain period of time. If we caculate the percentage of real confirmed, which is Real Confirmed/Confirmed.")
    col_sub1,col_sub2=st.columns([15,12])
    col_sub2.markdown("Although all regions show decreasing trend,from Janurary to Feburary Americas' percentage decreases, indicating there's more percentage recovered in Feburary. Then the bars' height become lower and lower, which signals the drop of the percentage of real confirmed, reflecting that the percentage recovered is increasing. This hidden phenomena alludes that superficially confirmed cases are rising, but at the same time the percentage of recovered is increasing as well, leading to less and less percentage of real confirmed.")
    col_sub2.markdown("")
    sub=make_subplots(rows=1, cols=3,
    specs=[[{'type':'domain'}, {'type':'domain'},{'type':'domain'}]],subplot_titles=("<b>Americas</b>","<b>Eastern Mediterranean</b>", "<b>Western Pacific</b>"))
    sub.add_trace(go.Pie(labels=['Real Confirmed','Recovered'],values=[245191750,157069444],marker=dict(colors=['gold','mediumturquoise'],line=dict(color='#000000', width=2)),hovertemplate = "<b>%{label}</b> <br>%{value:.5s} <br>%{percent}<extra></extra>"),row=1,col=1)
    sub.add_trace(go.Pie(labels=['Real Confirmed','Recovered'],values=[26032189,74082892],marker=dict(colors=['gold','mediumturquoise'],line=dict(color='#000000', width=2)),hovertemplate = "<b>%{label}</b> <br>%{value:.5s} <br>%{percent}<extra></extra>"),row=1,col=2)
    sub.add_trace(go.Pie(labels=['Real Confirmed','Recovered'],values=[7512461,26374411],marker=dict(colors=['gold','mediumturquoise'],line=dict(color='#000000', width=2)),hovertemplate = "<b>%{label}</b> <br>%{value:.5s} <br>%{percent}<extra></extra>"),row=1,col=3)
    sub.update_layout(
    autosize=False,
    width=1200,
    height=530,title_x=0.5,
    legend=dict(yanchor="top",y=0.99,xanchor="right",x=0.01,bordercolor="Black",borderwidth=2))
    hist3=px.histogram(avg_groupby[avg_groupby['WHO Region'].isin(['Americas','Western Pacific','Eastern Mediterranean'])],x='Month_Name',y='Real Confirmed Percentage',
                  barmode='group',color='WHO Region',template='simple_white',height=530,width=750,labels={'Month_Name':'<b>Month</b>'})
    hist3.update_layout(bargap=0.43,title_x=0.5,legend_title_text='<b>WHO Region</b>',title_text="<b>Percentage of Real Confirmed in Total Confirmed</b>",legend=dict(yanchor="top",y=0.99,xanchor="right",x=0.99,bordercolor="Black",borderwidth=2))
    hist3.update_yaxes(title_text='<b>Percentage of Real Confirmed</b>')
    col_sub1.plotly_chart(hist3)
    st.plotly_chart(sub)


    
    
    
    

    
    
    
if selected=="Conclusion":
    st.title("Conclusion")
    st.markdown("Throughout the analysis, 2020 was found to be a difficult year in fighting against covid. Some countries suffered at the start of the year, while others' situation grew worse later on. On the whole, all cases are growing in this year, but actually circumstances was becoming better. But now its too soon to say that the virus has little threat, as")
    
    
    
    
if selected=="Bibliography":
    st.title("Bibliography")
    st.markdown("The dataset is downloaded from https://www.kaggle.com/datasets/imdevskp/corona-virus-report , date accessed, 2023-01-18")
    st.markdown("[1] Omicron and its Subvariants: A Guide to What We Know. Yale Medicine. By Kathy Katella Janurary 6, 2023. https://www.yalemedicine.org/news/5-things-to-know-omicron")
    st.markdown("[2] Variants of Coronavirus. WebMD. By Kendall K. Morgan. https://www.webmd.com/covid/coronavirus-strains")
    st.markdown("[3] COVID-19 Vaccine Development: Behind the Scenes. Nation Health Institute. https://covid19.nih.gov/news-and-stories/vaccine-development , date accessed, 2023-01-18")
    st.markdown("[4] Weekly epidemiological update on COVID-19 - 11 January 2023. World Health Orgainzation, January, 11, 2023. https://www.who.int/publications/m/item/weekly-epidemiological-update-on-covid-19---11-january-2023 , date accessed, 2023-01-18")
    


