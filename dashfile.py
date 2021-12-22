#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 09:09:07 2021

@author: arpanshrivastava
"""
#Import data 
import pandas as pd 
df = pd.read_excel('Final NBA DataSet.xlsx', sheet_name='All')
df_variables = pd.read_excel('Final NBA DataSet.xlsx', sheet_name='Variable Meanings')

#Final Dashboard Code

import pandas as pd
import plotly.express as px
import numpy as np
from jupyter_dash import JupyterDash
from dash import dcc
from dash import html 
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import statsmodels.api as sm
import plotly.graph_objects as go
from dash import Input, Output, State, html
from dash import dash_table
from dash_canvas import DashCanvas
from collections import OrderedDict

app = JupyterDash(__name__, external_stylesheets=[dbc.themes.MORPH])
app.config.suppress_callback_exceptions=True

#Data 
df = pd.read_excel('Final NBA DataSet.xlsx', sheet_name='All')
df2 = df.groupby("Team")[["Team", "Wins"]].sum()
df2 = df2.rename(columns={'Wins': 'Combined 2013-2019 Wins', 'Team': 'Teams'})
df2.reset_index(inplace=True)
df_variables = pd.read_excel('Final NBA DataSet.xlsx', sheet_name='Variable Meanings')

#Figures
fig1 = pd.read_excel('Final NBA DataSet.xlsx', sheet_name='All', usecols=['Team','Year','Wins','Field Goal %'])
fig0 = pd.read_excel('Final NBA DataSet.xlsx', sheet_name='All', usecols=['Team','Year','Wins','TRB'])
fig2 = px.scatter(df, x="Wins", y="ORtg", color="Team", facet_col="Year", facet_col_wrap=4, trendline="ols", trendline_scope="overall")
fig2.add_layout_image(
    dict(
        source="https://raw.githubusercontent.com/timaboderin/NBA_Logos/master/new_team.png",
        xref="paper", yref="paper",
        x=1.40, y=1.03,
        sizex=0.12, sizey=1.35,
        xanchor="right", yanchor="bottom"
    )
)
fig2.update_layout(title = {'text': 'Wins vs Offensive Rating',
                           'y':.95, 'x':0.5, 
                           'xanchor': 'center', 
                           'yanchor': 'top'})
fig2.add_annotation(text="Correlation=.654",
                  xref="paper", yref="paper",
                  x=0.999, y=0.25, showarrow=False)

fig3 = px.sunburst(df, path=['Luxury Tax', 'Team'], values='Total Team Salary',
                  color='Wins', hover_data=['Wins'])
fig3.update_layout(title = {'text': 'Wins vs Luxury Tax',
                           'y':.95, 'x':0.5, 
                           'xanchor': 'center', 
                           'yanchor': 'top'})
fig4 = go.Figure(data=go.Heatmap(
        z=df['Wins'],
        x=df['Year'],
        y=df['Luxury Tax'],
        colorscale='Viridis', 
        hovertemplate='Offensive Rating: %{x}<br>Defensive Rating: %{y}<br>Wins: %{z}<br>'))

fig4.update_layout(title = {'text': 'Wins vs Luxury Tax',
                           'y':.95, 'x':0.5, 
                           'xanchor': 'center', 
                           'yanchor': 'top'},
                   xaxis_title="Season",
                   yaxis_title="Luxury Tax (Binary)",
                   xaxis_nticks=8,
                   yaxis_nticks=3,)
fig5 = px.scatter_geo(df, lat=df["Latitude"], lon=df["Longitude"], color=df["Wins"], hover_name=df["Team"], 
                      hover_data={"Team":True, "Year":True, "Wins":True, "Latitude":False, "Longitude":False}, 
                      size=df["Wins"],
                      animation_frame=df["Year"],
                      projection='natural earth', 
                      scope='north america')
fig5.update_layout(title = {'text': 'Wins vs Team Location by Season',
                           'y':.95, 'x':0.5, 
                           'xanchor': 'center', 
                           'yanchor': 'top'})
fig5.add_layout_image(
    dict(
        source="https://raw.githubusercontent.com/timaboderin/NBA_Logos/master/new_team.png",
        xref="paper", yref="paper",
        x=.1, y=1,
        sizex=0.12, sizey=1.35,
        xanchor="right", yanchor="bottom"))
        
fig6 = px.area(df, x="Wins", y="Attend/Game", color="Team", line_group="Year")
fig6.update_layout(title = {'text': 'Wins vs Attendance Per Game',
                           'y':.95, 'x':0.5, 
                           'xanchor': 'center', 
                           'yanchor': 'top'})




fig8 = go.Figure()
fig8.add_trace(go.Bar(x=['3P%','AST','STL','ORtg','Field Goal %'], y=[.698,.415,.414,.395,.346],
                marker_color='blue',
                name='Positive Correlations', 
                text=[.698,.415,.414,.395,.346]))

fig8.add_trace(go.Bar(x=['DRB','TRB','DRtg'], y=[.281,.273,.168],
                base=[-.281,-.273,-.168],
                marker_color='crimson',
                name='Negative Correlations',
                text=[-.281,-.273,-.168]))
fig8.update_layout(title = dict({'text':"Highest/Lowest Correlation Coefficients of <br>" 
                                 "Play-Related Variables for Winningest Teams",
                               'y':.9, 'x':0.45, 
                               'xanchor': 'center'}, font=dict(size=18)))

fig8.update_traces(texttemplate='%{text}', textposition='inside')
fig8.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_title="Variables",
    yaxis_title="Correlation with Wins", paper_bgcolor='#f0f5fa')


fig9 = go.Figure()
fig9.add_trace(go.Bar(x=['ORtg','Field Goal %','3P%','2P%','DRB'], y=[.653,.619,.547,.475,.359],
                marker_color='blue',
                name='Positive Correlations', 
                text=[.653,.619,.547,.475,.359]))

fig9.add_trace(go.Bar(x=['DRtg','TOV','ORB'], y=[.659,.259,.117],
                base=[-.659,-.259,-.117],
                marker_color='crimson',
                name='Negative Correlations',
                text=[-.659, -.259, -.117]))
fig9.update_layout(title = dict({'text':"Highest/Lowest Correlation Coefficients of <br>" 
                                 "Play-Related Variables for All Teams",
                               'y':.9, 'x':0.45, 
                               'xanchor': 'center'}, font=dict(size=18)))

fig9.update_traces(texttemplate='%{text}', textposition='inside')
fig9.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_title="Variables",
    yaxis_title="Correlation with Wins", paper_bgcolor='#f0f5fa')


fig10 = px.scatter(df, x=df['Wins'], y=df['Twitter Followers (Millions)'], trendline='ols', hover_data=['Twitter Followers (Millions)'])
fig10.update_traces(marker=dict(
        color='mediumblue'))
fig10.update_layout(title = {'text': 'Wins vs Twitter Followers',
                           'y':.95, 'x':0.5, 
                           'xanchor': 'center', 
                           'yanchor': 'top'})

fig11 = px.scatter(df, x=df['Wins'], y=df['Facebook Followers (Millions)'], trendline='ols', hover_data=['Facebook Followers (Millions)'])
fig11.update_traces(marker=dict(
        color='mediumturquoise'))
fig11.update_layout(title = {'text': 'Wins vs Facebook Followers',
                           'y':.95, 'x':0.5, 
                           'xanchor': 'center', 
                           'yanchor': 'top'})

fig12 = px.scatter(df, x=df['Wins'], y=df['Total Team Salary'], trendline='ols', size=df['Wins'], hover_data=['Total Team Salary'])
fig12.update_traces(marker=dict(
        color='lightgreen'))
fig12.update_layout(title = {'text': 'Wins vs Total Team Salary',
                           'y':.95, 'x':0.5, 
                           'xanchor': 'center', 
                           'yanchor': 'top'})
fig12.update_traces(marker=dict(size=16, opacity=.7, symbol='cross',
                              line=dict(width=2,
                                        color='black')),
                  selector=dict(mode='markers'))

fig13 = px.scatter(df, x=df['Wins'], y=df['Franchise Valuation (Millions)'], trendline='ols', hover_data=['Franchise Valuation (Millions)'])
fig13.update_traces(marker=dict(
        color='goldenrod'))
fig13.update_layout(title = {'text': 'Wins vs Franchise Valuation',
                           'y':.95, 'x':0.5, 
                           'xanchor': 'center', 
                           'yanchor': 'top'})
fig13.update_traces(marker=dict(size=18, opacity=.6, symbol='triangle-down',
                              line=dict(width=2,
                                        color='black')),
                  selector=dict(mode='markers'))

fig14 = px.area(df, x="Wins", y='Total Revenue (Millions)', color='Year')
fig14.update_layout(title = {'text': 'Wins vs Total Revenue (Millions)',
                           'y':.95, 'x':0.5, 
                           'xanchor': 'center', 
                           'yanchor': 'top'})
fig15 = px.scatter(df, x=df['Wins'], y=df['Tickets Sold (Millions)'], trendline='ols', hover_data=['Tickets Sold (Millions)'])
fig15.update_traces(marker=dict(
        color='orchid'))
fig15.update_layout(title = {'text': 'Wins vs Tickets Sold',
                           'y':.95, 'x':0.5, 
                           'xanchor': 'center', 
                           'yanchor': 'top'})
fig15.update_traces(marker=dict(size=20, opacity=.6, symbol='circle',
                              line=dict(width=2,
                                        color='black')),
                  selector=dict(mode='markers'))

fig16 = px.scatter(df, x=df['Wins'], y=df['Avg Ticket Price ($)'], trendline='ols', hover_data=['Avg Ticket Price ($)'])
fig16.update_traces(marker=dict(
        color='aliceblue'))
fig16.update_layout(title = {'text': 'Wins vs Avg Ticket Price',
                           'y':.95, 'x':0.5, 
                           'xanchor': 'center', 
                           'yanchor': 'top'})
fig16.update_traces(marker=dict(size=20, opacity=.6, symbol='circle',
                              line=dict(width=2,
                                        color='black')),
                  selector=dict(mode='markers'))

#Tables
table1 = dash_table.DataTable(
                data=df_variables.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in df_variables.columns],
                style_as_list_view=True,
                style_cell={'textAlign': 'left', 'whiteSpace': 'normal', 'backgroundColor': '#e4ebf5'},
                style_header={'backgroundColor': 'white','fontWeight': 'bold', 'fontColor':'black'},
                style_data={'whiteSpace': 'normal','height': 'auto', 'width':'auto'},
                fixed_columns={'headers': True, 'data': 1},
                style_table={'minWidth': '60%', 'width': '800px','height': '400px', 'overflowY': 'auto'},
                page_action='none',)

#Images 

image1 = html.Img(src=('https://user-images.githubusercontent.com/95270132/144998055-58d454d2-e56f-4932-87b5-66b29c80f5a3.png'), 
                     style={'height':'80%', 'width':'40%', 'margin-left':'1vw',}),


# Per team analysis info 
available_indicators = ['Luxury Tax Amt', 'Total Team Salary',
       'Loss', 'Field Goal %', 'Points Per Game', 'Attend/Game',
       'Playoff Wins', 'Avg Ticket Price ($)',
       'Tickets Sold (Millions)', 'Total Revenue (Millions)',
       'Franchise Valuation (Millions)', 'Facebook Followers (Millions)',
       'Twitter Followers (Millions)', '3P%', '2P%', 'FT%', 'ORB', 'DRB',
       'TRB', 'AST', 'STL', 'BLK', 'TOV', 'MOV', 'ORtg', 'DRtg']

neons = ['#1900A0','#38FF12','#FF00E3', '#FFF100', '#9600FF', '#00F5FB', '#8F00F2','#00CFFB','#5CFF00','#FDFB00','#FDAE32','#FF0C12', 
'#8CF200','#D3FD00', '#E53C6C','#FFFFFF','#6EE1E7','#0F33C9','#D23AAA','#8C33DC','#CC29A0','#FF00FF','#FFF3E6','#FFE5B4','#FFCBA4','#FF0000',
'#FFEA00','#FFFF00','#00FF00','#A0FEFC','#3D50FF','#FFFD41','#FF00FF','#11FF68','#F400FF','#6F00EF','#007FFF','#77FB00','#FEFF00','#FAAB00','#FF6FFF','#B927D6',
'#FF007F','#FF75D1','#FFA8EB','#660404','#F20000','#0BF7F4','#0010F3','#F9F9F9','#5500DD','#CE00FF','#FF1DD0','#00EDEB','#FCF000','#F62BFD',
'#1A1425','#FD3004', '#FF7200','#FF4501','#000000','#1DF301','#82FF06','#FF6FFF','#B927D6','#FF007F','#FF75D1','#FFA8EB','#8A00BA',
'#ED229D','#FF617B','#FFD58E','#0BF7F4', '#FF1DD0','#00F900', '#9DFF00', '#00DFFF','#0433FF','#00E4FF','#A8F5FD', '#F7FFFC','#FFEE00',
'#FFA300','#FF6FFF','#B927D6','#FF007F','#FF75D1','#FFA8EB','#8F00F2','#00CFFB','#5CFF00','#FDFB00','#FDAE32','#FF0C12']


#Cards

card0 = dbc.Card([dbc.CardImg(src="https://user-images.githubusercontent.com/95270132/144326164-b4efe114-dd24-4b1c-aded-c04a7e7c088c.jpg",
            style={"opacity": 0.3, "width":"10rem"}),
            dbc.CardFooter([dbc.Button("NBA.com", href='https://www.nba.com/', outline=True, color="primary", 
                        size="sm", style={'display':'block'})], style={"opacity": 1, "width": "10rem"})
                        ], color="tertiary", style={"opacity": 1, "width": "10rem"})

image_card = dbc.Card(
    [dbc.CardImg(
            src='https://user-images.githubusercontent.com/95270132/144998055-58d454d2-e56f-4932-87b5-66b29c80f5a3.png',
            top=True,
            style={"opacity": .9},),
        dbc.CardImgOverlay(
            dbc.CardBody([html.H4("", className="card-title"),
                    html.P(
                        "",
                        className="card-text",
                    ),],),),],style={"width": "45rem", 'margin-left': '1vw'},color='white',outline=True)

zero_card = dbc.Card(
    [dbc.CardImg(
            src="https://user-images.githubusercontent.com/95270132/144326164-b4efe114-dd24-4b1c-aded-c04a7e7c088c.jpg",
            top=True,
            style={"opacity": 0.9, 'height': '14.4vw'},),
        dbc.CardImgOverlay(
            dbc.CardBody([html.H4("", className="card-title"),
                    html.P(
                        "",
                        className="card-text",
                    ),],),),],style={"width": "18rem", 'margin-left': '1vw'},color='white')



first_card = dbc.Card(dbc.CardBody(
            [html.H4("National Basketball Association", className="card-title", 
                            style={'color':'#4f5887', 'fontsize': '30'}),
            html.P("The NBA is a professional basketball league in North America.  "
                                "It is the world's top professional basketball league. "
                                "Founded in 1946, the league is now composed of 30 teams (see below).",
                                            className="card-text", style={'color': '#8895bf', 'font-size': '16.2px', 'font-family':'sans-serif'}),
            html.A('Go to NBA.com!', href="https://www.nba.com", 
                                style={'color': 'blue', 'text-decoration': 'none'})]),color='white')


second_card = dbc.Card([
    dbc.CardHeader(html.H4('          All Variables Used', style={'font-size':'60'}), style={'color':'white', 'backgroundColor': '#1b64ad'}, className="card-title"),
    dbc.CardBody(dash_table.DataTable(
                data=df_variables.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in df_variables.columns],
                style_as_list_view=True,
                style_cell={'textAlign': 'left', 'whiteSpace': 'normal', 'backgroundColor': 'white', 'font-family':'sans-serif'},
                style_header={'backgroundColor': '#d14045', 'color':'white', 'fontWeight': 'bold', 'fontColor':'white', 'font-family':'sans-serif', 'font-size':'20'},
                style_data={'whiteSpace': 'normal','height': 'auto', 'width':'auto'},
                fixed_columns={'headers': True, 'data': 1},
                style_table={'minWidth': '60%', 'width': '500px','height': '748px', 'overflowY': 'auto'},
                page_action='none'), style={"width":"73.5rem", "height":'48.5rem', "opacity": .9, 'display':'center'}),
    dbc.CardFooter(html.P('* Play-Related Variable', style={'color': '#8895bf', 'font-size': '13px', 'font-family':'sans-serif'}),style={"height": "2rem"})]
                ,color='white')


advice_card1 = [
    dbc.CardHeader("Takeaways/Advice"),
    dbc.CardBody(
        [
            html.H5("Win Promotion Strategy: ", className="card-title", style={'color':'blue', 'fontsize': '20'}),
            dbc.ListGroup(
                [
                    dbc.ListGroupItem("• Improve Offensive Efficiency: (produce more points in fewer possessions to boost ORtg)"),
                    dbc.ListGroupItem("• Improve Field Goal Percentage: (increase shooting percentage, specifically 3 point percentage)"),
                    dbc.ListGroupItem("• Pay into the Luxury Tax: (pay for better players who can improve the above-mentioned statistics)"),
                ],
                flush=True, style={'fontcolor': '#7b8ab8', 'fontWeight':'bold'}
            )
        ]
    ),
]

advice_card2 = [
    dbc.CardHeader("Takeaways/Advice"),
    dbc.CardBody(
        [
            html.H5("Loss Reduction Strategy:", className="card-title", style={'color':'crimson', 'fontsize': '20'}),
            dbc.ListGroup(
                [
                    dbc.ListGroupItem("• Improve Defensive Efficiency: (give up fewer points in greater possessions to boost DRtg)"),
                    dbc.ListGroupItem("• Reduce Turnovers: (improve decision making/coaching to reduce the amount of lost possessions)"),
                    dbc.ListGroupItem("• Value Total Team Salary over Total Revenue: (win coorelation is positive for the former and negative for the latter)"),
                ],
                flush=True,style={'fontcolor': '#7b8ab8', 'fontWeight':'bold'}
            )
        ]
    ),
]


#Page 2 Jumbotron/Conclusions
left_jumbotron = dbc.Col(
    html.Div(
        [
            html.H2("The Winning Formula", className="display-3", style={'color': 'blue'}),
                    html.Hr(className="my-2"),
                    html.P("  ________________________________________________________________________________  "
                           " NBA Teams That Value Winning and Championships Should Focus on Improving Statistics "
                                    "That Have Significant Positive Correlations with Wins.", style={'fontWeight': 'bold'}),
                    html.P(" - Of the 30 variables analyzed, 3 play-related variables had significant positive correlations with wins and 2 non-play related "
                        "variables had moderate positive coorelations with wins. They, along with their correlation values, are displayed below:"),
                ],className="h-100 p-5 bg-light border rounded-3",
    ),
    md=6,
)

right_jumbotron = dbc.Col(
    html.Div(
        [html.H2("The Losing Remedy", className="display-3", style={'color': 'crimson'}),
                    html.Hr(className="my-2"),
                    html.P("  ________________________________________________________________________________ "
                           " NBA Teams That Value Winning and Championships Should Focus on Reducing Statistics "
                                    "that Have Significant Negative Correlations with Wins.", style={'fontWeight': 'bold'}),
                    html.P(" - Of the 30 variables analyzed, 1 play-related variable had a significant negative correlation with wins, 2 "
                        "play-related variables had weak negative coorelations, and 2 non-play-related variables had weak negative correlations. They, along with their correlation values, are displayed below:"),
                ],className="h-100 p-5 bg-light border rounded-3",
    ),
    md=6,
)

jumbotron = dbc.Row(
    [left_jumbotron, right_jumbotron],
    className="align-items-md-stretch",
)


#Jumbotron 2
left_jumbotron = dbc.Col(
    html.Div(
        [
            html.H2("Non-Play-Related Variables", className="display-3"),
                    html.Hr(className="my-2"),
                    html.P("  _________________________________________________________________________________  "
                           "- Variables such as Offensive Rebounds or Field Goal Percentage are considered play-related "
                           "variables in our dataset, as their data is collected via play during games. "),
                    html.P(" - Variables such as Attendance per Game or Total Team Salary are non-play-related variables, "
                           " as thier data is collected externally from the court of play. "),
                    html.P(" The tabs below display various graphs showing the impact these non-play-related variables "
                           " have on wins. ", style={'fontWeight': 'bold'}),
                ],className="h-100 p-5 bg-light border rounded-3",
    ),
    md=6,
)


jumbotron2 = dbc.Row(
    [left_jumbotron, dcc.Graph(id='correlation_graph', figure=fig8, 
                 style = {'width': '50%'}),],
    className="align-items-md-stretch", style={'width':'99.2%', 'margin-left':'.35vw'}
)


#Page 1 Tabs

tabs = dbc.Col(
    html.Div([
        dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Attendance", tab_id="attendance", label_style={"color": "#485785"}),
                    dbc.Tab(label="Ticket Price", tab_id="avg_ticket_price", label_style={"color": "#485785"}),
                    dbc.Tab(label="Tickets Sold", tab_id="tickets_sold", label_style={"color": "#485785"}),
                    dbc.Tab(label="Total Revenue", tab_id="total_revenue", label_style={"color": "#485785"}),
                    dbc.Tab(label="Franchise Valuation", tab_id="franchise_valuation", label_style={"color": "#485785"}),
                    dbc.Tab(label="Luxury Tax", tab_id="luxury_tax", label_style={"color": "#485785"}),
                    dbc.Tab(label="Total Team Salary", tab_id="tot_team_salary", label_style={"color": "#485785"}),
                    dbc.Tab(label="Team Location", tab_id="location", label_style={"color": "#485785"}),
                    dbc.Tab(label="Social Media", tab_id="social_media", label_style={"color": "#485785"}),
                    
                ],
                id="card-tabs",
                active_tab="attendance", style = {'background':'white'}
            )
        ),
        dbc.CardBody(html.P(id="card-content", className="card-text")),
    ],style = {'background':'#f0f5fa'}
)
    ]),md=6,style={'width':'49%', 'margin-left':'1vw'})
        
        
#Progress Bars

bar_group1 = dbc.Col(
    html.Div(
        [
        dbc.Progress(value=75, label= 'Offensive Rating = .654', color='blue', className="mb-3"),
        dbc.Progress(value=68, label= 'Field Goal Percentage = .619',color='blue', className="mb-3"),
        dbc.Progress(value=59, label= '3 Point Percentage = .548', color='blue', className="mb-3"),
        dbc.Progress(value=48, label= 'Attendance per Game = .426', color='blue', className="mb-3"),
        dbc.Progress(value=39, label= 'Luxury Tax = .316', color='blue', className="mb-3")
        ]
        ,style={'margin-left':'1vw'}),)

bar_group2 = dbc.Col(
    html.Div(
        [dbc.Progress(value=75, label= 'Defensive Rating = -.659', color='danger',className="mb-3"),
        dbc.Progress(value=40, label= 'Turnovers = -.259',color='danger', className="mb-3"),
        dbc.Progress(value=30, label= 'Offensive Rebounds  = -.117', color='danger', className="mb-3"),
        dbc.Progress(value=29, label= 'Franchise Valuation = -.104', color='danger', className="mb-3"),
        dbc.Progress(value=18, label= 'Total Revenue = -.011', color='danger', className="mb-3"),
        ]
        ,style={'margin-right':'1vw'}),)

bar_groups = dbc.Row(
    [bar_group1, bar_group2],
    className="align-items-md-stretch",
)





#Dropdown and Logo Image
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
nav_item = dbc.NavItem(dbc.NavLink("Data Source", href="https://www.basketball-reference.com/"))
dropdown = dbc.DropdownMenu(children=[
        dbc.NavLink(dbc.DropdownMenuItem("Project Overview", href="/"), active="exact"),
        dbc.DropdownMenuItem(divider=True),
        dbc.NavLink(dbc.DropdownMenuItem("Season Analysis", href="/page-1"), active="exact"),
        dbc.NavLink(dbc.DropdownMenuItem("Team Analysis", href="/page-2"), active="exact"),],
    nav=True,in_navbar=True,label="Menu",)

logo = dbc.Navbar(dbc.Container([html.A(
               dbc.Row(
                   [dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("NBA Dashboard", class_name="ms-2")),],
                    align="center",class_name="g-0",),href="/",style={"textDecoration": "none"},),
                dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
                dbc.Collapse(dbc.Nav([nav_item, dropdown], class_name="ms-auto",navbar=True,
                ), id="navbar-collapse2", navbar=True,),],),
                  color= '#4f5887',
                  dark=True,class_name="mb-5",)



#Content Determiner 
content=html.Div(id="page-content", children=[])   

#General App Layout Determiner 
app.layout = html.Div([dcc.Location(id="url", pathname="/"),logo,content])

@app.callback(Output("page-content", "children"),
              [Input("url","pathname")])

def render_page_content(pathname): 
    if pathname == "/": 
        return [html.Div(children=[
        html.H1(children='NBA Dashboard', style={'textAlign': 'center', 'display': 'block'}),
        html.H4(children='''
        An Analysis of the Factors that Affect Team Wins''', style={'textAlign': 'center', 'display':'block'}),
        html.Div(children='''
        Team Members: 
        Yuan-Cheng Tsai, Gabe Owens, Shree Vidya Ravi Kumar, Arpan Shrivastava, Radhika Kumari
        ''', style={'textAlign': 'center', 'display':'block'}),
        html.Br(),
        dbc.Col(children=[
        dbc.Row([
        dbc.Col(zero_card, width=2),
        dbc.Col(first_card, width=4),
        dbc.Col(second_card, width=6, style={'margin-right': '1vw', 'width': '48%'}),
        dbc.Col(image_card, width=5, style={
    'display': 'inline-block', 'float': 'left', 'flex_wrap':'wrap','margin-top': '15vw', 'position': 'absolute'}),
        ])
        ], lg=12,md=6,sm=6)]
                         )]
    elif pathname == "/page-1": 
        return [html.Div(children=[
    html.H1(children='Per-Season Analysis', style={'textAlign': 'center'}),
        html.Div(children='''
        A Combined Analysis of Grouped Data from the 2013-2019 NBA Seasons
    ''', style={'textAlign': 'center'}),
    html.Br(), 
    html.Div([
    dbc.Col(children=[
            html.Div([
                dcc.Dropdown(
                    id='team-dropdown2',
                    options=[{'label': i, 'value': i} for i in df['Year'].unique()],
                    value=2013
                ),
                ], style={'width': '47.1%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='yaxis-column2',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='DRB'
                ),             
                ], style={'width': '47.1%', 'display': 'inline-block'}), 
            dcc.Graph(id='indicator-graphic2', style={'display': 'inline-block', 'border': 'thin lightgrey dashed'}),
            ], lg=12,md=6,sm=6),
            dbc.Toast(
                [html.P("This graph shows the effect of each variable on wins for the selected season.", className="mb-0")],
                    header="Comprehensive Season Graph",  style={'width':'40%', 'float':'left'})
                ],style={'width': '49%', 'display': 'inline-block', 'margin-left':'1vw'}),
        html.Div([
        dbc.Col(children=[ 
            dbc.Alert("2013 Most Wins: San Antonio Spurs", color="hotpink"),
            dbc.Alert("2014 Most Wins: Golden State Warriors", color="warning"),
            dbc.Alert("2015 Most Wins: Golden State Warriors", color="warning"),
            dbc.Alert("2016 Most Wins: Golden State Warriors", color="warning"),
            dbc.Alert("2017 Most Wins: Houston Rockets", color="info"),
            dbc.Alert("2018 Most Wins: Toronto Raptors", color="lightgreen"),
            dbc.Alert("2019 Most Wins: Milwaukee Bucks", color="palevioletred"),
        ], lg=12,md=6,sm=6),
            dbc.Toast(
            [html.P("These teams won the most total games (including playoffs), for their respective seasons.", className="mb-0")],
            header="NBA Win Leaders 2013-2019", style={'width':'45%', 'float':'right', 'margin-bottom':'1vw'}),
        ],style={'width': '49%', 'float': 'right', 'display': 'inline-block', 'margin-right':'1vw', 'position': 'absolute'}),
        html.Br(),
        html.Br(),
        jumbotron2,
        html.Br(),
        dbc.Row(
            [tabs, dcc.Graph(id='correlation_graph2', figure=fig9, 
                 style = {'width': '48.8%', 'float':'right'})],
            className="align-items-md-stretch", 
            ),
        html.Br(),
        ]),
               ]
    
    elif pathname == "/page-2":
        return [html.Div(children=[
    html.H1(children='Per-Team Analysis', style={'textAlign': 'center'}),
    html.Div(children='''
        An Individual Analysis of Data from Each of the 30 NBA Teams   
    ''', style={'textAlign': 'center'}),
    html.Br(), 
    html.Div([
    dbc.Col(children=[ 
            html.Div([
                dcc.Dropdown(
                    id='team-dropdown',
                    options=[{'label': i, 'value': i} for i in df['Team'].unique()],
                    value='Atlanta Hawks'
                ),
                ], style={'width': '47.1%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Field Goal %'
                ),             
                ], style={'width': '47.1%', 'display': 'inline-block'}), 
            dcc.Graph(id='indicator-graphic', style={'display': 'inline-block', 'border': 'thin lightgrey dashed'}),
        ], lg=12,md=6,sm=6),
            dbc.Toast(
                [html.P("This graph shows the effect of each variable on wins for the selected team.", className="mb-0")],
                    header="Comprehensive Team Graph",  style={'width':'40%', 'float':'left'})
                ],style={'width': '49%', 'display': 'inline-block', 'margin-left':'1vw'}),
        html.Div([
        dbc.Col(children=[ 
        dbc.Alert("2013 NBA Champion: San Antonio Spurs", color="darkmagenta"),
        dbc.Alert("2014 NBA Champion: Golden State Warriors", color="darkblue"),
        dbc.Alert("2015 NBA Champion: Cleveland Cavaliers", color="lightskyblue"),
        dbc.Alert("2016 NBA Champion: Golden State Warriors", color="lightgreen"),
        dbc.Alert("2017 NBA Champion: Golden State Warriors", color="yellowgreen"),
        dbc.Alert("2018 NBA Champion: Toronto Raptors", color="warning"),
        dbc.Alert("2019 NBA Champion: Los Angeles Lakers", color="danger"),
        ], lg=12,md=6,sm=6),
        dbc.Toast(
            [html.P("These teams won enough games to make the playoffs, then won 16 more to win the Championship.", className="mb-0")],
            header="NBA Champions 2013-2019", style={'width':'40%', 'float':'right', 'margin-bottom':'1vw'}),
        ],style={'width': '49%', 'float': 'right', 'display': 'inline-block', 'margin-right':'1vw', 'position': 'absolute'}),
        html.Br(),
        html.Br(),
        html.Br(),
            
        jumbotron,
            
        html.Br(),
        html.Br(),
        
        bar_groups, 
            
        html.Br(),
        
        html.Div([
            dbc.Row(
            [
            dbc.Col(dbc.Card(advice_card1, color="primary", outline=True)),
            dbc.Col(dbc.Card(advice_card2, color="danger", outline=True)),
            ]
            ,style={'margin-left':'.5vw', 'margin-right':'.5vw'})
        ])
        ]
        )]
    
    else: 
        return dbc.Jumbotron([html.H1("404: Not found", className="text-danger"), 
                              html.Hr(), 
                              html.P(f"The pathname {pathname} was not recognized..."), 
                             ])

    
# per season analysis first graph callback 
@app.callback(
    Output('indicator-graphic2', 'figure'),
    Input('team-dropdown2', 'value'),
    Input('yaxis-column2', 'value'))
    
def update_graph(season_dropdown_name, yaxis_column_name2):

    df_season = df[df['Year'] == season_dropdown_name]

    fig = px.scatter(df_season, x=df_season['Wins'], y=df_season[yaxis_column_name2],
                    color=df_season['Team'],
                    title=(f'{season_dropdown_name} Wins vs {yaxis_column_name2}'), trendline="ols", trendline_scope="overall", hover_data=['Year'])
    fig.update_layout(title = dict({
                               'y':.9, 'x':0.45, 
                               'xanchor': 'center'}, font=dict(size=25, color='#4c5c84')))

    fig.update_layout({
    'plot_bgcolor': 'rgb(215,217,229)',
    'paper_bgcolor': 'white',})
    fig.add_layout_image(
    dict(
        source="https://raw.githubusercontent.com/timaboderin/NBA_Logos/master/new_team.png",
        xref="paper", yref="paper",
        x=1.25, y=1.1,
        sizex=0.14, sizey=1.75,
        xanchor="right", yanchor="bottom"
    )
    )  
    fig.update_traces(textposition="middle center", marker_symbol='circle', marker=dict(colorscale='rainbow'), marker_size=16, line_color='#4c5c84')
    fig.update_xaxes(showline=True, linewidth=3, linecolor='#4c5c84', gridcolor='white')
    fig.update_yaxes(showline=True, linewidth=3, linecolor='#4c5c84', gridcolor='white')

    return fig
    
    
# Per team analysis first graph callback 
@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('team-dropdown', 'value'),
    Input('yaxis-column', 'value'))
    
def update_graph(team_dropdown_name, yaxis_column_name):

    df_year = df[df['Team'] == team_dropdown_name]
    
    colorchoice = np.random.choice(neons)
    color_list = [colorchoice, colorchoice, colorchoice, colorchoice, colorchoice, colorchoice, colorchoice]
    color_list

    fig = px.scatter(df_year, x=df_year['Wins'], y=df_year[yaxis_column_name], 
                  text=df_year['Year'],
                  title=(f'{team_dropdown_name} <br> Wins vs {yaxis_column_name}'), trendline="ols", trendline_scope="overall", hover_data=['Team'])
    fig.update_layout(title = dict({
                               'y':.9, 'x':0.45, 
                               'xanchor': 'center'}, font=dict(size=25, color='#4c5c84')))

    fig.update_layout({
    'plot_bgcolor': 'rgb(215,217,229)',
    'paper_bgcolor': 'white',})
    fig.add_layout_image(
    dict(
        source="https://raw.githubusercontent.com/timaboderin/NBA_Logos/master/new_team.png",
        xref="paper", yref="paper",
        x=1.25, y=1.1,
        sizex=0.14, sizey=1.75,
        xanchor="right", yanchor="bottom"
    )
    )  
    fig.update_traces(textposition="top center", marker_symbol='circle', marker_color=df_year['Year'], marker=dict(colorscale='rainbow'), marker_size=df_year['Wins'], line_color='#4c5c84')
    fig.update_xaxes(showline=True, linewidth=3, linecolor='#4c5c84', gridcolor='white')
    fig.update_yaxes(showline=True, linewidth=3, linecolor='#4c5c84', gridcolor='white')

    return fig

#Page 1 Tabs Callback
@app.callback(
    Output("card-content", "children"), [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    if active_tab== 'attendance':
        return [
           dcc.Graph(id='wins vs attendance', figure=fig6), 
        ]
    elif active_tab== 'avg_ticket_price':
        return [
           dcc.Graph(id='wins vs avg ticket price', figure=fig16), 
        ]
    elif active_tab== 'tickets_sold':
        return [
        dcc.Graph(id="wins vs tickets sold", figure = fig15)
        ]
    elif active_tab== 'total_revenue':
        return [
        dcc.Graph(id="wins vs total revenue", figure = fig14)
        ]
    elif active_tab== 'franchise_valuation':
        return  [
        dcc.Graph(id="wins vs franchise valuation", figure = fig13)
        ]
    elif active_tab== 'luxury_tax':
        return [
            dbc.Row(
                [dcc.Graph(id='wins vs luxury tax', figure= fig3, 
                        style={'width':'50%'}), 
                dcc.Graph(id='wins vs luxury tax2', figure= fig4, 
                        style={'width':'50%'}),],
                className="align-items-md-stretch"
                )
                ]
    elif active_tab== 'tot_team_salary':
        return [
        dcc.Graph(id="wins vs total team salary", figure = fig12)
        ]
    elif active_tab== 'location':
        return [
        dcc.Graph(id="wins vs location", figure = fig5)
        ]
    elif active_tab== 'social_media':
        return [
            dbc.Col(
                [dcc.Graph(id='wins vs twitter', figure= fig10, 
                        style={'height':'15vw'}), 
                dcc.Graph(id='wins vs facebook', figure= fig11, 
                        style={'height':'15vw'}),],
                className="align-items-md-stretch"
                )
            ]
            

#Navigation Bar Callback
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

app.run_server(mode='external', port=7250)

#app._terminate_server_for_port("localhost", 7250)