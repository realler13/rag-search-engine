import string
from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies, load_stopwords
from nltk.stem import PorterStemmer
import os
import pickle

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
    
    # Stem each query token
    stemmed_query_tokens = [stemmer.stem(token) for token in query_tokens]
    
    # DEBUG: Print what we're searching for
    print(f"DEBUG: Query tokens after preprocessing: {query_tokens}")
    print(f"DEBUG: Stemmed query tokens: {stemmed_query_tokens}")
    
    # Count how many query terms each document matches
    doc_match_count = {}
    
    for token in stemmed_query_tokens:
        doc_ids = index.get_documents(token)
        print(f"DEBUG: Token '{token}' found in {len(doc_ids)} documents")
        
        for doc_id in doc_ids:
            doc_match_count[doc_id] = doc_match_count.get(doc_id, 0) + 1
    
    # Sort by match count (descending), then by ID (ascending)
    sorted_docs = sorted(doc_match_count.items(), 
                        key=lambda x: (-x[1], x[0]))
    
    # Take top 'limit' results
    top_doc_ids = [doc_id for doc_id, _ in sorted_docs[:limit]]
    
    # Build results list
    results = []
    for doc_id in top_doc_ids:
        document = index.docmap[doc_id]
        match_count = doc_match_count[doc_id]
        results.append(document)
        print(f"ID: {doc_id}, Title: {document['title']} (matched {match_count} terms)")
    
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

class InvertedIndex:
    def __init__(self):
       self.index =  {}
       self.docmap = {}
       self.term_frequencies = {}
       
    def __add_document(self, doc_id, text):
        preprocessed = preprocess_text(text)
        tokens = preprocessed.split()
        
        for token in tokens:
            # STEM THE TOKEN DURING INDEXING!
            stemmed_token = stemmer.stem(token)
            
            if stemmed_token not in self.index: # type: ignore
                self.index[stemmed_token] = set()
            self.index[stemmed_token].add(doc_id)
       
    def get_documents(self, term):
        term = term.lower()
        doc_ids = self.index.get(term, set())
        return sorted(list(doc_ids))
    
    def build(self, movies):
        for movie in movies:
            doc_id = movie['id']
            self.docmap[doc_id] = movie
            text = f"{movie['title']} {movie['description']}"
            self.__add_document(doc_id, text)

    def save(self):
        cache_dir = 'cache'      
        os.makedirs(cache_dir, exist_ok=True)
        index_path = os.path.join(cache_dir, 'index.pkl')
        with open(index_path, 'wb') as f:
            pickle.dump(self.index, f)
        
        
        docmap_path = os.path.join(cache_dir, 'docmap.pkl')
        with open(docmap_path, 'wb') as f:
            pickle.dump(self.docmap, f)
        
        print(f"Index saved to {index_path}")
        print(f"Docmap saved to {docmap_path}")

    def load(self):
        cache_dir = 'cache'
        index_path = os.path.join(cache_dir, 'index.pkl')
        docmap_path = os.path.join(cache_dir, 'docmap.pkl')
         
        if not os.path.exists(index_path):
           raise FileNotFoundError(f"Index file not found: {index_path}")
    
        if not os.path.exists(docmap_path):
            raise FileNotFoundError(f"Docmap file not found: {docmap_path}")

        with open(index_path, 'rb') as f:
            self.index = pickle.load(f)
        
        with open(docmap_path, 'rb') as f:
            self.docmap = pickle.load(f)

        print(f"Loaded index with {len(self.index)} tokens")
        print(f"Loaded docmap with {len(self.docmap)} documents")

