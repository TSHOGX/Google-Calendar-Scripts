# Google-Calendar-Scripts

[Quickstart](https://developers.google.com/calendar/quickstart/python)

used API:
* [Events](https://developers.google.com/calendar/v3/reference/events): Events 按照日期倒序排列 
* [CalendarList: list](https://developers.google.com/calendar/v3/reference/calendarList/list): list of categories

Next:
* count for select items
* calculate each items periods and plot a graph

Plot(for selected week, this 7 days):
* day - labels
* category - items
* all events in this category - number



   Google Calendar Script {
       'kind': 'calendar#event', 
       'etag': '"3190622168384000"', 
       'id': '_68sjgh1l6p1j0b9k850k8b9k8d2jiba16l0k4b9h88p46d9o8go34g9i6c', 'status': 'confirmed', 
       'htmlLink': 'https://www.google.com/calendar/event?eid=XzY4c2pnaDFsNnAxajBiOWs4NTBrOGI5azhkMmppYmExNmwwazRiOWg4OHA0NmQ5bzhnbzM0ZzlpNmMgbXRjNWNubzhxMDlmZWZ0bXYzbTduMGxpMzBAZw', 
       'created': '2020-07-21T05:49:22.000Z', 
       'updated': '2020-07-21T05:58:04.231Z', 
       'summary': 'Google Calendar Script', 
       'creator': {'email': 'tshogx@gmail.com'}, 
       'organizer': {'email': 'mtc5cno8q09feftmv3m7n0li30@group.calendar.google.com', 'displayName': 'Study', 'self': True}, 
s       'start': {'dateTime': '2020-07-21T11:30:00+08:00'}, 
s       'end': {'dateTime': '2020-07-21T14:00:00+08:00'}, 
       'iCalUID': '298D56C0-4AAD-4CE9-A5AB-1B2C58D02A23', 
       'sequence': 2, 
       'reminders': {'useDefault': False}}

for each category:
for each event:
    append 'daylist'
    if daylist.len > 7 : break # only count one week
    if day == daylist[-1]: # still in same day
        continue calculate time period

{'kind': 'calendar#events', 'etag': '"p33c8trnstreuk0g"', 'summary': '个人', 'updated': '2020-07-21T07:54:42.439Z', 'timeZone': 'Asia/Shanghai', 'accessRole': 'owner', 'defaultReminders': [{'method': 
'popup', 'minutes': 30}], 'nextSyncToken': 'CNiO7vzu3eoCENiO7vzu3eoCGAU=', 'items': []}