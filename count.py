from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./ignore/token.pickle'):
        with open('./ignore/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './ignore/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('./ignore/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)


    # show calendar items name and id
    print('----Show calendar items name----')
    page_token = None
    while True:
        eventid = []
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print(calendar_list_entry['summary'])
            eventid.append(calendar_list_entry['id'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            print('----Count: this calendar has ',len(eventid), ' items----')
            print()
            break

    # traverse all items. Show summaries for every items
    print('----Show summaries for every items----')
    page_token = None
    for i in range(len(eventid)):
        itemId = eventid[i]

        while True:
            events = service.events().list(calendarId=itemId, pageToken=page_token).execute()
            print('# ', events['summary'], ': ')
            for event in events['items']:
                print('  ', event['summary'])
            page_token = events.get('nextPageToken')
            if not page_token:
                break
    print('----', len(eventid),' items down----')
    
if __name__ == '__main__':
    main()