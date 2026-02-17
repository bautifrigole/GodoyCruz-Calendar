from bs4 import BeautifulSoup
import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

TEAM_URL = os.getenv('TEAM_URL', 'https://www.promiedos.com.ar/team/godoy-cruz/ihd')
TEAM_NAME = os.getenv('TEAM_NAME', 'Godoy Cruz')
OUTPUT_JSON = os.getenv('OUTPUT_JSON', 'matches.json')

def getNextMatches(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error fetching team page: {e}")
        return []
    
    try:
        script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
        if not script_tag:
            print("JSON script not found")
            return []
        
        data = json.loads(script_tag.string)
        page_data = data.get('props', {}).get('pageProps', {}).get('data', {})
        partidos_data = page_data.get('games', {}).get('next', {}).get('rows', [])
        
        if not partidos_data:
            print("No upcoming matches found")
            return []
        
        partidos = []
        for partido_row in partidos_data[:5]:
            game = partido_row.get('game', {})
            values = partido_row.get('values', [])
            entity = partido_row.get('entity', {}).get('object', {})
            
            fecha = next((v['value'] for v in values if v['key'] == 'date'), 'N/A')
            hora = next((v['value'] for v in values if v['key'] == 'time'), 'N/A')
            local_visitante = next((v['value'] for v in values if v['key'] == 'home_away'), 'L')
            rival = entity.get('short_name', 'N/A')
            game_id = game.get('id')
            game_url_name = game.get('url_name')
            
            competicion = 'N/A'
            if game_url_name and game_id:
                partido_url = f'https://www.promiedos.com.ar/game/{game_url_name}/{game_id}'
                competicion = getCompeticion(partido_url, headers)
                time.sleep(0.5)
            
            partidos.append({
                'id': game_id,
                'fecha': fecha,
                'hora': hora,
                'rival': rival,
                'local_visitante': 'Local' if local_visitante == 'L' else 'Visitante',
                'competicion': competicion
            })
        
        return partidos
        
    except Exception as e:
        print(f"Error processing data: {e}")
        return []

def getCompeticion(url_partido, headers):
    try:
        response = requests.get(url_partido, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
        if not script_tag:
            return 'N/A'
        
        data = json.loads(script_tag.string)
        game = data.get('props', {}).get('pageProps', {}).get('initialData', {}).get('game', {})
        league = game.get('league', {})
        
        return league.get('name', 'N/A')
    
    except Exception as e:
        print(f"Error fetching competition from {url_partido}: {e}")
        return 'N/A'

def main():
    print(f"Fetching matches for {TEAM_NAME}...")
    partidos = getNextMatches(TEAM_URL)
    
    if partidos:
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(partidos, f, ensure_ascii=False, indent=2)
        
        print(f"\nSaved {len(partidos)} matches to {OUTPUT_JSON}")
        
        for partido in partidos:
            print(f"{partido['fecha']} {partido['hora']} - {partido['rival']} ({partido['local_visitante']}) - {partido['competicion']} [ID: {partido['id']}]")
        
        return True
    else:
        print("No matches found")
        return False

if __name__ == "__main__":
    main()
