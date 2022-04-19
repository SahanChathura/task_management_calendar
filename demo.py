from pprint import pprint
from Google import Create_Service

# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRET_FILE = 'client_secret_998712119906-j7madrublb03gqhutj7oanbk0jhpuhhf.apps.googleusercontent.com.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# flow = InstalledAppFlow.from_client_secrets_file("client_secret_998712119906-j7madrublb03gqhutj7oanbk0jhpuhhf.apps.googleusercontent.com.json", scopes=SCOPES)
# flow.run_console
#   to create a calendar

request_body = {
    'summary' : 'NIE'
}

# response = service.calendars().insert(body=request_body).execute()

# delete calendar

# service.calendars().delete(calendarId='9hrlsi5333v5h146gluqk3rens@group.calendar.google.com').execute();

# print(response)


# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.

event = {
  'summary': 'SERVER Working',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2022-06-07T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2022-06-07T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

event = service.events().insert(calendarId='primary', body=event).execute()
