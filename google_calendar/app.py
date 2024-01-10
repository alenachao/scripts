import os.path
import csv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def authentication():
  """
  Completes authorization flow and builds service
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=3000)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    return build("calendar", "v3", credentials=creds)
  except HttpError as error:
    raise f"An error occurred: {error}"

def add_event(event_details, service):
  """
  Add event to calendar.
  """
  event = {
        'summary': event_details['summary'],
        'location': event_details.get('location', ''),
        'description': event_details.get('description', ''),
        'start': {
            'dateTime': event_details['start.dateTime'],
            'timeZone': event_details.get('start.timeZone', 'UTC'),
        },
        'end': {
            'dateTime': event_details['end.dateTime'],
            'timeZone': event_details.get('end.timeZone', 'UTC'),
        },
        'recurrence': event_details.get('recurrence', []),
        'attendees': event_details.get('attendees', []),
    }
    
  service.events().insert(calendarId='primary', body=event).execute()
    


def main():
  """
  Entry point.
  """
  service = authentication()

  # Read events from CSV file
  with open('events.csv', mode='r') as file:
      reader = csv.DictReader(file)
      for row in reader:
          # process attendees list:
          if row.get("attendees"):
            row["attendees"] = row["attendees"].split(",")

          # process recrurrence list:
          if row.get("recurrence"):
            row["recurrence"] = row["recurrence"].split(",")

          add_event(row, service)

  print("success!")


if __name__ == "__main__":
  main()