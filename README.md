# Godoy Cruz Calendar Sync 🏆⚽

Automatically fetch upcoming Godoy Cruz matches from Promiedos and sync them to Google Calendar.

## Features

✅ Scrapes next 5 matches from Promiedos  
✅ Extracts match details (date, time, opponent, competition)  
✅ Syncs to Google Calendar automatically  
✅ Updates existing events if data changes  
✅ Configurable via `.env` file  
✅ Color-coded events (lavanda by default)  
✅ Custom reminders and duration  

## Installation

### 1. Clone/Download the project

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **Google Calendar API**
4. Create **OAuth 2.0 credentials** (Desktop app)
5. Download credentials as `credentials.json`
6. Add your email as a **Test User** in OAuth consent screen

### 4. Set up environment variables

Copy the example file:
```bash
cp .env.example .env
```

Edit `.env` with your preferences:
```env
# Promiedos Configuration
TEAM_URL=https://www.promiedos.com.ar/team/godoy-cruz/ihd
TEAM_NAME=Godoy Cruz
OUTPUT_JSON=matches.json

# Google Calendar Configuration
CALENDAR_ID=primary
CREDENTIALS_FILE=credentials.json
TOKEN_FILE=token.pickle

# Event Configuration
EVENT_DURATION_HOURS=2
REMINDER_MINUTES=60
EVENT_COLOR_ID=1

# Timezone
TIMEZONE=America/Argentina/Buenos_Aires
```

## Usage

### Run everything at once:

```bash
python main.py
```

This will:
1. Fetch matches from Promiedos
2. Save to `matches.json`
3. Sync with Google Calendar

### Or run individually:

```bash
# Just fetch matches
python scraper.py

# Just sync to calendar
python google_calendar.py
```

## Configuration Options

### Event Color IDs

Change `EVENT_COLOR_ID` in `.env`:

- `1` = Lavanda (default)
- `2` = Salvia
- `3` = Uva
- `4` = Flamingo
- `5` = Banana
- `6` = Mandarina
- `7` = Pavo real
- `8` = Grafito
- `9` = Arándano
- `10` = Albahaca
- `11` = Tomate

### Use Different Calendar

Instead of `primary`, use a specific calendar ID:

```env
CALENDAR_ID=your-calendar-id@group.calendar.google.com
```

To find your calendar ID:
1. Go to Google Calendar settings
2. Select the calendar
3. Scroll to "Integrate calendar"
4. Copy the Calendar ID

### Change Team

To track a different team, update `.env`:

```env
TEAM_URL=https://www.promiedos.com.ar/team/river-plate/igi
TEAM_NAME=River Plate
```

## Project Structure

```
.
├── main.py                 # Main entry point
├── scraper.py             # Promiedos scraper
├── google_calendar.py     # Google Calendar sync
├── requirements.txt       # Python dependencies
├── .env                   # Configuration (create from .env.example)
├── .env.example          # Configuration template
├── credentials.json      # Google OAuth credentials (download)
├── token.pickle          # Auth token (auto-generated)
└── matches.json          # Scraped matches (auto-generated)
```

## Troubleshooting

**"credentials.json not found"**
- Download OAuth credentials from Google Cloud Console

**"Error 403: access_denied"**
- Add your email as Test User in OAuth consent screen

**"matches.json not found"**
- Run `python scraper.py` first, or run `python main.py`

**Events not updating**
- The script uses Match ID to identify duplicates
- If you manually edited an event, it might not update

**Wrong timezone**
- Update `TIMEZONE` in `.env`
- List of timezones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

## Automation

### Schedule with cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Run every day at 9 AM
0 9 * * * cd /path/to/project && /usr/bin/python3 main.py >> sync.log 2>&1
```

### Schedule with Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., Daily at 9 AM)
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\main.py`
7. Start in: `C:\path\to\project`

## Security Notes

⚠️ **Do NOT commit these files:**
- `credentials.json`
- `token.pickle`
- `.env`

Add to `.gitignore`:
```
credentials.json
token.pickle
token.json
.env
matches.json
*.log
```

## License

Free to use for personal purposes.

## Support

For issues or questions, check:
- [Google Calendar API Docs](https://developers.google.com/calendar/api)
- [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
