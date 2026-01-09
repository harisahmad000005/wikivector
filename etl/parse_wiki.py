import xml.etree.ElementTree as ET
import bz2
import re
import os
import json

INPUT_FILE = "data/enwiki-latest-pages-articles.xml.bz2"
OUTPUT_FILE = "data/articles_cleaned.jsonl"

def clean_text(text):
    text = re.sub(r"\[\[.*?\|?(.*?)\]\]", r"\1", text)  # remove wiki links
    text = re.sub(r"<.*?>", "", text)  # remove HTML tags
    text = re.sub(r"\{\{.*?\}\}", "", text)  # remove templates
    text = re.sub(r"\n+", "\n", text).strip()
    return text

def parse_dump():
    print("Parsing Wikipedia dump...")
    with bz2.open(INPUT_FILE, "rt") as f, open(OUTPUT_FILE, "w") as out:
        context = ET.iterparse(f, events=("end",))
        for event, elem in context:
            if elem.tag.endswith("page"):
                title = elem.findtext(".//title")
                text = elem.findtext(".//text") or ""
                text = clean_text(text)
                if text:
                    json.dump({"title": title, "text": text}, out)
                    out.write("\n")
                elem.clear()
    print(f"Saved cleaned articles to {OUTPUT_FILE}")

if __name__ == "__main__":
    parse_dump()
