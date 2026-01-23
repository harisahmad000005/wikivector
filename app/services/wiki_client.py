import wikipedia

def fetch_wikipedia_chunks(title: str, chunk_size: int = 500):
    """
    Fetch page content and split into chunks of roughly `chunk_size` words.
    """
    page = wikipedia.page(title)
    words = page.content.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks
