from __future__ import print_function
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class txtcolors:
    normal = '\033[0m'
    No_events = '\33[91m'

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('gog.json', SCOPES)    #my json have name gog in another situation we need to rename it to the name that we have on our computer
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    print(f'{chr(27) + "[2J"}')
    print('(1) Show events for selected day')
    print('(2) Show closest upcoming x events')
    print('(3) Add new upcoming event')
    print('(4) Edit event')
    print('(5) Search for event by name\n') #w zdarzenia list "q"
    program = int(input('Select program: '))

    if program == 1:
        input_date = input('Please input date in format YYYY-MM-DD: ')
        date_format = '%Y-%m-%d'
        try:
            date_check = datetime.datetime.strptime(input_date, date_format)
            try:
                service = build('calendar', 'v3', credentials=creds)
                print(f'Getting the upcoming events for this day')
                events_result = service.events().list(calendarId='primary', timeMin=input_date + 'T00:00:00-00:00', timeMax=input_date + 'T23:59:59-00:00', singleEvents=True, orderBy='startTime').execute()
                events = events_result.get('items', [])
                if not events:
                    print(f'{txtcolors.No_events}You dont have upcoming events!{txtcolors.normal}')
                    return
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    print(start, event['summary'])
            except HttpError as error:
                print('Error: %s' % error)
        except ValueError:
            print('Incorect format of date')

    if program == 2:
        numb_of_events = int(input('Select number of showing event(s): '))
        try:
            service = build('calendar', 'v3', credentials=creds)
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            print(f'Getting the upcoming {numb_of_events} events')
            events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=numb_of_events, singleEvents=True, orderBy='startTime').execute()
            events = events_result.get('items', [])
            if not events:
                print(f'{txtcolors.No_events}You dont have upcoming events!{txtcolors.normal}')
                return
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])
        except HttpError as error:
            print('Error: %s' % error)


if __name__ == '__main__':
    main()
