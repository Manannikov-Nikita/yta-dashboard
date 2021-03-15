
# -*- coding: utf-8 -*-

import os
import pandas as pd
import datetime as dt
from pprint import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'secret.json'

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

def get_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def execute_api_request(client_library_function, **kwargs):
  response = client_library_function(
    **kwargs
  ).execute()

  return json_to_df(response)


if __name__ == '__main__':
  # Disable OAuthlib's HTTPs verification when running locally.
  # *DO NOT* leave this option enabled when running in production.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

  youtubeAnalytics = get_service()
  response = execute_api_request(
      youtubeAnalytics.reports().query,
      ids='channel==MINE',
      startDate='2021-03-11',
      endDate='2021-03-15',
      metrics='views',
      dimensions='day',
      sort='day',
      filters='video==wtQTwYX4dGc'
  )

  json_to_df(response)