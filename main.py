"""
Main script to fetch Godoy Cruz matches and sync with Google Calendar
"""

import sys
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    print("="*60)
    print("Godoy Cruz Calendar Sync")
    print("="*60)
    print()
    
    print("Step 1: Fetching matches from Promiedos...")
    print("-" * 60)
    
    try:
        import scraper
        success = scraper.main()
        
        if not success:
            print("\n❌ Failed to fetch matches")
            return 1
        
    except Exception as e:
        print(f"\n❌ Error running scraper: {e}")
        return 1
    
    print()
    print("Step 2: Syncing with Google Calendar...")
    print("-" * 60)
    
    try:
        import google_calendar
        success = google_calendar.main()
        
        if not success:
            print("\n❌ Failed to sync with calendar")
            return 1
        
    except Exception as e:
        print(f"\n❌ Error syncing calendar: {e}")
        return 1
    
    print()
    print("="*60)
    print("✅ Sync completed successfully!")
    print("="*60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
