from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = os.getenv('CALENDAR_ID', 'primary')
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE', 'service_account.json')
TIMEZONE = os.getenv('TIMEZONE', 'America/Argentina/Buenos_Aires')
EVENT_DURATION_HOURS = int(os.getenv('EVENT_DURATION_HOURS', '2'))
REMINDER_MINUTES = int(os.getenv('REMINDER_MINUTES', '60'))
EVENT_COLOR_ID = os.getenv('EVENT_COLOR_ID', '1')
TEAM_NAME = os.getenv('TEAM_NAME', 'Godoy Cruz')
INPUT_JSON = os.getenv('OUTPUT_JSON', 'matches.json')

def authenticate_google_calendar():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        raise FileNotFoundError(
            f"Service account file not found: {SERVICE_ACCOUNT_FILE}\n"
            "Please create a service account in Google Cloud Console."
        )
    
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    
    return build('calendar', 'v3', credentials=credentials)

def parse_date_time(fecha, hora):
    current_year = datetime.now().year
    date_str = f"{fecha}/{current_year} {hora}"
    
    dt = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
    
    dt_aware = dt.replace(tzinfo=ZoneInfo(TIMEZONE))
    
    return dt_aware

def event_exists(service, calendar_id, match_id):
    try:
        events_result = service.events().list(
            calendarId=calendar_id,
            q=match_id,
            singleEvents=True
        ).execute()
        
        events = events_result.get('items', [])
        
        for event in events:
            description = event.get('description', '')
            if f"Match ID: {match_id}" in description:
                return event['id']
        return None
    except Exception as e:
        print(f"Error checking if event exists: {e}")
        return None

def create_calendar_event(service, calendar_id, partido):
    match_id = partido['id']
    rival = partido['rival']
    fecha = partido['fecha']
    hora = partido['hora']
    local_visitante = partido['local_visitante']
    competicion = partido['competicion']
    
    existing_event_id = event_exists(service, calendar_id, match_id)
    
    if local_visitante == 'Local':
        title = f"{TEAM_NAME} vs {rival}"
    else:
        title = f"{rival} vs {TEAM_NAME}"
    
    start_dt = parse_date_time(fecha, hora)
    end_dt = start_dt + timedelta(hours=EVENT_DURATION_HOURS)
    
    event = {
        'summary': title,
        'description': f"Competition: {competicion}\nMatch ID: {match_id}",
        'start': {
            'dateTime': start_dt.isoformat(),
            'timeZone': TIMEZONE,
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': TIMEZONE,
        },
        'colorId': EVENT_COLOR_ID,
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': REMINDER_MINUTES},
            ],
        },
    }
    
    try:
        if existing_event_id:
            event = service.events().update(
                calendarId=calendar_id,
                eventId=existing_event_id,
                body=event
            ).execute()
            print(f"Event updated: {title} - {fecha} {hora}")
        else:
            event = service.events().insert(calendarId=calendar_id, body=event).execute()
            print(f"Event created: {title} - {fecha} {hora}")
        return event
    except Exception as e:
        print(f"Error creating/updating event: {e}")
        return None

def main():
    if not os.path.exists(INPUT_JSON):
        print(f"Error: {INPUT_JSON} not found. Run scraper first.")
        return False
    
    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        partidos = json.load(f)
    
    if not partidos:
        print("No matches to process")
        return False
    
    print("Authenticating with Google Calendar...")
    service = authenticate_google_calendar()
    
    print(f"\nProcessing {len(partidos)} matches...\n")
    
    created_count = 0
    updated_count = 0
    
    for partido in partidos:
        match_id = partido['id']
        existing_event_id = event_exists(service, CALENDAR_ID, match_id)
        
        result = create_calendar_event(service, CALENDAR_ID, partido)
        
        if result:
            if existing_event_id:
                updated_count += 1
            else:
                created_count += 1
    
    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Created: {created_count}")
    print(f"  Updated: {updated_count}")
    print(f"  Total: {len(partidos)}")
    print(f"{'='*50}")
    
    return True

if __name__ == '__main__':
    main()