from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import matplotlib.pyplot as plt
from datetime import date

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    service = initialize()
    categoryList = getCategoryList(service)
    day, daylist = getDaylist()
    print("Today's date:", day,daylist)
    print('#', categoryList[1], ': ')

    daydict = {}
    for day in daylist:
        # daydict: {day:[list store every category's total time]} [timeList]
        # return timeList [list store every category's total time]
        # traverse all category, count category time for this day
        daydict[str(day)] = getDict(day, categoryList) # timeList


    # page_token = None
    # daydict = {}
    # for day in daylist:
    #     timeList = []

    #     # traverse all category
    #     for i in range(len(categoryIdList)):
    #         categoryId = categoryIdList[i]
    #         # for each category
    #         page_token = None
    #         while True:
    #             categories = service.events().list(calendarId=categoryId, pageToken=page_token).execute()
    #             # traverse all event in this day in this category
    #             print('#', categories, ': ')
    #             time = 0
    #             daylist = []
    #             for event in categories['items']:
    #                 day, daystr = getDay(event['start']['dateTime'])
    #                 print(day,daystr)
    #                 # print('   ', event['summary'], timeCalculator(event))
    #                 time += timeCalculator(event)
    #             print('    total time:', time)
    #             timeList.append(time)
                
    #             daydict[str(day)] = timeList
    #             print(daydict[str(day)])


    #             page_token = categories.get('nextPageToken')
    #             if not page_token:
    #                 break
    
    
    
    return



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

def getCategoryList(service):
    # list of all category, can call events in them
    # event: for event in categories['items']: item is list of calendar#events
    # title: categories['summary']
    page_token = None
    categoryIdList = getCategoriesId(service)
    categories = []
    for i in range(len(categoryIdList)):
        categoryId = categoryIdList[i]
        # for each category
        while True:
            categories.append(service.events().list(calendarId=categoryId, pageToken=page_token).execute())
            page_token = categories[-1].get('nextPageToken')
            if not page_token:
                break
    return categories


def getDaylist():
    '''
    get today and initial daylist
    '''
    today = str(date.today())
    day, daystr = getDay(today)
    daylist = []
    for i in range(day-6,day+1):
        daylist.append(i)
    return day, daylist


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


def getDay(timestamp):
    '''
    get day number in this year: 0-366 or 0-365
    return the number of this event
    '''
    year = int(timestamp[0:4])
    month = int(timestamp[5:7])
    day = int(timestamp[8:10])
    
    if year % 4 == 0:
        Feb = 29
    else:
        Feb = 28
    mlist = [31,Feb,31,30,31,30,31,31,30,31,30,31]

    count = day
    for i in range(month-1):
        count += mlist[i]
    parts = [str(month), '.', str(day)]
    daystr = ''.join(parts)
    return count, daystr



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