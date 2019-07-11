from math import sqrt
import csv
import os
import re
from string import punctuation

from itertools import chain
from nltk.corpus import stopwords
from nltk.stem import (LancasterStemmer, PorterStemmer, SnowballStemmer,
                       WordNetLemmatizer)

from db import db


class NaiveBayesClassifier(object):

    def __init__(self, training_data: list, values: list):
        self.__porter = PorterStemmer()
        self.__lancaster = LancasterStemmer()
        self.__snowball = SnowballStemmer("english")
        self.__lemmatizer = WordNetLemmatizer()
        self.__stopwords = set(
            stopwords.words("english") +
            list(punctuation) +
            ["{mention}", "{link}"]
        )

        self.training_data = {}
        self.values = set(values)
        self.stemmer: callable=lambda x: x
        self.P = {'_': dict.fromkeys(self.values)}
        self.__build_training_data(training_data)

    def __build_training_data(self, data):
        for vj in self.values:
            filtered_data = filter(lambda x: x[0] == vj, data)
            self.training_data[vj] = list(map(lambda x: x[1], filtered_data))

        self.all_training_data = list(chain(*self.training_data.values()))

    def train(self, stem_method: str=None, training_data: list=None):
        if isinstance(training_data, list):
            self.__build_training_data(training_data)

        self.__set_stemmer(stem_method)
        self.vocabulary = self.__get_vocabulary()
        self.P.update(dict((w, {}) for w in self.vocabulary))
        for vj in self.values:
            docs_j = self.training_data[vj]
            self.P['_'][vj] = len(docs_j) / len(self.all_training_data)
            all_text_j: str = " ".join(docs_j)
            words_j: list = self.__get_document_words(all_text_j)
            n = len(words_j)
            for w in self.vocabulary:
                w_occurrences = words_j.count(w)
                self.P[w][vj] = sqrt(
                    (w_occurrences + 1) / (n + len(self.vocabulary))
                )

        self.__trained = True

    def __get_vocabulary(self):
        words = self.__get_document_words(" ".join(self.all_training_data))
        words = list(set(words))
        return words

    def __get_document_words(self, text: str) -> list:
        text = text.lower()
        text = re.sub(r"((www\.[^\s]+)|(https?://[^\s]+))", "{link}", text)
        text = re.sub(r"@[^\s]+", "{mention}", text)
        text = re.sub(r"#([^\s]+)", r"\1", text)
        words = re.findall(r"([^\d\W_]{2,}|\{(mention|link)\})", text)
        words = filter(lambda w: w not in self.__stopwords, words)
        words = map(self.stemmer, words)
        words = list(words)
        return words

    def __set_stemmer(self, name="default"):
        self.stem_method = name
        if name == "porter":
            self.stemmer = self.__porter.stem
        elif name == "lancaster":
            self.stemmer = self.__lancaster.stem
        elif name == "snowball":
            self.stemmer = self.__snowball.stem
        elif name == "lemmatizer":
            self.stemmer = lambda w: self.__lemmatizer.lemmatize(w, pos="v")
        else:
            self.stemmer: callable=lambda x: x


def main():
    def path(filename: str) -> str:
        return os.path.join(
            os.path.join(os.path.abspath(""), "learning_data"),
            filename
        )

    data = []
    values = {"neg", "pos"}
    with open(path("join.csv"), "rt", encoding="utf-8-sig") as data_file:
        data_file.readline()
        reader = csv.reader(data_file)
        for row in reader:
            if row[0] in values:
                data.append(row)

    print(len(data), "records...")
    classifiers = [
        "default",
        # "lancaster",
        # "lemmatizer",
        # "porter",
        # "snowball"
    ]
    for classifier_name in classifiers:
        print(classifier_name, "...")
        classifier = NaiveBayesClassifier(training_data=data, values=values)
        classifier.train(classifier_name)
        for word, p in classifier.P.items():
            total_factor = sum(v for k, v in p.items() if k in values)
            factors = {}
            for vj in values:
                factors[vj] = p[vj] / total_factor

            db.words.insert_one({
                'classifier': classifier_name,
                'value': word,
                **factors
            })

    print(".")


if __name__ == "__main__":
    main()
