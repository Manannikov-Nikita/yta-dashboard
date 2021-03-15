import dash
import os
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from api_connector import get_service, execute_api_request
from dash.dependencies import Input, Output

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'secret.json'

app = dash.Dash(__name__)

app.layout = html.Div(
    children = [

    dcc.DatePickerRange(
        id = 'date-picker',
        calendar_orientation = 'horizontal',
        start_date = '2021-03-01',
        end_date= '2021-03-15'
    ),

    dcc.Graph(id='views-graph', figure={}) 
    ]
)

@app.callback(
    Output(component_id='views-graph', component_property='figure'),
    [Input(component_id='date-picker', component_property='start_date'),
    Input(component_id='date-picker', component_property='end_date')]
)

def update_graph(start_date, end_date):

    youtubeAnalytics = get_service()
    date_x_views = execute_api_request(
      youtubeAnalytics.reports().query,
      ids='channel==MINE',
      startDate=start_date,
      endDate=end_date,
      metrics='views',
      dimensions='day',
      sort='day',
      filters='video==wtQTwYX4dGc'
    )

    fig = px.bar(
        data_frame = date_x_views,
        x='date',
        y='views',
        template='plotly_dark'
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
