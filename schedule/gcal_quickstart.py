from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly'] # read.only
SCOPES = ['https://www.googleapis.com/auth/calendar']

class EventBuilder:

    def __init__(self):
        self.output = {}
        self.timezone = "Asia/Singapore"

    def add_event(self, subject_code, subject_name):
        self.output['summary'] = f"{subject_code} - {subject_name}"
        return self

    def add_location(self, location):
        self.output['location'] = f"{location}"
        return self

    def add_description(self, description):
        self.output['description'] = f"{description}"
        return self

    def add_startTime(self, date, start_time, timezone="Asia/Singapore"):
        self.output['start'] = {'dateTime':f"{date}T{start_time}",
                                'timeZone':timezone}
        return self

    def add_endTime(self, date, end_time, timezone="Asia/Singapore"):
        self.output['end'] = {'dateTime':f"{date}T{end_time}",
                                'timeZone':timezone}
        return self

    def build(self):
        return self.output
    
class Gcal:

    def __init__(self, calendar_id='primary'):
        self.creds_file = 'credentials.json'
        self.creds = None
        self.calendar_id = calendar_id
        self._set_creds()
        self.service = build('calendar', 'v3', credentials=self.creds)
    
    def _set_creds(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.creds_file, SCOPES)
                self.creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

    def _create_event(self, event, calendar_id=""):
        if calendar_id == "":
            calendar_id = self.calendar_id
        event = self.service.events().insert(calendarId=calendar_id, body=event).execute()
        print ('Event created: %s' % (event.get('htmlLink')))

    def create_events(self,event_list):
        for event in event_list:
            self._create_event(event)
        print("All Events Created")

    def view_events(self,calendar_id=""):
        if calendar_id == "":
            calendar_id = self.calendar_id
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = self.service.events().list(calendarId=calendar_id, timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
    
def main():
    gcal = Gcal()
    gcal.view_events('primary')
    event = (EventBuilder()
    .add_event("50.001","Introduction to Information Systems")
    .add_location("CC13")
    .add_startTime("2019-04-23","12:00:00")
    .add_endTime("2019-04-23","15:00:00")
    .build())
    events = []
    events.append(event)
    gcal.create_events(events)
    

if __name__ == '__main__':
    main()
