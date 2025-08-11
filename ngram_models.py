import math
from collections import defaultdict

class NGramModels:
    def __init__(self, corpus):
        self.corpus = corpus
        self.unigrams = defaultdict(int)
        self.bigrams = defaultdict(int)
        self.trigrams = defaultdict(int)
        self.vocab = set()
        self.build_ngram_models()

    def build_ngram_models(self):
        """Build n-gram counts from corpus"""
        for sentence in self.corpus:
            tokens = ['<s>'] + sentence.split() + ['</s>']
          
            self.vocab.update(tokens)
            # Unigrams
            for token in tokens:
                self.unigrams[token] += 1
            # Bigrams
            for i in range(len(tokens)-1):
                self.bigrams[(tokens[i], tokens[i+1])] += 1
            # Trigrams
            for i in range(len(tokens)-2):
                self.trigrams[(tokens[i], tokens[i+1], tokens[i+2])] += 1

    def calculate_probability(self, context, word):
        """Calculate probability using Markov assumption and MLE"""
        if len(context) == 2:  # Trigram
            count = self.trigrams.get((context[0], context[1], word), 0) + 1
            denominator = self.bigrams.get((context[0], context[1]), 0) + len(self.vocab)
            return count / denominator if denominator else 0
        elif len(context) == 1:  # Bigram
            count = self.bigrams.get((context[0], word), 0) + 1
            denominator = self.unigrams.get(context[0], 0) + len(self.vocab)
            return count / denominator if denominator else 0
        else:  # Unigram
            return (self.unigrams.get(word, 0) / sum(self.unigrams.values()))

    def log_probability(self, context, word):
        """Log probability to avoid underflow"""
        prob = self.calculate_probability(context, word)
        return math.log(prob) if prob > 0 else float('-inf')