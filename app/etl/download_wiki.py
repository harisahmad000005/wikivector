import requests
import bz2
import os

WIKI_URL = "https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2"
SAVE_PATH = "data/enwiki-latest-pages-articles.xml.bz2"

os.makedirs("data", exist_ok=True)

def download_wiki():
    if not os.path.exists(SAVE_PATH):
        print("Downloading Wikipedia dump...")
        response = requests.get(WIKI_URL, stream=True)
        with open(SAVE_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024*1024):
                f.write(chunk)
        print("Download completed.")
    else:
        print("Dump already exists.")

if __name__ == "__main__":
    download_wiki()
