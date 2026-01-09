from db.postgres import SessionLocal, RawArticle, CleanedArticle
import bz2, xml.etree.ElementTree as ET, re

INPUT_FILE = "data/enwiki-latest-pages-articles.xml.bz2"

def clean_text(text):
    text = re.sub(r"\[\[.*?\|?(.*?)\]\]", r"\1", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"\{\{.*?\}\}", "", text)
    text = re.sub(r"\n+", "\n", text).strip()
    return text

def parse_dump():
    session = SessionLocal()
    print("Parsing Wikipedia dump and saving to PostgreSQL...")
    with bz2.open(INPUT_FILE, "rt") as f:
        context = ET.iterparse(f, events=("end",))
        for event, elem in context:
            if elem.tag.endswith("page"):
                title = elem.findtext(".//title")
                text = elem.findtext(".//text") or ""
                cleaned_text = clean_text(text)
                
                if text:
                    raw_article = RawArticle(title=title, xml=text)
                    session.add(raw_article)
                    session.commit()
                    
                    # Split paragraphs and save
                    for idx, paragraph in enumerate(cleaned_text.split("\n\n")):
                        if paragraph.strip():
                            cleaned_article = CleanedArticle(title=title, paragraph=paragraph.strip(), chunk_id=idx)
                            session.add(cleaned_article)
                    session.commit()
                elem.clear()
    session.close()
    print("ETL Completed.")
