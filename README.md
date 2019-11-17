# Homework 3 - What movie to watch tonight?

<p align="center">
<img src="https://www.lifewire.com/thmb/5EJ5OHxtAhaf5IEYXENLVj3Dg-M=/768x0/filters:no_upscale():max_bytes(150000):strip_icc()/itunes-movie-rental-rules-570a5c903df78c7d9edb7593.jpg">
</p>

Goals of this assignment were: scraping various Wikipedia movie pages and building up three different search engines which, taking a query  as input, return a list of results that match the latter. 

__`Usage instructions (should you want to execute our code):`__

	1. Run the collector.py file which will collect the movie pages and store them as html files.
 	2. Run the parser.py file which will preprocess the html files and extract the information needed by 
       the search engines.
 	3. Run the index.py file which will produce the vocabulary, the index and initialize every search engine and make 
       it ready to use.
 	4. Finally run the main.py file an query the data.
 
 
The repository includes the following files:
1. __`main.ipynb`__: 
     > A Jupyter notebook which provides an overview of every single step of which the process to solve implement the code has                     consisted in.
			
2. __`collector.py`__:
      > A python file which contains the code needed to collect our data from the html page provided by the TAs and Wikipedia. 

3. __`collector_utils.py`__:
      > A Python file which stores the functions we used in collector.py. 
      
4. __`parser.py`__:
      > A Python file containing the code needed to parse the entire collection of html pages and store them as tsv files.
      
5. __`parser_utils.py`__:
      > A Python file gathering the functions used in parser.py. 
      
6. __`index.py`__:
      > A Python file which, once executed, generates the indices, the vocabulary and intializes the Search engines.
      
7. __`index_utils.py`__:
      > A Python file containing the functions used in index.py.
      
8. __`utils.py`__:
      > A Python file gathering functions we needed in more than one of the previous files.
      
9. __`main.py`__:
      > A Python file that, once executed, allows the user to interact with the search engine. When the user runs the file it will be             able to choose:
          the search_engine: a parameter that the user set to choose the search engine to run (1,2 or 3).

9. __`exercise_4.py`__:
      > A Python file that contains the implementation of the algorithm that solves problem 4.

__`Team members:  Mousaalreza Dastmard - Giorgio Maria Mandolini`__
