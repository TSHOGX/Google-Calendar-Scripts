from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import matplotlib.pyplot as plt
from datetime import date
import numpy as np


from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题


TOKEN = 'C:/Users/TSHOG/Documents/__Codes__/Google-Calendar-Scripts/ignore/token.pickle'
CREDENTIALS = 'C:/Users/TSHOG/Documents/__Codes__/Google-Calendar-Scripts/ignore/credentials.json'

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def getTimeList(day, categoryList):
    '''
    for this day:
        traverse all category
        calculate each category's time
        return timeList store each category's time
    '''
    timelist = []
    for cat in categoryList:
        time = 0
        for event in cat['items']:
            eventDay, daystr = getDay(event['start']['dateTime'])
            if eventDay != day:
                continue
            time += timeCalculator(event)
        timelist.append(time)
    # print(timelist)
    return timelist

def initialize():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
    if os.path.exists(TOKEN):
        with open(TOKEN, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN, 'wb') as token:
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


def plotThisWeek(daydict,cats):
    cats.append('else')
    category_names = cats

    # append else item, to get 24h
    for day in daydict:
        el = 24
        for i in daydict[day]:
            el -= i
        daydict[day].append(el)

    results = daydict

    survey(results, category_names)
    plt.show()


def getDate(day):
    '''
    convert day(0-366) to date(mm-dd)
    return date (string)
    '''
    today = str(date.today())
    year = int(today[0:4])
    
    if year % 4 == 0:
        Feb = 29
    else:
        Feb = 28
    mlist = [31,Feb,31,30,31,30,31,31,30,31,30,31]

    dd = day
    mm = 0
    for i in range(11):
        dd -= mlist[i]
        mm += 1
        if dd < mlist[i+1]:
            break
    
    mm += 1
    parts = [str(mm), '.', str(dd)]
    daystr = ''.join(parts)
    return daystr


def survey(results, category_names):
    '''
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    '''
    labels = []
    for day in list(results.keys()):
        labels.append(getDate(int(day)))
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('twilight')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5,
                label=colname, color=color)
        xcenters = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            ax.text(x, y, str(int(c)), ha='center', va='center',
                    color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
            loc='lower left', fontsize='small')

    return fig, ax



def main():
    service = initialize()
    categoryList = getCategoryList(service)
    day, daylist = getDaylist()
    # print("Today's date:", day,daylist)
    # print(categoryList[1])

    daydict = {} # {day:[time list]}
    for day in daylist:
        daydict[str(day)] = getTimeList(day, categoryList)
    # print(daydict)
    
    cats = []
    for cat in categoryList:
        cats.append(cat['summary'])

    plotThisWeek(daydict,cats)
    
    return

if __name__ == '__main__':
    main()