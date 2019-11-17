import codecs
from bs4 import BeautifulSoup

# The following function takes as input the htmls file path and returns in output a dictionary storing all the information derived from parsing
# the pages.

def info_extractor(file_path):
    # make a template to store the data caught from html
    movie_info = {}
    infobox_temp = infobox_scheme()
    for i in range(len(infobox_temp)):
        movie_info[infobox_temp[i]] = None
    # read the html in Beaitiful Soup format
    f = codecs.open(file_path, 'r', 'utf-8')
    document = BeautifulSoup(f.read(), 'lxml')
    f.close()
    # Extracting the URL of the movie
    movie_info['Url'] = document.find('link', {'rel': 'canonical'})['href']
    # Check the html file has an infobox
    if not hasattr(document.find('table', {'class': "infobox vevent"}),'tbody'):
        return False
    # make an iterator to extract the Plot and Intro since they stored on <p>-like xml format
    # the paragraphs related to Plot and Intro trapped between two <h2>-like xml
    doc_iter = document.find_all('div', {'class': "mw-parser-output"})[0].children
    info = True
    intro = ""
    plot  = ""
    # Extracting the text of the <p> since we see the first <h2> and storing as Intro
    while info:
        try:
            t = next(doc_iter)
        except:
            info = False
            break
        if t.name == None:
            continue
        if t.name == 'p':
            intro += t.text
            continue
        if t.name == 'h2':
            break
    # Extracting the text of the <p> from the first <h2> till the second <h2> and storing as Plot
    while info:
        try:
            t = next(doc_iter)
        except:
            info = False
            break
        if t.name == None:
            continue
        if t.name == 'p':
            plot += t.text
            continue
        if t.name == 'h2':
            break
    
    movie_info['Intro'] = intro
    movie_info['Plot'] =  plot
    
    # Find the parent for infobox
    info_box = document.find('table', {'class': "infobox vevent"}).tbody
    
    # Update movie_info ditionary based on keys that are found in the infobox 
    for row in info_box.find_all('th'):
        row_text = row.text.strip()
        sibling = row.nextSibling
        if sibling is not None:
            if row_text in movie_info.keys():
                sib_info = sibling.text.strip().split('\n')
                if len(sib_info) == 1:
                    sib_info = sib_info[0]
                movie_info[row_text] = sib_info
            else:
                return False
        else:
            movie_info['Title'] = row_text
    return movie_info

# This other function defines a scheme used in the previous one to create the dictionary.

def infobox_scheme():
    return ['Intro', 'Plot', 'Title', 'Directed by', 'Produced by', 'Written by', 'Screenplay by', 'Story by',
            'Based on', 'Starring', 'Narrated by', 'Music by', 'Cinematography', 'Edited by', 'Productioncompany', 'Distributed by',
            'Release date', 'Running time', 'Country', 'Language', 'Budget', 'Box office', 'Url']