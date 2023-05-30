#Wagner Twitter Dashboard

#Install needed Packages
from dash import Dash, html, dcc, dash_table
import pandas as pd
import plotly.express as px
import tweepy
import webbrowser
import time
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from collections import OrderedDict

#Define app with Cosmo bootstrap style
app = Dash(external_stylesheets=[dbc.themes.COSMO])

#load in data for dashboard
#Country Data
dataTable = pd.read_csv('https://raw.githubusercontent.com/alecwick4/Datasets/main/Country_Data2.csv')
#Twitter Data
wagner_tweets=pd.read_csv('https://raw.githubusercontent.com/alecwick4/Datasets/main/Wagner_Tweets.csv')
#Date Frequency
tweet_freq=pd.read_csv('https://raw.githubusercontent.com/alecwick4/Datasets/main/Tweet_Freq.csv')

#Create Visuals using plotly package
#Map Visual - Country Count
fig=px.choropleth(dataTable, locations='Country',color='Frequency',locationmode = "country names",color_continuous_scale = 'viridis', title="Number Wagner Group Tweets by Country",projection='natural earth')
#Line Chart - Date Trend
fig2=px.line(tweet_freq,x="Date",y="Freq",title="Number of Tweets in Past 7 Days",color_discrete_sequence=['#30788a'])
#Bar Chart - Country Count
fig3=px.bar(dataTable,x="Country",y="Frequency",title="Number of Tweets by Country",color_discrete_sequence=['#30788a'])

#Application Layout using html Div Structure
app.layout = html.Div([
    #Title Row
    dbc.Row([
        dbc.Col(
            html.H1("Wagner Group Twitter Tracking",style={'text-align':'center'}),width=12)
    ]),
    #Visual Row
    dbc.Row([
        #Country Count Tab
        dbc.Col([
            dcc.Tabs([
                dcc.Tab(label='World Map',children=dcc.Graph(id='example-graph',figure=fig)),
                dcc.Tab(label='Country Frequency',children=dcc.Graph(id="example-graph3",figure=fig3))
            ])
        ],width=6),
        #Date Trend Tab
        dbc.Col([
            dcc.Graph(id='example-graph2',figure=fig2)
        ],width=6)
    ]),
    #Empty Row
    dbc.Row([html.Div("")])
    ,
    #Twitter Detail Table with style attributes
    dbc.Row([
        dbc.Col([
        dash_table.DataTable(
        data=wagner_tweets.to_dict('records'),
        style_data={'whiteSpace':'normal','height':'auto'},
        columns=[{'id': c, 'name': c} for c in wagner_tweets.columns],
        page_action='none',
        #Updates Style and allow for scrolling
        style_table={'height': '300px', 'overflowY': 'auto'},
        style_cell={'textAlign':'center'},
        style_data_conditional=[
                {
                    #Alternative cell formatting
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                }
            ],
            style_header={
                'backgroundColor': 'rgb(84, 88, 90)',
                'color': 'white',
                #Bold Column Headings
                'fontWeight': 'bold'
            }
        )
        ])
    ])
])

#Run application
if __name__ == '__main__':
    app.run_server(debug=True)