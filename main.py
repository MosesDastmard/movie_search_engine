import pickle
import pandas as pd
se = pickle.load(open( "se.p", "rb" ))
movie_df = pd.read_csv('movie_data.csv')
#%%
while True:
    search_engine = input('Select the search engine: ')
    if search_engine == '':
        break
    elif not search_engine.isnumeric():
        print('It should be a number in range 1 to 3')
        continue
    elif  int(search_engine) > 3:
        print('It should be a number in range 1 to 3')
        continue
    search_engine = int(search_engine)
    while True:
        query = input('What your looking for? ')
        print(query)
        if query == '':
            break
        if search_engine == 1:
            print(se.query(search_engine = 1, q = query, dataframe = movie_df))
        if search_engine == 2:
            print(se.query(search_engine = 2, q = query, dataframe = movie_df))
        if search_engine == 3:
            print(se.query(search_engine = 3, q = query, dataframe = movie_df))
#%%
query = 'disney movie 2019'
x = se.query(search_engine = 2, q = query, dataframe = movie_df)