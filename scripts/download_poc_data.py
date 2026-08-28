import urllib.request
import urllib.parse
import json
import os
import time

# Create folders for English and Khmer raw data
os.makedirs("data/raw/en", exist_ok=True)
os.makedirs("data/raw/km", exist_ok=True)

topics = {
    "en": ["Cambodia", "Angkor_Wat", "Siem_Reap", "Phnom_Penh", "Tonlé_Sap", "Culture_of_Cambodia", "Khmer_language"],
    "km": ["កម្ពុជា", "អង្គរវត្ត", "ខេត្តសៀមរាប", "រាជធានីភ្នំពេញ", "បឹងទន្លេសាប", "វប្បធម៌ខ្មែរ", "ភាសាខ្មែរ"]
}

def fetch_wikipedia_text(title, lang):
    safe_title = urllib.parse.quote(title)
    url = f"https://{lang}.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&titles={safe_title}&format=json"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'CambodiaTourismLM-PoC/1.1'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            pages = data['query']['pages']
            for page_id in pages:
                if page_id != "-1":
                    return pages[page_id].get('extract', '')
    except Exception as e:
        print(f"Error fetching {title} ({lang}): {e}")
    return ""

print("Downloading Proof-of-Concept dataset from Wikipedia...")

for lang, titles in topics.items():
    for title in titles:
        filepath = f"data/raw/{lang}/{title}.txt"
        
        # Skip if we already downloaded this file successfully
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            print(f"Skipping {title} ({lang}) - already downloaded.")
            continue
            
        print(f"Fetching: {title} ({lang})...")
        text = fetch_wikipedia_text(title, lang)
        
        if text:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)
                
        # Pause for 2 seconds to be polite to Wikipedia's servers
        time.sleep(2)

print("\nData collection complete! Texts are saved in data/raw/")