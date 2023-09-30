import re
import advertools as adv

STOPLIST = adv.stopwords['polish']

class Searchterm:
    def __init__(self, query):
        self.text = self.get_searchterm(query)

    def get_searchterm(self, query):
        pipeline = [
            self.lower,
            self.clean_text,
            self.filter_stopwords
        ]
        out = query
        for f in pipeline:
            out = f(out)
        return out

    def lower(self, text):
        return text.lower()

    def clean_text(self, text):
        return re.sub(r'[^a-z0-9ąęłńóśćźż ]+', '', text)
    
    def filter_stopwords(self, text):
        return ' '.join([word for word in text.split() if word not in STOPLIST])
