from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from .models import Meeting

try:
    import argparse
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None


SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main(method, event):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    meeting_id = event['meeting_id']

    if method == 'create':
        reminds = {'reminders': {
                                    'useDefault': False, #если напоминание по умолчанию
                                    'overrides': [ #если напоминание не по умолчанию
                                {'method': 'popup', 'minutes': 60}, #через всплывающее окно
                ] }
            }
        event.update(reminds)

        event = service.events().insert(calendarId='primary', body=event).execute()
        m = Meeting.objects.get(pk=meeting_id)
        m.event_id = event['id']
        m.save()
        print('Event created: %s' % (event.get('htmlLink')))
        return event

    elif method == 'delete':
        eventId = event['id']
        service.events().delete(calendarId='primary', eventId=eventId).execute()

    elif method == 'update':
        eventId = event['id']
        service.events().delete(calendarId='primary', eventId=eventId).execute()
        event['id']=''
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event updated: %s' % (event.get('htmlLink')))


def start(method, data):
    main(method, data)


event = {
    'summary': 'Проверить лабу на готовность',
    'location': 'ИТМО университет',
    'description': 'Радоваться, что всё работает',
    'start': {
        'dateTime': '2017-06-04T13:00:00-07:00'  # 2017-06-08T09:16:00-07:00
    },
    'end': {
        'dateTime': '2017-06-04T16:00:00-07:00'
    },
    'attendees': ['Igor',
                   {'email': 'ikhalepsky@gmail.com'}#почта посетителя, участника
                  # {'email': 'sbrin@example.com'},
                  ]
}

#start('update', event)