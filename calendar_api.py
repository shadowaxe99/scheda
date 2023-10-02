from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json
import pickle
import firebase_admin
from firebase_admin import credentials, storage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
from cryptography.fernet import Fernet

# Initialize Firebase Admin SDK (only do this once in your application)
cred = credentials.Certificate('firebase_secrets.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'enter-bucket-name-here'
})

def get_calendar_service(email_id):
    # Fetch serialized credentials from Firebase Storage
    bucket = storage.bucket()
    blob = bucket.blob(email_id)
    serialized_credentials = blob.download_as_text()

    # Deserialize the credentials
    # serialized_credentials = fernet.decrypt(encrypted_serialized_credentials)
    cred_info = json.loads(serialized_credentials)
    creds = Credentials(
        token=cred_info['token'],
        refresh_token=cred_info['refresh_token'],
        token_uri=cred_info['token_uri'],
        client_id=cred_info['client_id'],
        client_secret=cred_info['client_secret'],
        scopes=cred_info['scopes']
    )

    # Build the calendar service
    service = build('calendar', 'v3', credentials=creds)
    return service


# Fetch free time slots for the next two months
def fetch_free_time(email_address):
    calendar_service = get_calendar_service(email_address)

    now = datetime.utcnow()
    end_time = now + timedelta(days=20)

    # Fetch the free/busy information
    body = {
        "timeMin": now.isoformat() + 'Z',
        "timeMax": end_time.isoformat() + 'Z',
        "items": [{"id": email_address}]
    }
    free_busy_response = calendar_service.freebusy().query(body=body).execute()

    # Extract the busy times
    busy_times = free_busy_response['calendars'][email_address]['busy']

    # Check if there are no upcoming events
    if not busy_times:
        return "You are free for the next 20 days."

    # Calculate the free times based on the busy times
    free_slots = []
    prev_end_time = now
    for busy in busy_times:
        busy_start = datetime.fromisoformat(busy['start'][:-1])
        busy_end = datetime.fromisoformat(busy['end'][:-1])
        if busy_start != prev_end_time:
            free_slots.append((prev_end_time, busy_start))
        prev_end_time = busy_end

    if prev_end_time != end_time:
        free_slots.append((prev_end_time, end_time))

    # Group free slots by day and format them
    free_slots_by_day = {}
    for start, end in free_slots:
        day = start.strftime('%Y-%m-%d')
        time_range = f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')} GMT"
        if day in free_slots_by_day:
            free_slots_by_day[day].append(time_range)
        else:
            free_slots_by_day[day] = [time_range]

    # Convert the grouped free slots into a human-readable format
    formatted_free_slots = []
    for day, time_ranges in free_slots_by_day.items():
        formatted_day = datetime.fromisoformat(day).strftime('%A, %d %B %Y')
        formatted_time_ranges = ', '.join(time_ranges)
        formatted_free_slots.append(f"{formatted_day}: {formatted_time_ranges}")

    return '\n'.join(formatted_free_slots)


if __name__ == '__main__':
    print(fetch_free_time("shivam@elysiuminnovations.ai"))
