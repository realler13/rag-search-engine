import string
from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies, load_stopwords


def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    stopwords = load_stopwords()
    results = []
    preprocessed_query = tokenize_text(preprocess_text(query))
    for token in preprocessed_query[:]:
        if token in stopwords:
            preprocessed_query.remove(token)

    for movie in movies:
        preprocessed_title = tokenize_text(preprocess_text(movie['title']))
        for title_word in preprocessed_title[:]:  # Copy with [:]
            if title_word in stopwords:
                preprocessed_title.remove(title_word)
        
        
        for token in preprocessed_query:
            for title in preprocessed_title:
                if token in title:
                    results.append(movie)
                    break
            else:
                continue
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