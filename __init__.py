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

    @intent_handler(IntentBuilder("").require("update.start"))
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
        self.speak_dialog('successful.update')

    @intent_handler(IntentBuilder("").require("update.start"))
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
        self.speak_dialog('successful.update')

    @intent_handler(IntentBuilder("").require("update.name"))
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
        self.speak_dialog('successful.update')

    @intent_handler(IntentBuilder("").require("update.location"))
    def handle_update_location(self):
        # list of rooms
        listofroomsadress = ['focus-corporation.com_3436373433373035363932@resource.calendar.google.com',
                             'focus-corporation.com_3132323634363237333835@resource.calendar.google.com',
                             'focus-corporation.com_3335353934333838383834@resource.calendar.google.com',
                             'focus-corporation.com_3335343331353831343533@resource.calendar.google.com',
                             'focus-corporation.com_3436383331343336343130@resource.calendar.google.com',
                             'focus-corporation.com_36323631393136363531@resource.calendar.google.com',
                             'focus-corporation.com_3935343631343936373336@resource.calendar.google.com',
                             'focus-corporation.com_3739333735323735393039@resource.calendar.google.com',
                             'focus-corporation.com_3132343934363632383933@resource.calendar.google.com',
                             'focus-corporation.com_3636383930383831343637@resource.calendar.google.com',
                             'focus-corporation.com_3538333137333939363039@resource.calendar.google.com',
                             'focus-corporation.com_38333135333134383939@resource.calendar.google.com']
        listofroomsnames = ['FOCUS-1ere-Midoune Meeting Room (10)', 'FOCUS-1ere-Aiguilles Meeting Room (10)',
                            'FOCUS-1ere-Barrouta Meeting Room (10)', 'FOCUS-1ere-Kantaoui Meeting Room (10)',
                            'FOCUS-2eme-Gorges Meeting Room (10)', 'FOCUS-2eme-Ichkeul Meeting Room (10)',
                            'FOCUS-2eme-Khemir Meeting Room (10)', 'FOCUS-2eme-Tamaghza Meeting Room (10)',
                            'FOCUS-RDC-Friguia Meeting Room (15)', 'FOCUS-RDC-Ksour Meeting Room (10)',
                            'FOCUS-RDC-Medeina Meeting Room (10)', 'FOCUS-RDC-Thyna Meeting Room (10)']
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
            roomname = 'FOCUS-1ere-Aiguilles Meeting Room (10)'
        elif r == "Barrouta Meeting Room":
            room = "focus-corporation.com_3335353934333838383834@resource.calendar.google.com"
            roomname =''
        elif r == "Kantaoui Meeting Room":
            room = "focus-corporation.com_3335343331353831343533@resource.calendar.google.com"
            roomname = ''
        elif r == "Gorges Meeting Room":
            room = "focus-corporation.com_3436383331343336343130@resource.calendar.google.com"
            roomname = ''
        elif r == "Ichkeul Meeting Room":
            room = "focus-corporation.com_36323631393136363531@resource.calendar.google.com"
            roomname = ''
        elif r == "Khemir Meeting Room":
            room = "focus-corporation.com_3935343631343936373336@resource.calendar.google.com"
            roomname = ''
        elif r == "Tamaghza Meeting Room":
            room = "focus-corporation.com_3739333735323735393039@resource.calendar.google.com"
            roomname = ''
        elif r == "Friguia Meeting Room":
            room = "focus-corporation.com_3132343934363632383933@resource.calendar.google.com"
            roomname = ''
            maxattendees = 15
        elif r == "Ksour Meeting Room":
            room = "focus-corporation.com_3636383930383831343637@resource.calendar.google.com"
        elif r == "Medeina Meeting Room":
            room = "focus-corporation.com_3538333137333939363039@resource.calendar.google.com"
        elif r == "Thyna Meeting Room":
            room = "focus-corporation.com_38333135333134383939@resource.calendar.google.com"

        # In this part we have to get the list of attendees, then extract the email of the meeting room to reserve
        # then change it with the email matching the input new location to the email list of rooms
        o = 0
        p = 0
        t = 0
        y = 0
        attendemail = []
        attendname = []
        finallist = []
        l = len(attendees)
        while o != l:
            attendemail.append(attendees[o]['email'])
            attendname.append(attendees[o].get('displayName'))
            o = o + 1
        while p != len(attendemail):
            while t != len(listofroomsadress):
                if attendemail[p] == listofroomsadress[t]:
                    attendemail[p] = room
                    attendname[p] == r
                t = t + 1
            p = p + 1
        while y != len(attendemail):
            mr = {'email': attendemail[y]}
            finallist.append(mr)
            y = y + 1

        event['attendees'] = finallist
        # event['location'] = r
        updated_event = service.events().update(calendarId='primary', eventId=eventid, body=event).execute()
        # Updating the Event
        service.events().update(calendarId='primary', eventId=eventid, body=event).execute()
        self.speak_dialog('successful.update')

    @intent_handler(IntentBuilder("").require("add.attendees"))
    def handle_add_attendees(self):
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
            invitedattendees = event['attendees']
            eventid = event['id']
        # Getting the contact ALL READY invited
        invitedattendemail = []
        invitedattendname = []
        o = 0
        l = len(invitedattendees)
        while o != l:
            invitedattendemail.append(invitedattendees[o]['email'])
            invitedattendname.append(invitedattendees[o].get('displayName'))
            o = o + 1
        # at this stage we have 3 lists
        # 1) invitedattend[] which is what we get from the google calendar
        # 2) invitedattendname[]the list of names of each attendee
        # 3) invitedattendemail[] the list of emails of each attendee

        # Now we have to figure out the number of attendees that we can add no more then the capacity of the room
        maxattendees = 10
        if event['location'] == 'FOCUS-RDC-Friguia Meeting Room (15)':
            maxattendees = 15
        at = self.get_response('how many attendees would like to add ?')
        na = maxattendees - at
        if l == maxattendees:
            self.speak('infortunatly you can\'t add more attendees because the room is full')
        elif na < at:
            self.speak_dialog('max.attendees ', data={'na': na})
        else:
            na = at

        # Getting the Attendees from input
        attemail = []
        noms = []
        f = 0
        i = 1
        g = 0
        found = False
        found2 = False
        # get all contacts in a list
        for person in connections:
            emailAddresses = person.get('emailAddresses', [])
            names = person.get('names', [])
            attemail.append(emailAddresses[0].get('value'))
            noms.append(names[0].get('displayName'))
        # print(noms)
        p = len(noms)
        # Int a list of attendees and it's length is the maximum number of attendees according to the room chosen befor
        attendees = ['blabla@blabla'] * na
        # first attendee
        # print('attendees :')
        a = self.get_response('how do you want to add ?')
        # looking for the contact in contact list
        if a != '':
            while (g != p) & (found is False):
                # if the name in the input matches the a name in the list we add the email of that person to the attendees
                # list which will be treated later to delete the examples 'blabla@blabla.com'
                if noms[g] == a:
                    attendees[0] = attemail[g]
                    g = g + 1
                    found = True
                else:
                    g = g + 1
            if found is False:
                self.speak('contact not found try again please')
        else:
            self.speak('no attendees added')
        # other attendees to add less then max number of attendees
        while i != na:
            a = self.get_response('how many attendees would like to add ?')
            if a == '':
                break
            else:
                while (f != p) | (found2 is False):
                    if noms[f] == a:
                        attendees[i] = attemail[f]
                        found2 = True
                    f = f + 1
            i = i + 1
        # until this stage we have a list of attendees + blanks filled with blabla@blabla.om
        l = len(attendees)
        # in this part we are going to get the attendees without the blanks
        t = 0
        att = []
        while t != l:
            if attendees[t] != 'blabla@blabla':
                att.append(attendees[t])
                t = t + 1
            else:
                t = t + 1
        w = 0
        attendemail = []
        while w != len(attendees):
            attendemail.append(attendees[w])
            w = w + 1
        attendee = []
        for s in range(len(invitedattendemail)):
            email = {'email': invitedattendemail[s]}
            attendee.append(email)
        for r in range(len(attendemail)):
            email = {'email': attendemail[r]}
            attendee.append(email)
        event['attendees'] = attendee

        updated_event = service.events().update(calendarId='primary', eventId=eventid, body=event).execute()
        self.speak_dialog('successful.update')


def create_skill():
    return UpdateEvent()
