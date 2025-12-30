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
    
    
def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    stopwords = load_stopwords()
    
    # Load the index from disk
    index = InvertedIndex()
    try:
        index.load()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run 'build' command first to create the index.")
        return []
    
    # Preprocess and tokenize the query
    preprocessed_query = tokenize_text(preprocess_text(query))
    
    # Remove stopwords
    query_tokens = [token for token in preprocessed_query if token not in stopwords]
    
    # Collect matching documents
    results = []
    seen_doc_ids = set()  # To avoid duplicates
    
    # Iterate over each token in the query
    for token in query_tokens:
        # Get document IDs that contain this token
        doc_ids = index.get_documents(token)
        
        # Add each matching document to results
        for doc_id in doc_ids:
            if doc_id not in seen_doc_ids:
                # Get the full document from docmap
                document = index.docmap[doc_id]
                results.append(document)
                seen_doc_ids.add(doc_id)
                
                # Print the result
                print(f"ID: {doc_id}, Title: {document['title']}")
                
                # Stop if we have enough results
                if len(results) >= limit:
                    break
        
        # Break outer loop if we have enough results
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