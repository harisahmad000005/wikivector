import wikipedia

def fetch_page(topic: str) -> str:
    wikipedia.set_lang("en")
    return wikipedia.page(topic).content
