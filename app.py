import pandas as pd
import dash
import numpy as np
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input ,Output
import plotly.graph_objs as go


df = pd.read_csv('clean_data.csv')
df.head(5)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout=  html.Div([


  html.Div(style={'background-color': '#194c7f','padding':"2%"}),

        html.Br(),

    html.Div([
        html.Div([
           
            dcc.Dropdown(id='country',options=[{'label':i,'value':i} for i in set(df['country'])],value='Japan',
            placeholder='Select Country',style={'width':"100%"})
        ], className="four columns"),

        html.Div([
            
            dcc.Dropdown(id='year',options=[{'label':i,'value':i} for i in set(df['year'])], value=df['year'].min(),
            placeholder='Select year',style={'width':"100%"})
        ], className="four columns"),


      html.Div([
            
            dcc.Dropdown(id='age',options=[{'label':i,'value':i} for i in set(df['age'])], value='15-24 years',
            placeholder='Select age group',style={'width':"100%"})
        ], className="four columns"),

    ], className="row"),

    #################################################END OF INPUT#########################

    ######################################START OF GRAPHS-1#####################################

    html.Div([
        html.Div([
            
            dcc.Graph(id='g1')
        ], className="six columns"),

        html.Div([
            
            dcc.Graph(id='g2')
        ], className="six columns"),
    ], className="row"),

#######################################END OF GRAPH-1###################################################################


########################################START OF GRAPH-2#################################################################

    html.Div([
        html.Div([
            
            dcc.Graph(id='g4')
        ], className="six columns"),

        html.Div([
            
            dcc.Graph(id='g5')
        ], className="six columns"),
    ], className="row")

    ######################################END OF GRAPH-2######################################################################


])


@app.callback(Output('g1','figure'),
           [Input('country','value'),
           Input('age','value')])

def update_figure(country,age):
  data = []
  nation = df['country']==country
  group  = df['age']==age
  sex_male    = df['sex']=='male'
  sex_female    = df['sex']=='female' 
  
  filter_data_male=df[nation & group & sex_male]
  filter_data_female=df[nation & group & sex_female]

  data_male = go.Scatter(x=filter_data_male['year'],
                   y=filter_data_male['suicides_no'],
                   mode='markers+lines',name='male')

  data_female = go.Scatter(x=filter_data_female['year'],
                   y=filter_data_female['suicides_no'],
                   mode='markers+lines',name='female')

  data.append(data_female)
  data.append(data_male)

  return {'data':data,'layout':go.Layout(title='Number of suicide in {} for {} age group'.format(country,age) ) }


###################################################################################################

@app.callback(Output('g2','figure'),
           [Input('country','value'),
           Input('age','value')])

def update_figure(country,age):
  data = []
  nation = df['country']==country
  group  = df['age']==age
  sex_male    = df['sex']=='male'
  sex_female    = df['sex']=='female' 
  
  filter_data_male=df[nation & group & sex_male]
  filter_data_female=df[nation & group & sex_female]

  data_male = go.Scatter(x=filter_data_male['year'],
                   y=filter_data_male['population'],
                   mode='markers+lines',name='male')

  data_female = go.Scatter(x=filter_data_female['year'],
                   y=filter_data_female['population'],
                   mode='markers+lines',name='female')

  data.append(data_female)
  data.append(data_male)

  return {'data':data,'layout':go.Layout(title='Population of {} for {} age group'.format(country,age))}

################################################################################################################



@app.callback(Output('g4','figure'),
           [Input('country','value'),
           Input('year','value')])

def update_figure(country,year):
  data = []
  nation = df['country']==country
  Year  = df['year']==year
  sex_male   = df['sex']=='male'
  sex_female = df['sex']=='female' 
  
  filter_data_male=df[nation & Year & sex_male]
  filter_data_female=df[nation & Year & sex_female]

  data_male = go.Bar(x=filter_data_male['age'],
                   y=filter_data_male['suicides_no']
                   ,name='male')

  data_female = go.Bar(x=filter_data_female['age'],
                   y=filter_data_female['suicides_no']
                   ,name='female')

  data.append(data_female)
  data.append(data_male)

  return {'data':data,'layout':go.Layout(title='Distribution  of suicide in {} for different age groups in year {}'.format(country,year))}



########################################################################################################################


@app.callback(Output('g5','figure'),
           [Input('country','value'),
           Input('year','value')])

def update_figure(country,year):
  data = []
  nation = df['country']==country
  Year  = df['year']==year
  sex_male   = df['sex']=='male'
  sex_female = df['sex']=='female' 
  
  filter_data_male=df[nation & Year & sex_male]
  filter_data_female=df[nation & Year & sex_female]

  data_male = go.Bar(x=['Male'],
                   y=[sum(filter_data_male['suicides_no'])]
                   ,name='male')

  data_female = go.Bar(x=['Female'],
                   y=[sum(filter_data_female['suicides_no'])]
                   ,name='female')

  data.append(data_female)
  data.append(data_male)

  return {'data':data,'layout':go.Layout(title='Total Suicide Based on Gender in {} for year {}'.format(country,year))}


#########################################################################################################

if __name__=="__main__":
    app.run_server(debug=True)
