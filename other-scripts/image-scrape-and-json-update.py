# /other-scripts/image-scrape-and-json-update.py

import requests
import json
import os
import re
import time
import argparse
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# ── LOAD ENVIRONMENT VARIABLES ─────────────────────────────────────
load_dotenv()

AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
ACCOUNT_NAME = os.getenv("AZURE_ACCOUNT_NAME")

# ── HARDCODED CONFIGURATION ────────────────────────────────────────
CONTAINER_NAME = "flashcard-other-files"
FOLDER_NAME = "images"

if not AZURE_CONNECTION_STRING or not ACCOUNT_NAME:
    raise ValueError("Missing Azure credentials in .env file!")

BLOB_BASE_URL = f"https://{ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{FOLDER_NAME}/"
INPUT_JSON = "../frontend/cards.json"
OUTPUT_JSON = "../frontend/updated_cards.json"

HEADERS = {
    "User-Agent": "FlashcardBot/1.0 (contact: your@email.com) Mozilla/5.0",
    "Accept": "application/json"
}

def get_wikipedia_image_urls(search_term):
    """Uses Wikipedia Action API to find high-res image URLs."""
    api_url = "https://en.wikipedia.org/w/api.php"
    try:
        search_params = {"action": "query", "list": "search", "srsearch": search_term, "format": "json", "srlimit": 1}
        r = requests.get(api_url, params=search_params, headers=HEADERS, timeout=10)
        r.raise_for_status()
        search_results = r.json().get("query", {}).get("search", [])
        
        if not search_results: return []
        page_title = search_results[0]['title']

        img_params = {"action": "query", "prop": "images", "titles": page_title, "format": "json", "imlimit": 20}
        r = requests.get(api_url, params=img_params, headers=HEADERS, timeout=10)
        r.raise_for_status()
        
        pages = r.json().get("query", {}).get("pages", {})
        page_id = list(pages.keys())[0]
        image_list = pages[page_id].get("images", [])

        valid_urls = []
        for img in image_list:
            img_title = img['title']
            if any(ext in img_title.lower() for ext in ['.jpg', '.jpeg', '.png']):
                if not any(noise in img_title.lower() for noise in ['icon', 'map', 'stub', 'logo', 'button']):
                    url_params = {"action": "query", "prop": "imageinfo", "titles": img_title, "iiprop": "url", "format": "json"}
                    img_r = requests.get(api_url, params=url_params, headers=HEADERS, timeout=10)
                    img_r.raise_for_status()
                    img_pages = img_r.json().get("query", {}).get("pages", {})
                    img_id = list(img_pages.keys())[0]
                    actual_url = img_pages[img_id].get("imageinfo", [{}])[0].get("url")
                    if actual_url: valid_urls.append(actual_url)
            if len(valid_urls) >= 2: break 
        return valid_urls
    except Exception as e:
        print(f"      ❌ API Error: {e}")
        return []

def download_and_upload(url, filename, container_client, overwrite_flag):
    """Downloads image and uploads to Azure. Skips if exists unless overwrite_flag is True."""
    try:
        blob_path = f"{FOLDER_NAME}/{filename}"
        blob_client = container_client.get_blob_client(blob=blob_path)

        # Skip logic
        if not overwrite_flag and blob_client.exists():
            print(f"      ⏭️ Skipping {filename} (already in Blob)")
            return True

        response = requests.get(url, headers=HEADERS, stream=True, timeout=15)
        response.raise_for_status()
        
        blob_client.upload_blob(response.content, overwrite=True)
        print(f"      ✅ Uploaded to {CONTAINER_NAME}/{blob_path}")
        return True
    except Exception as e:
        print(f"      ❌ Download/Upload Error: {e}")
        return False

def clean_search_term(text):
    text = str(text)
    if text.lower().startswith("the "): text = text[4:]
    text = re.sub(r'\(.*?\)', '', text)
    return text.strip()

def main():
    parser = argparse.ArgumentParser(description="Scrape Wikipedia images and update flashcard JSON.")
    parser.add_argument('--overwrite', action='store_true', help="Overwrite existing images.")
    args = parser.parse_args()

    print(f"☁️ Connecting to Azure (Container: {CONTAINER_NAME})...")
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        if not container_client.exists():
            container_client.create_container(public_access='blob')
    except Exception as e:
        print(f"❌ Connection Error: {e}"); return

    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    update_count = 0
    for deck_name, deck_data in data.get("decks", {}).items():
        print(f"\n📂 Scanning Deck: {deck_name}")
        
        # Deck-level images
        for key in ["q_image", "a_image"]:
            val = deck_data.get(key)
            if val and not str(val).startswith("http"):
                urls = get_wikipedia_image_urls(clean_search_term(deck_name))
                if urls and download_and_upload(urls[0], val, container_client, args.overwrite):
                    deck_data[key] = BLOB_BASE_URL + val
                    update_count += 1

        # Card-level images
        for card in deck_data.get("cards", []):
            q_img = card.get("q_image"); a_img = card.get("a_image")
            needs_q = q_img and not str(q_img).startswith("http")
            needs_a = a_img and not str(a_img).startswith("http")
            if not needs_q and not needs_a: continue

            search_term = clean_search_term(card.get("a", ""))
            
            # Smart skip check
            q_path = f"{FOLDER_NAME}/{q_img}"; a_path = f"{FOLDER_NAME}/{a_img}"
            q_exists = not args.overwrite and container_client.get_blob_client(q_path).exists() if needs_q else True
            a_exists = not args.overwrite and container_client.get_blob_client(a_path).exists() if needs_a else True

            if q_exists and a_exists:
                if needs_q: card["q_image"] = BLOB_BASE_URL + q_img
                if needs_a: card["a_image"] = BLOB_BASE_URL + a_img
                update_count += (1 if needs_q else 0) + (1 if needs_a else 0)
                continue

            valid_urls = get_wikipedia_image_urls(search_term)
            if not valid_urls: continue

            if needs_q and len(valid_urls) > 0:
                if download_and_upload(valid_urls[0], q_img, container_client, args.overwrite):
                    card["q_image"] = BLOB_BASE_URL + q_img
                    update_count += 1
            if needs_a and len(valid_urls) > 1:
                if download_and_upload(valid_urls[1], a_img, container_client, args.overwrite):
                    card["a_image"] = BLOB_BASE_URL + a_img
                    update_count += 1
            time.sleep(0.5)

    # ── CUSTOM JSON FORMATTING ──
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    
    # Matches objects containing "q": and flattens them, preserving leading indentation
    compact_json = re.sub(
        r'(?ms)^(\s+)\{(.*?"q":.*?)\n\s+\}(,?)', 
        lambda m: f'{m.group(1)}{{ {re.sub(r"\s*\n\s*", " ", m.group(2).strip())} }}{m.group(3)}', 
        json_str
    )

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        f.write(compact_json)
    
    print(f"\n🎉 Done! Updated {update_count} image references.")

if __name__ == "__main__":
    main()