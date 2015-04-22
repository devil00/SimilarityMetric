import re
import math
import os
from stemming import porter


splitter = re.compile(r"[a-z\-']+", re.I)
stemmer = porter
POEM_THRESHOLD = 0.13


def _get_stop_words():
    with open("stop_words.txt", "r") as f:
        stop_words = [w.strip().lower() for w in f.readlines() 
                      if len(w) > 1]
    return stop_words


class PoemSimilarity(object):
    def __init__(self, source_doc, list_docs):
        self.source_doc = source_doc
        self.list_docs = list_docs
        self.stop_words = _get_stop_words()

    def find_similar_poems(self):
        '''
        Compare the source doc with the list of docs and store the similarity 
        metric in `similarity_doc_map`.
        '''
        similarity_doc_map = {}
        # Read all the docs 
        list_docs = [self.read_doc(doc) for doc in self.list_docs]
        # Read source doc
        source_doc = self.read_doc(self.source_doc)
        # Generate tokens for a source doc.
        source_doc_tokens = self.tokenize(source_doc)
        for j, doc in enumerate(list_docs):
            word_dict = {}
            # Generate tokens.
            doc_tokens = self.tokenize(doc)
            # Gather all the tokens to generate a keyword index map.
            list_words = source_doc_tokens + doc_tokens
            self.add_words_to_dict(list_words, word_dict)
            dict_word_idx = {}
            dict_word_keys = word_dict.keys()
            for i in xrange(len(dict_word_keys)):
                dict_word_idx[dict_word_keys[i]] = (
                    i, word_dict[dict_word_keys[i]])
            del dict_word_keys
            del word_dict
            # Make vectors corresponding to every doc.
            vec1 = self.make_vector(source_doc, dict_word_idx)
            vec2 = self.make_vector(doc, dict_word_idx)
            similarity_metric = self.get_cosine_similarity(vec1, vec2)
            similarity_doc_map[j] = similarity_metric
        # Filter and get all the similar docs whose similarity metric reaches
        # to a fixed threshold.
#        print similarity_doc_map
        possible_similar_poems_indices = map(
            lambda lp: lp[0],
            filter(lambda l: l[1] > POEM_THRESHOLD,
                   similarity_doc_map.items()))
        return [self.list_docs[pi] for pi in possible_similar_poems_indices]

    def read_doc(self, doc_name):
        try:
            with open(doc_name, "rb") as f:
                doc = f.read()
        except IOError:
            return ""
        return doc

    def add_words_to_dict(self, list_words, word_dict):
        for word in list_words:
            word = word.lower()
            if word not in self.stop_words:
                ws = stemmer.stem(word)
                word_dict.setdefault(ws, 0)
                word_dict[ws] += 1
            
    def tokenize(self, doc):
        return splitter.findall(doc)

    def make_vector(self, doc, keyword_idx):
        '''
        Represent a string doc to a vector.
        :param doc: content of document.
        :type doc: str
        :param keyword_idx: Mapping containing index of word in bag of 
                            words for a given doc.
        :type keyword_idx: dict
        '''
        vector = [0.0]*len(keyword_idx.keys())
        doc_tokens = self.tokenize(doc)
        for word in doc_tokens:
            key_data = keyword_idx.get(stemmer.stem(word).lower(), None)
            if key_data:
                vector[key_data[0]] += 1
        return vector

    def get_cosine_similarity(self, vec1, vec2):
        '''
        Perform the cosine similarity to find the similr docs.
        :param vec1: Vector representation of doc1.
        :type vec1: list or array
        :param vec2: Vector representation of doc2
        :type vec2: list
        :return: similarity metric.
        '''
        assert len(vec1) == len(vec2)
        numerator = sum([vec1[x] * vec2[x] for x in range(len(vec1))])
        sum1 = sum([x**2 for x in vec1])
        sum2 = sum([x**2 for x in vec2])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator


if __name__ == "__main__":
    poems_file = os.listdir("./poem")
    poems_file.remove("1")
    source = "./poem/1"
    list_poems = ["./poem/{}".format(p) for p in poems_file]
    ps = PoemSimilarity(source, list_poems)
    print "Possible similar poems to poem 1 are : "
    print ps.find_similar_poems()

