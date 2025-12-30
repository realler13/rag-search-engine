import os
import pickle

class InvertedIndex:
    def __init__(self):
       self.index =  {}
       self.docmap = {}
    def __add_document(self, doc_id, text):
        tokens = text.lower().split()
        for token in tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)
       
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