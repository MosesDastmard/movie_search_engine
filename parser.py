import parser_utils
import os
from tqdm import tqdm
import pandas as pd
ls = ['Htmls/' + file for file in os.listdir('Htmls') if file[-4:] == 'html']
ls.sort(key = lambda x: int(''.join(filter(str.isdigit, x))))

#%%
movie_data = list()
fails = 0

try:
    os.makedirs('Tsv')
except:
    _ = None

for i in tqdm(range(len(ls))):
    path_file = ls[i]
    movie_info = parser_utils.info_extractor(path_file)
    if movie_info != False:
        movie_data.append(movie_info)
        #pd.DataFrame(list(movie_info.values())).to_csv(r'Tsv\Article_' + str(i + 1) + '.tsv', sep='\t', header = False, index = False)
    else:
        fails += 1
        #print(ls[i])

print(str(fails) + ' files are not Wikipedia movie pages')
movies_info_df = pd.DataFrame(movie_data)
movies_info_df['Doc_ID'] = movies_info_df.index
movies_info_df.to_csv('movie_data.csv')
movies_info_df = pd.read_csv('movie_data.csv')