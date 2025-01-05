import os.path
import datetime as dt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from findDates import due_dates

SCOPES = ["https://www.googleapis.com/auth/calendar"]


# Centralized credential management
def get_credentials():
    creds = None
    # Check if the token file exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid token or credentials are invalid, prompt reauthorization
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def main():
    creds = get_credentials()  # Use get_credentials to handle the OAuth flow

    try:
        service = build("calendar", "v3", credentials=creds)

        if not due_dates:
            print("No events found")
        else:
            for event in due_dates:
                # Call to Google Calendar API here
                event_result = service.events().insert(calendarId='primary', body=event).execute()
                print(f"Event created {event_result.get('htmlLink')}")

    except HttpError as error:
        print("An error has occurred", error)


if __name__ == "__main__":
    main()
