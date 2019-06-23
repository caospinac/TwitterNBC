from math import sqrt
import re
from string import punctuation

from nltk.corpus import stopwords

from web.core import db


class NaiveBayesClassifier(object):

    def __init__(self, values: list=("pos", "neg")):
        self.__stopwords = set(
            stopwords.words("english") +
            list(punctuation) +
            ["{mention}", "{link}"]
        )

        self.values = set(values)

    def classify_naive_bayes_text(self, doc: str):
        if not doc:
            print("Error: The document is not valid.")
            return

        P = self.__get_word("_")
        for key in [k for k in P.keys()]:
            if key not in self.values:
                del P[key]

        for w in filter(self.__in_vocabulary, self.get_document_words(doc)):
            for vj in self.values:
                P[vj] *= self.__get_word(w)[vj]


        total_factor = sum(v for k, v in P.items() if k in self.values)
        for vj in self.values:
            P[vj] = P[vj] / total_factor

        return {'document': doc, **P, 'trend': max(P, key=P.get)}

    def __in_vocabulary(self, word: str):
        return self.__get_word(word) is not None

    def __get_word(self, value):
        return db.words.find_one({'value': value})

    def get_vocabulary(self):
        return db.words.distinct('value', {'value':{'$ne':"_"}})

    def get_document_words(self, text: str) -> list:
        text = text.lower()
        text = re.sub(r"((www\.[^\s]+)|(https?://[^\s]+))", "{link}", text)
        text = re.sub(r"@[^\s]+", "{mention}", text)
        text = re.sub(r"#([^\s]+)", r"\1", text)
        words = re.findall(r"[^\d\W_]{2,}", text)
        words = filter(lambda w: w not in self.__stopwords, words)
        words = list(words)
        return words
