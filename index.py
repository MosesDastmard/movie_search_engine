#%%
import index_utils
import pandas as pd
import pickle
#%%
movies_df = pd.read_csv('movie_data.csv')
# initiate the search engine class
se = index_utils.search_engine()
# train the search engine (make index)
se.create_engine(movies_df)
# Store the results (trained search engine) on hard disk
pickle.dump(se , open( "se.p", "wb" ) )
