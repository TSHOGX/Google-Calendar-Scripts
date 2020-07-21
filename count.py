from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import matplotlib.pyplot as plt

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    service = initialize()
    categoryIdList = getCategoriesId(service)


    print('----Show summaries for every category----')
    page_token = None
    # traverse all category
    timeList = [] # time list for every category
    for i in range(len(categoryIdList)):
        categoryId = categoryIdList[i]
        # for each category
        while True:
            categories = service.events().list(calendarId=categoryId, pageToken=page_token).execute()

            # iterate every event in this category
            print('#', categories['summary'], ': ')
            time = 0
            for event in categories['items']:
                print('   ', event['summary'], timeCalculator(event))
                time += timeCalculator(event)
            timeList.append(time)

            page_token = categories.get('nextPageToken')
            if not page_token:
                break
    print('----', len(categoryIdList),'category down----')
    



    # plotThisWeek()




def initialize():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
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
    return service

def getCategoriesId(service):
    '''
    get user's categories
    store id in categoryIdList
    '''
    page_token = None
    while True:
        categoryIdList = []
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            # print(calendar_list_entry['summary'])
            categoryIdList.append(calendar_list_entry['id'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            # print('----Count: this calendar has',len(categoryIdList), 'categories----')
            # print()
            break
    return categoryIdList


def timeCalculator(event):
    '''
    calculate event lasted time
    return float type (hour)
    '''
    startTime = event['start']['dateTime']
    endTime = event['end']['dateTime']
    # 2020-07-21T10:30:00+08:00
    sHour = startTime[11:13]
    sMinute = startTime[14:16]
    # sSecond = startTime[17:19]
    eHour = endTime[11:13]
    eMinute = endTime[14:16]
    # eSecond = endTime[17:19]
    lastMinute = (int(eHour) * 60 + int(eMinute)) - (int(sHour) * 60 + int(sMinute))
    lastHour = lastMinute / 60
    return lastHour


def plotThisWeek(labels, category):
    labels = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7']
    men_means = [20, 35, 30, 35, 27]
    women_means = [25, 32, 34, 20, 25]
    men_std = [2, 3, 4, 1, 2]
    women_std = [3, 5, 2, 3, 3]
    width = 0.35       # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()

    ax.bar(labels, men_means, width, yerr=men_std, label='Men')
    ax.bar(labels, women_means, width, yerr=women_std, bottom=men_means,
        label='Women')

    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.legend()

    plt.show()


if __name__ == '__main__':
    main()