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
        if not os.path.exists('cache'):
            with open('cache/index.pkl', 'wb') as f:
               pickle.dump(self.docmap, f)