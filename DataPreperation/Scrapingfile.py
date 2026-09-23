# This Python script scrapes deck lists from https://dotgg.gg/ 


import requests
import json
from urllib.parse import quote

# URL for API call
BASE_URL = "https://api.dotgg.gg"

# Functions to fetch cards and deck lists
def get_cards(game):
    response = requests.get(f"{BASE_URL}/cgfw/getcards?game={game}")
    return response.json()

def get_deck(game, slug):
    response = requests.get(f"{BASE_URL}/cgfw/getdeck?game={game}&slug={slug}")
    return response.json()



def search_decks(game, search_term="", current_page=1):
    request = {
        "page": current_page,
        "limit": 30,
        "srt": "date",
        "direct": "desc",
        "type": "",
        "my": 0,
        "myarchive": 0,
        "fav": 0,
        "getdecks": {
            "hascrd": [],
            "nothascrd": [],
            "youtube": 0,
            "smartsrch": search_term,
            "date": "",
            "color": [],
            "collection": 0,
            "topset": "",
            "at": 0,
            "format": "",
            "is_tournament": ""
        }
    }

    url = f"{BASE_URL}/cgfw/getdecks?game={game}&rq={quote(json.dumps(request))}"
    response = requests.get(url)
    return response.json()
 
import time

def search_decks_all_pages(game, search_term=""):
    """Fetch all deck pages and return as a single flattened list."""
    all_decks = []
    page = 1
    
    while True:
        result = search_decks(game, search_term, page)
        
        # Check if result has decks; adjust based on API response structure
        if isinstance(result, list) and len(result) > 0:
            all_decks.extend(result)
            print(f"Page {page}: Fetched {len(result)} decks (Total: {len(all_decks)})")
            page += 1
        elif isinstance(result, dict) and 'data' in result and len(result['data']) > 0:
            all_decks.extend(result['data'])
            print(f"Page {page}: Fetched {len(result['data'])} decks (Total: {len(all_decks)})")
            page += 1
        else:
            print(f"Page {page}: No more decks found. Finished.")
            break
        
        # Wait 1 second before next API call
        time.sleep(1)
    
    return all_decks

# One-line execution with auto-pagination
all_nami_decks = search_decks_all_pages('onepiece', 'nami')
with open("Decks/nami.json", "w", encoding="utf-8") as f:
    json.dump(all_nami_decks, f, indent=4, ensure_ascii=False)

print(f"\nTotal decks saved: {len(all_nami_decks)}")


