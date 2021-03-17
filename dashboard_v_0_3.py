import os 
import flask

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output

import datetime as dt
import pandas as pd

CLIENT_SECRETS_FILE = "secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'

server = flask.Flask(__name__)
app = dash.Dash(__name__, server = server)

server.secret_key = 'secret'

app.layout=html.Div(
    children = [
        dcc.Link(
            'authorize', 
            href='http://localhost:8080/authorize'),

        dcc.DatePickerRange(
            id = 'date-picker',
            calendar_orientation = 'horizontal',
            start_date = '2021-03-01',
            end_date= '2021-03-15'),

        dcc.Graph(
            id='views-graph',
            figure={})
    ]
)

@server.route('/test')
def test_api_request():

    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    youtube = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    report = youtube.reports().query(
        ids='channel==MINE', 
        startDate='2021-03-01', 
        endDate='2021-03-15', 
        metrics='views').execute()

    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.jsonify(**report)

@server.route('/authorize')
def display_index():

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES)

    flow.redirect_uri = flask.url_for(
        'oauth2callback', 
        _external=True)

    authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true')

    flask.session['state'] = state

    return flask.redirect(authorization_url)

@server.route('/oauth2callback')
def oauth2callback():

    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, 
        scopes=SCOPES, 
        state=state)

    flow.redirect_uri = flask.url_for(
        'oauth2callback', 
        _external=True)

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.redirect(flask.url_for('test_api_request'))

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

def json_to_df(response):
    yta_report_df = pd.DataFrame()
    date = []
    views = []

    for day in response['rows']:

        proper_date = dt.datetime.strptime(day[0], '%Y-%m-%d')
        date.append(proper_date)
        views.append(day[1])

    yta_report_df['date'] = date
    yta_report_df['views'] = views

    return yta_report_df

@app.callback(
    Output(component_id='views-graph', component_property='figure'),
    [Input(component_id='date-picker', component_property='start_date'),
    Input(component_id='date-picker', component_property='end_date')]
)

def update_graph(start_date, end_date):

    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    youtube = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    report = youtube.reports().query(
        ids='channel==MINE',
        startDate=start_date,
        endDate=end_date,
        metrics='views',
        dimensions='day',
        sort='day',
        filters='video==wtQTwYX4dGc').execute()


    fig = px.bar(
        data_frame = json_to_df(report),
        x='date',
        y='views',
        template='plotly_dark')

    return fig

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    server.run('localhost', 8080, debug=True)