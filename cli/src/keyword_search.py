import string
from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies


def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    results = []
    preprocessed_query = tokenize_text(preprocess_text(query))

    for movie in movies:
        preprocessed_title = tokenize_text(preprocess_text(movie['title']))
        for token in preprocessed_query:
            for title in preprocessed_title:
                if token in title:
                    results.append(movie)
                    break
        if len(results) >= limit:
            break
    return results

def preprocess_text(text):
    text = text.lower()
    translation_table = str.maketrans("", "", string.punctuation)
    text = text.translate(translation_table)
    return text

def tokenize_text(text):
    tokens = list(text.split())
    for token in tokens:
        if token == string.whitespace:
            tokens.remove(token)
    return tokens