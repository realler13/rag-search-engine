import string
from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies, load_stopwords
from nltk.stem import PorterStemmer
from src.inverted_index import InvertedIndex

stemmer = PorterStemmer()

def build_command():
    movies = load_movies()  # However you load your movie data
    
    index = InvertedIndex()
    index.build(movies)
    index.save()
    
    # Get the first document for 'merida' and print it
    docs = index.get_documents('merida')
    print(f"First document for token 'merida' = {docs[0]}")

def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    stopwords = load_stopwords()
    results = []
    preprocessed_query = tokenize_text(preprocess_text(query))
    for token in preprocessed_query[:]:
        if token in stopwords:
            preprocessed_query.remove(token)
    stem_tokens = []
    for token in preprocessed_query:
        token = stemmer.stem(token)
        stem_tokens.append(token)    

    for movie in movies:
        preprocessed_title = tokenize_text(preprocess_text(movie['title']))
        for title_word in preprocessed_title[:]:  # Copy with [:]
            if title_word in stopwords:
                preprocessed_title.remove(title_word)
        stem_title_words = []
        for title_word in preprocessed_title:
            title_word = stemmer.stem(title_word)
            stem_title_words.append(title_word)
                                    
        
        for token in stem_tokens:
            for title in stem_title_words:
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