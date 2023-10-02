import pickle
from flask import Flask, render_template, request, redirect
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    role = request.form.get('role')
    if role == 'owner':
        calendar_service = get_calendar_service()
        # Save owner's email to owner_email.txt
        with open('owner_email.txt', 'w') as f:
            f.write(calendar_service.calendarList().get(calendarId='primary').execute()['id'])
        with open('calendar_service.pkl', 'wb') as f:
            pickle.dump(calendar_service, f)
    elif role == 'assistant':
        gmail_service = get_gmail_service()
        # Save assistant's email to assistant_email.txt
        with open('assistant_email.txt', 'w') as f:
            f.write(gmail_service.users().getProfile(userId='me').execute()['emailAddress'])
        with open('gmail_service.pkl', 'wb') as f:
            pickle.dump(gmail_service, f)
    return redirect('/')

def get_gmail_service():
    gmail_creds = None
    gmail_scopes = ['https://www.googleapis.com/auth/gmail.modify']

    if gmail_creds and not gmail_creds.valid:
        if gmail_creds.expired and gmail_creds.refresh_token:
            gmail_creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', gmail_scopes)
        gmail_creds = flow.run_local_server(port=0)
        with open('gmail_token.json', 'w') as token:
            token.write(gmail_creds.to_json())

    gmail_service = build('gmail', 'v1', credentials=gmail_creds)
    with open('gmail_service.pkl', 'wb') as f:
        pickle.dump(gmail_service, f)
    return gmail_service

def get_calendar_service():
    calendar_creds = None
    calendar_scopes = ['https://www.googleapis.com/auth/calendar']

    if calendar_creds and not calendar_creds.valid:
        if calendar_creds.expired and calendar_creds.refresh_token:
            calendar_creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', calendar_scopes)
        calendar_creds = flow.run_local_server(port=0)
        with open('calendar_token.json', 'w') as token:
            token.write(calendar_creds.to_json())

    calendar_service = build('calendar', 'v3', credentials=calendar_creds)
    with open('calendar_service.pkl', 'wb') as f:
        pickle.dump(calendar_service, f)
    return calendar_service

if __name__ == '__main__':
    app.run(debug=True)
