#from __future__ import print_function
import requests
import pickle
from bs4 import BeautifulSoup
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API

    spreadsheet = {
        'properties': {
            'title': 'Covid '
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                        fields='spreadsheetId').execute()

    spreadsheet_id = spreadsheet.get('spreadsheetId')

    range_name = 'mention_range'

    body = {
        "majorDimension": "ROWS",
        "values": [
            mention titles in a list],
           }

    URL = 'url_to_connect'
    html_str = requests.get(URL)
    soup = BeautifulSoup(html_str.text, 'html.parser')
    l = []
    #search for class in a element
    l = soup.find_all('a', class_="mention_class")

    final_list = []
    base_url = 'base_url'

    for t in l:
        final_url = base_url + t['href'][3:]
        print(final_url)
        final_list.append([t.text, final_url])
        body["values"].append([t.text, final_url])

    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        body=body,
        valueInputOption='USER_ENTERED'
    ).execute()
    print(result)

if __name__ == '__main__':
    main()
