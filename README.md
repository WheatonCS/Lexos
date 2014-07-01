# Lexos
# Summary
Lexos is an integrated workflow of tools to facilitate the computational analyses of texts, presented in a web-based interface. Functionality provided includes the ability to "scrub" texts (remove punctuation, lemmatize, consolidate characters, remove stopwords, etc), cut or segment texts, and a suite of options for analysis and visualizations, including creating and downloading Document Term Matrices (DTM) of token counts (both word- and character-ngrams or tf-idf); cluster analysis (hierarchical or k-means, with silhouette scores); rolling-window analyses of substring, word, or regex-pattern occurrances; bubble visualizations (of term frequencies); and word clouds (of term frequencies or 
[MALLET](http://mallet.cs.umass.edu/)-produced topic modelling results). More functionality is being added on an ongoing basis.


## System Architecture (in brief)
Lexos is written primarily in Python 2.7.3 using the 
[Flask](http://flask.pocoo.org/) microframework, based on Werkzeug and Jinja 2. 
A heavy dose of Javascript and CSS is included on the front-end. We increasingly incorporate the wiz from 
[D3.js](http://d3js.org/) in our visualizations and the power in the 
[scilearn-kit](http://scikit-learn.org/stable/) modules for text and statistical processing. 
The INSTALLME file provides directions for setting up the development environment for testing (using localhost:5000) on your local machine.

## Dependencies
chardet, flask, gensim, matplotlib, numpy, pip, scikit-learn, scipy

The PDF Viewer extension needs to be enabled in the Chrome browser on MacOS. 

## License information
See the file LICENSE for information on the
terms & conditions for usage and a DISCLAIMER OF ALL WARRANTIES.
