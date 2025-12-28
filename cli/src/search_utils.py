import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
MOVIE_PATH = PROJECT_ROOT / "data" / "movies.json"
STOPWORD_PATH = PROJECT_ROOT / "data" / "stopwords.txt"

DEFAULT_SEARCH_LIMIT = 5

def load_movies() -> list[dict]:
    with open(MOVIE_PATH, "r") as f:
        data = json.load(f)
    return data["movies"]

def load_stopwords():
    print(f"DEBUG: Looking for file at: {STOPWORD_PATH}")
    
    p = Path(STOPWORD_PATH)
    print(f"DEBUG: File exists: {p.exists()}")
    print(f"DEBUG: File size: {p.stat().st_size} bytes")

    
    with open(STOPWORD_PATH, 'r') as f:
        stop_words = f.readlines()
        print(f"DEBUG: Read {len(stop_words)} lines")
        print(f"DEBUG: First few lines: {stop_words[:3]}")
        
        cleaned_list_of_stopwords = []
        for word in stop_words:
            cleaned_list_of_stopwords.append(word.strip().lower())
        
        print(f"DEBUG: After cleaning: {cleaned_list_of_stopwords[:3]}")
    return cleaned_list_of_stopwords
