import dash
import random
import datetime as dt
from httplib2 import Response
import pandas as pd 
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from pandas.io.formats import style
from test import execute_api_request

from dash.dependencies import Input, Output

#Genertating a dake date-line
date = []

start = dt.datetime(2021, 3, 1)
end = dt.datetime(2021, 4, 1)
step = dt.timedelta(days=1)

while start < end:
    date.append(start)
    start += step

#Genrating fake views amount
views = []

for i in range(0, len(date)):
    random_views = random.randint(1000, 3000)
    views.append(random_views)

date_x_views = pd.DataFrame()
date_x_views['date'] = date
date_x_views['views'] = views

app = dash.Dash(__name__)


video_name = 'Nice video'

app.layout = html.Div(
    children = [

    dcc.DatePickerRange(
        id = 'date-picker',
        calendar_orientation = 'horizontal',
        start_date = date[0],
        end_date= date[-1]
    ),

    dcc.Graph(id='Graph1', figure={}) 
    ]
)



@app.callback(
    Output(component_id='Graph1', component_property='figure'),
    [Input(component_id='date-picker', component_property='start_date'),
    Input(component_id='date-picker', component_property='end_date')]
)

def update_graph(start_date, end_date):

    filtered_df = date_x_views.copy()
    filtered_df = filtered_df.query(' @start_date <= date <= @end_date')

    fig = px.bar(
        data_frame = filtered_df,
        x='date',
        y='views',
        template='plotly_dark',
        labels={
            'x':'TEST'
        }
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)