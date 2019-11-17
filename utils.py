import nltk
nltk.download('stopwords')
nltk.download('punkt')

import string
import numpy as np
from numpy.linalg import norm
from nltk.corpus import stopwords 
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from scipy.spatial.distance import cosine
from nltk.tokenize import wordpunct_tokenize


# Loading the stopwords from nltk

stop_words = set(stopwords.words('english'))
# Adding the punctautions to stopword list
stop_words.update(set(string.punctuation))
# Adding some wierd symbols
stop_words.update(["''","``","'s"])

stemmer = PorterStemmer()

# This function takes as input a generic text and parses it in order to get its stemmed version.

def text_cleaner(text):
    if not type(text) is str:
        return []
    else:
        # Two tokenizers appleid to the text, wordpunct_tokenize and word_tokenize
        words = wordpunct_tokenize(text)
        text = " ".join(words)
        words = word_tokenize(text)
        #words = word_tokenize(text)
        filtered_words = [w.lower() for w in words if w.lower() not in stop_words]
        stemmed_words = [stemmer.stem(word) for word in filtered_words]
        if type(stemmed_words) is str:
            stemmed_words = [stemmed_words]
        return stemmed_words

# With the following two functions we compute the cosine similarity in search engine #2 and #3.

def cosine_similarity_se2(row):
    query_val = np.ones(shape=(1, len(row)))
    return 1-cosine(row, query_val)*norm(row) # we also take into account the norm in order to increase the score related 
                                              # to documents with higher word frequency

# The function generates a function with a static parameter of the word
# The generated function checks whether the word is a substring of the input                                             
def word_check(x, word):
    def z(x):
        x = str(x)
        return word in ' '.join(text_cleaner(x))
    return z