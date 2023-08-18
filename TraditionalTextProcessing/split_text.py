import re
from snownlp import SnowNLP

class TraditionalTextProcessing:
    def __init__(self, text):
        self._text = text
        self._nlp = SnowNLP(text)
        self._sentences = self._nlp.sentences
        self._words = []
        for s in self._sentences:
            self._words.append(SnowNLP(s).words)

    def sentences(self):
        return self._sentences

    def sentences_index(self, index):
        if index < 0 or index >= len(self._sentences):
            raise ValueError("index out of range")
        return self._sentences[index]

    def words(self, index):
        if index < 0 or index >= len(self._words):
            raise ValueError("index out of range")
        return self._words[index]

    def lang(self):
        return self._lang



