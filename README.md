# Lexos

# Summary
Lexos is an integrated workflow of tools to facilitate the computational analyses of texts, presented in a web-based interface. Functionality provided includes the ability to "scrub" documents (handle punctuation, lemmatize, consolidate characters, remove stopwords, etc), cut or segment documents, and a suite of options for analysis and visualizations, including creating and downloading Document Term Matrices (DTM) of token counts (both word- and character-ngrams); cluster analyses (hierarchical or k-means, with silhouette scores); rolling-window analyses of substring, word, or regex-pattern occurrences; bubble visualizations (of term frequencies); and word clouds (of term frequencies or 
[MALLET](http://mallet.cs.umass.edu/)-produced topic modelling results). More functionality is being added on an ongoing basis.

# Release history
This repo reflects our Summer 2016 development work: Lexos v3.0b (currently unreleased).

Summer 2015: Our latest stable release (version 2.5) is available at [x](URL) and is running on our server at [lexos.wheatoncollege.edu](http://lexos.wheatoncollege.edu).

Summer 2014: Version 2.0 [https://zenodo.org/record/10956#.VXWcakZWJ-8](https://zenodo.org/record/10956#.VXWcakZWJ-8).

You can read more about our [Lexomics Research Group](http://lexomics.wheatoncollege.edu).

## System Architecture (in brief)
Lexos is written primarily in Python 2.7.11 (Anaconda 4.0.0) using the 
[Flask](http://flask.pocoo.org/) microframework, based on Werkzeug and Jinja 2. 
A heavy dose of Javascript and CSS is included on the front-end. We increasingly incorporate the wiz from 
[D3.js](http://d3js.org/) in our visualizations and the power in the 
[scikit-learn](http://scikit-learn.org/stable/) modules for text and statistical processing. 
The directions for setting up the development environment for testing (using localhost:5000) on your local machine are stored in the 0_InstallGuides directory.

## Dependencies
chardet, flask, matplotlib, numpy, pip, scikit-learn, scipy, pip (gensim, ete2, natsort, chardet)

The PDF Viewer extension needs to be enabled in the Chrome browser on MacOS. 

## License information
See the file LICENSE for information on the
terms & conditions for usage and a DISCLAIMER OF ALL WARRANTIES.

## Citation information:
Kleinman, S., LeBlanc, M.D., and Zhang, C. (2016). Lexos. v3.0. https://github.com/WheatonCS/Lexos/.

[//]: # "[Lexos Release 2.0](http://dx.doi.org/10.5281/zenodo.10956)"
[//]: # "[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.10956.png)](http://dx.doi.org/10.5281/zenodo.10956)"
