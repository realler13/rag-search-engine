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