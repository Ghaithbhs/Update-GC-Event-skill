from __future__ import print_function
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.parse import extract_datetime
import pickle
import os.path
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
#from oauth2client.tools import run
from oauth2client import tools

# SCOPES for google calendar API.
SCOPES = ['https://www.googleapis.com/auth/calendar']
# OAuth2webserverFlow for Google People API
FLOW = OAuth2WebServerFlow(
    client_id='361001423406-meqq5djv2vf54fhd0ect7163ugkpssmm.apps.googleusercontent.com',
    client_secret='pioORdrpsd-cFemxkETi08yM',
    scope='https://www.googleapis.com/auth/contacts.readonly',
    user_agent='Focus Smart Box')


class UpdateEvent(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler(IntentBuilder("").require("querry"))
    def handle_update_start_date(self):
        # Getting the credentials for G.People API
        storage = Storage('info.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid is True:
            credentials = tools.run_flow(FLOW, storage)

        http = httplib2.Http()
        http = credentials.authorize(http)

        people_service = build(serviceName='people', version='v1', http=http)

        results = people_service.people().connections().list(
            resourceName='people/me',
            pageSize=10,
            personFields='emailAddresses,names').execute()
        connections = results.get('connections', [])

        # Get credentials for google calendar with smart.box@focus-corporation.com
        # and token management
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
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
        # Getting the event you want to update

        title = self.get_response('what\'s the name of the event')
        events_result = service.events().list(calendarId='primary',
                                              maxResults=1, singleEvents=True,
                                              orderBy='startTime', q=title).execute()
        events = events_result.get('items', [])
        if not events:
            self.speak('event not found')
        for event in events:
            eventid = event['id']
        start = self.get_response('when does it start?')
        st = extract_datetime(start)
        event['start'] = st
        # Updating the Event
        service.events().update(calendarId='primary', eventId=eventid, body=event).execute()

    @intent_handler(IntentBuilder("").require("morning.bus"))
    def handle_update_end_date(self):
        # Getting the credentials for G.People API
        storage = Storage('info.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid is True:
            credentials = tools.run_flow(FLOW, storage)

        http = httplib2.Http()
        http = credentials.authorize(http)

        people_service = build(serviceName='people', version='v1', http=http)

        results = people_service.people().connections().list(
            resourceName='people/me',
            pageSize=10,
            personFields='emailAddresses,names').execute()
        connections = results.get('connections', [])

        # Get credentials for google calendar with smart.box@focus-corporation.com
        # and token management
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
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
        # Getting the event you want to update
        title = self.get_response('what\'s the name of the event')
        events_result = service.events().list(calendarId='primary',
                                              maxResults=1, singleEvents=True,
                                              orderBy='startTime', q=title).execute()
        events = events_result.get('items', [])
        if not events:
            self.speak('event not found')
        for event in events:
            eventid = event['id']

        # Getting inputs
        end = self.get_response('when does it end?')
        et = extract_datetime(end)
        event['start'] = et
        # Updating the Event
        service.events().update(calendarId='primary', eventId=eventid, body=event).execute()

    @intent_handler(IntentBuilder("").require("evening.bus"))
    def handle_update_name(self):
        # Getting the credentials for G.People API
        storage = Storage('info.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid is True:
            credentials = tools.run_flow(FLOW, storage)

        http = httplib2.Http()
        http = credentials.authorize(http)

        people_service = build(serviceName='people', version='v1', http=http)

        results = people_service.people().connections().list(
            resourceName='people/me',
            pageSize=10,
            personFields='emailAddresses,names').execute()
        connections = results.get('connections', [])

        # Get credentials for google calendar with smart.box@focus-corporation.com
        # and token management
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
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
        # Getting the event you want to update
        title = self.get_response('what\'s the name of the event')
        events_result = service.events().list(calendarId='primary',
                                              maxResults=1, singleEvents=True,
                                              orderBy='startTime', q=title).execute()
        events = events_result.get('items', [])
        if not events:
            self.speak('event not found')
        for event in events:
            eventid = event['id']

        # Getting inputs
        ns = self.get_response('what\'s the new summery or title of your event?')
        event['summary'] = ns
        # Updating the Event
        service.events().update(calendarId='primary', eventId=eventid, body=event).execute()

    @intent_handler(IntentBuilder("").require("bus.number"))
    def handle_update_location(self):
        # list of rooms
        listofroomsadress = ['focus-corporation.com_3436373433373035363932@resource.calendar.google.com',
                             'focus-corporation.com_3132323634363237333835@resource.calendar.google.com',
                             'focus-corporation.com_3335353934333838383834@resource.calendar.google.com',
                             'focus-corporation.com_3335343331353831343533@resource.calendar.google.com',
                             'focus-corporation.com_3436383331343336343130@resource.calendar.google.com',
                             'focus-corporation.com_36323631393136363531@resource.calendar.google.com',
                             'focus-corporation.com_3935343631343936373336@resource.calendar.google.com'
                             'focus-corporation.com_3739333735323735393039@resource.calendar.google.com',
                             'focus-corporation.com_3132343934363632383933@resource.calendar.google.com',
                             'focus-corporation.com_3636383930383831343637@resource.calendar.google.com',
                             'focus-corporation.com_3538333137333939363039@resource.calendar.google.com',
                             'focus-corporation.com_38333135333134383939@resource.calendar.google.com']
        listofroomsnames = ['Midoun meeting room', 'Aiguilles Meeting Room', 'Barrouta Meeting Room',
                            'Kantaoui Meeting Room', 'Gorges Meeting Room', 'Ichkeul Meeting Room',
                            'Khemir Meeting Room', 'Tamaghza Meeting Room', 'Friguia Meeting Room',
                            'Ksour Meeting Room', 'Medeina Meeting Room', 'Thyna Meeting Room']
        # Getting the credentials for G.People API
        storage = Storage('info.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid is True:
            credentials = tools.run_flow(FLOW, storage)

        http = httplib2.Http()
        http = credentials.authorize(http)

        people_service = build(serviceName='people', version='v1', http=http)

        results = people_service.people().connections().list(
            resourceName='people/me',
            pageSize=10,
            personFields='emailAddresses,names').execute()
        connections = results.get('connections', [])

        # Get credentials for google calendar with smart.box@focus-corporation.com
        # and token management
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
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
        # Getting the event you want to update
        title = self.get_response('what\'s the name of the event')
        events_result = service.events().list(calendarId='primary',
                                              maxResults=1, singleEvents=True,
                                              orderBy='startTime', q=title).execute()
        events = events_result.get('items', [])
        if not events:
            self.speak('event not found')
        for event in events:
            eventid = event['id']
            attendees = event['attendees']
            l = len(attendees)

        # Getting inputs
        r = self.get_response('what\'s the new location of your event?')
        maxattendees = 10
        if r == "Midoun meeting room":
            room = "focus-corporation.com_3436373433373035363932@resource.calendar.google.com"
        elif r == "Aiguilles Meeting Room":
            room = "focus-corporation.com_3132323634363237333835@resource.calendar.google.com"
        elif r == "Barrouta Meeting Room":
            room = "focus-corporation.com_3335353934333838383834@resource.calendar.google.com"
        elif r == "Kantaoui Meeting Room":
            room = "focus-corporation.com_3335343331353831343533@resource.calendar.google.com"
        elif r == "Gorges Meeting Room":
            room = "focus-corporation.com_3436383331343336343130@resource.calendar.google.com"
        elif r == "Ichkeul Meeting Room":
            room = "focus-corporation.com_36323631393136363531@resource.calendar.google.com"
        elif r == "Khemir Meeting Room":
            room = "focus-corporation.com_3935343631343936373336@resource.calendar.google.com"
        elif r == "Tamaghza Meeting Room":
            room = "focus-corporation.com_3739333735323735393039@resource.calendar.google.com"
        elif r == "Friguia Meeting Room":
            room = "focus-corporation.com_3132343934363632383933@resource.calendar.google.com"
            maxattendees = 15
        elif r == "Ksour Meeting Room":
            room = "focus-corporation.com_3636383930383831343637@resource.calendar.google.com"
        elif r == "Medeina Meeting Room":
            room = "focus-corporation.com_3538333137333939363039@resource.calendar.google.com"
        elif r == "Thyna Meeting Room":
            room = "focus-corporation.com_38333135333134383939@resource.calendar.google.com"

        # fel partie hethi lazem nzid script elli yekhou les attendees ou ntesti 3lihom nkharej el room ou ba3ed
        # nbadel el valeur kahaw
        meetingroom = []
        mr = {'email': room}
        meetingroom.append(mr)
        event['attendees'] = meetingroom
        # Updating the Event
        service.events().update(calendarId='primary', eventId=eventid, body=event).execute()

    @intent_handler(IntentBuilder("").require("seat.number"))
    def handle_seat_number(self):
        np = self.settings.get("np")
        self.speak_dialog("seat.number", data={"np": np})


def create_skill():
    return UpdateEvent()
