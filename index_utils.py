import utils
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from tqdm import tqdm
import numpy as np
import pandas as pd
from itertools import combinations, permutations
import heapq

# Here we created a class in order to store the index of a search engine

class index:
    def __init__(self, name):
        self.name = name
        self.index = dict()
        
# The following class contains methods used to create the search engine itself    
        
class search_engine:
    def __init__(self, name = 'movie search engine'):
        self.name = name
        self.trained = False
        self.vocabulary = dict()
        self.search_engines = [index(name = 'Search Engine ' + str(i)) for i in range(1,3)]
        self.vectorizer = CountVectorizer(tokenizer = utils.text_cleaner)
        self.transformer = TfidfTransformer(smooth_idf=False)
        
    # This method takes as input a dataframe containing the information about the movies obtained by parsing the html files.
    # The returned output is the index for each search engine. 

    def create_engine(self, dataframe):
        # storing the itro and plot in a list for search engine 1 & 2
        words_list = []
        for i in tqdm(range(len(dataframe))):
            words_list.append(str(dataframe.loc[i]['Plot']) + ' ' + str(dataframe.loc[i]['Intro']))
        print('word list is made')
    
        print('word frequency is running...')  
        # computing the word frequency for each document
        words_freq = self.vectorizer.fit_transform(words_list)
        words_freq = words_freq.toarray()
        corpus_words = self.vectorizer.get_feature_names()
        print('index initiating...')
        # creating the vocabulary and initiating the index
        
        for i,word in enumerate(corpus_words):
            self.vocabulary[word] = i
            self.search_engines[0].index[i]=set()
            self.search_engines[1].index[i]=set()
        # updating the index for search engine 1
        # keep a list of documents IDs
        docs_id = np.array(range(words_freq.shape[0]))
        # Pick the column of the work frequency related to each term. The positive values means the term appears in the document
        for j in tqdm(range(words_freq.shape[1])):
            term_freq = words_freq[:,j] > 0
            doc_id = docs_id[term_freq]
            # Updating the index related to each term for documents ID that contains the term
            for i in range(doc_id.shape[0]):
                self.search_engines[0].index[j].update({doc_id[i]})
        # updating the index for search engines 2
        # transforming the word frequency to tf-idf score
        tfidf = self.transformer.fit_transform(words_freq)
        tfidf = tfidf.toarray()
        # Pick the column of the tf-idf related to each term. The positive values means the term appears in the document
        for j in tqdm(range(words_freq.shape[1])):
            term_freq = words_freq[:,j] > 0
            term_tfidf = tfidf[term_freq,j]
            doc_id = docs_id[term_freq]
            # Updating the index (doc_id, tfidf) related to each term for documents ID that contains the term
            for i in range(term_tfidf.shape[0]):
                self.search_engines[1].index[j].update({(doc_id[i],term_tfidf[i])})
        # set the search engine to trained in order to avoid retraning and check the posibility of fetching query
        self.trained = True
    
    # The method below takes as input the search engine ID, a query and the dataframe and returns in output the results yielded by running the search engine.
    # Provide suggestion to the user to enhance the query 
    def query(self, search_engine, q, dataframe):
        # check whether the engine is trained or not 
        if self.trained:
            # parsing the query into text_cleaner in order to match the words (tokenized and stemmed) we have for making index 
            query_words = utils.text_cleaner(q)
            if search_engine == 1:
                # check if the whole terms appear in document and output the result for 'Title', 'Intro' and 'URL'
                return pd.DataFrame([dataframe.loc[j][['Title','Intro','Url']] 
                    for j in set.intersection(*[self.search_engines[search_engine -1].index[i] 
                    for i in [self.vocabulary[t] 
                    for t in query_words if t in self.vocabulary.keys()]])])
            if search_engine in [2, 3]:
                # pick the document that at least one of the word in the query appears in
                doc_ids = [self.search_engines[1].index[t] for t in [self.vocabulary[w] for w in query_words if w in self.vocabulary.keys()]]
                mat = []
                for v in doc_ids:
                    d = dict()
                    for i in v:
                        d[i[0]]=i[1]
                    mat.append(d)
                # make a pandas dataframe (matrix) which element is a tfidf of the term (column) in the document (row)
                Results = pd.DataFrame(mat).transpose()
                # Fill zero for those terms with NaN tfidf (when the term doesn't appear in the document)
                Results.fillna(0, inplace = True)
                # Drop the rows that do not satisfy the conjunctive query 
                Results = Results.loc[[all(Results.loc[i] > 0) for i in Results.index]]
                # computing the cosine similarity for search engine 2
                Results['Score'] = Results.apply(utils.cosine_similarity_se2, axis = 1)
                Results['Doc_ID'] = Results.index
                # store the result in tuple like (value, key) in order to heapify the output
                hp = [(Results.loc[row]['Score'], Results.loc[row]['Doc_ID']) for row in Results.index]
                heapq.heapify(hp)
                # Output the result of the first top-50 scores
                hp_res = heapq.nlargest(50, hp)
                # output 'Title', 'Intro' and 'URL' for top-50
                Results = pd.DataFrame([dataframe.loc[j][['Title','Intro','Url']] for j in [a[1] for a in hp_res]])
                Results['Score'] = [a[0] for a in hp_res]
                # search engine 3
                if search_engine == 3:
                    # create a list of all possible combinations of the words in the query
                    word_combinations = list()                    
                    for i in range(len(query_words)):
                        for j in combinations(query_words,i+1):
                            for h in permutations(j):
                                word_combinations.append(' '.join(h))
                
                    
                    # pick the whole information of the movies stem from search engine 2 query
                    docs = dataframe.loc[Results.index]
                    # check if the words combination appears in the dataframe (not only Plot and Intro but also whole columns) 
                    results_dic = dict()
                    for word in word_combinations:
                        word_checker = utils.word_check(x='make_function',word=word)    
                        results_dic[word] = docs.applymap(word_checker)
                    possible_questions = list()
                    # check the frequency of the words combinations
                    for word,df in results_dic.items():
                        r_df = df.sum()
                        for col_name in r_df.keys():
                            if r_df[col_name] > 0 and not col_name in ['Intro','Plot']:
                                possible_questions.append((r_df[col_name],len(word),word,col_name))
                    # make a list of possible candidates for asking the question
                    if len(possible_questions) > 0:
                        questions_df = pd.DataFrame(possible_questions, columns = ['frequency','length','word','col_name'])
                        questions_df['Score'] = questions_df['frequency']*.7 + questions_df['length']*.3
                        questions_df = questions_df.sort_values(by='Score',ascending=False).reset_index(drop=True)
                        print(questions_df)
                        # pick the most likely question
                        question = questions_df.loc[0]
                        while True:
                            answer = input('do you mean ' + question['col_name'] + ': ' + question['word'] + '? Y/n:')
                            if answer.lower() in ['y','n']:
                                break

                        if answer.lower() == 'y':    
                            Results['Score'] = Results['Score'] + 0.02*results_dic[question['word']][question['col_name']]*Results['Score']
                            hp = [(Results.loc[row]['Score'], row) for row in Results.index]
                            heapq.heapify(hp)
                            # Output the result of the first top-10 scores
                            hp_res = heapq.nlargest(50, hp)
                            # output 'Title', 'Intro' and 'URL' for top-10
                            Results = pd.DataFrame([dataframe.loc[j][['Title','Intro','Url']] for j in [a[1] for a in hp_res]])
                            Results['Score'] = [a[0] for a in hp_res]
                return Results
                     
                            
        else:
            print('search engine is not trained')            

        