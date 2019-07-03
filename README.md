# Lexos
[![Build status](https://ci.appveyor.com/api/projects/status/vqyfuqr15gfqj544/branch/master?svg=true)](https://ci.appveyor.com/project/chantisnake/lexos/branch/master)
[![Build Status](https://travis-ci.com/WheatonCS/Lexos.svg?branch=master)](https://travis-ci.com/WheatonCS/Lexos)
[![JavaScript Style Guide](https://img.shields.io/badge/code_style-standard-brightgreen.svg)](https://standardjs.com)
[![DOI](https://zenodo.org/badge/10040275.svg)](https://zenodo.org/record/1403869#.W4LuCRgpA5k)

## Summary

Lexos is a suite of tools designed to facilitate the computational analysis of literary and historical texts. It offers an integrated workflow in which the pre-processing ("scrubbing"), analysis, and visualization steps can be accomplished in a single, web-based environment. Scrubbing features include handling punctuation, stop words, markup tags, and character consolidations, as well as document segmentation, culling, and n-gram tokenization. Analytical tools include basic document statistics, hierarchical and k-means cluster analysis, cosine similarity ranking, and z-score analysis. Visualizations include word and bubble clouds, comparative "multiclouds", and rolling window analysis. Analytical tools produce line, PCA, Voronoi cell, and dendrogram graphs. Each of the tools has export functionality.

Lexos is aimed at entry-level users as well as advanced scholars using small to medium-sized text corpora. It places particular emphasis on the processing of ancient and non-standard languages, as well as non-Western languages that do not use the Roman alphabet.

Lexos is produced by the [Lexomics Research Group](http://lexomics.wheatoncollege.edu). An online version of Lexos v4.0 is available at [http://lexos.wheatoncollege.edu/](http://lexos.wheatoncollege.edu/).

## Release history

This repo reflects ongoing development since our Summer 2019: Lexos v4.0

### New Features in v4.0

- A new UI for all tools.
- Several features have been promoted from beta, including Scrape URLs, Bootstrap Consensus Tree, and Content Analysis.
- Several color themes can now be selected from the header bar.
- A walkthrough for each page is now available.
- Active documents can be selected at any point from the footer.
- Visualizations now have selectable color schemes.
- Several tools now have PNG and SVG download options.
- Several scrub options are now more robust and inclusive.
- More helpful/descriptive error handling.
- Redesigned and rewritten help section and tooltips.

### Removed Features in v4.0

- Video guides removed (replaced with page walkthroughs).
- "Assign Temporary Labels" function was removed from the tools that used it.
- Some advanced word cloud and Bubbleviz options were removed.
- TF-IDF distance metric option removed.

## Installation

Installation instructions for Lexos v4.0 are available in the project Wiki.

- [Windows Install Guide](https://github.com/WheatonCS/Lexos/wiki/Windows-Install-Guide)
- [macOS Install Guide](https://github.com/WheatonCS/Lexos/wiki/macOS-Install-Guide)
- [Linux Install Guide](https://github.com/WheatonCS/Lexos/wiki/Linux-Install-Guide)

### System Architecture (in brief)

Lexos v4.0 is written in Python 3.7 (as distributed in [Anaconda](https://www.continuum.io/downloads) 2019.03) using the
[Flask](http://flask.pocoo.org/) microframework, based on Werkzeug and Jinja2.

The front end is designed using [jQuery](https://jquery.com/). We increasingly incorporate the viz from
[D3.js](http://d3js.org/) and the [Plotly](https://plot.ly/python/) Python graphing library in our visualizations and the power in the
[scikit-learn](http://scikit-learn.org/stable/) modules for text and statistical processing.

The directions for setting up the development environment for testing (using `localhost:5000`) on your local machine can be found on our [wiki](https://github.com/WheatonCS/Lexos/wiki) page.

## Dependencies

Lexos requires the following Python packages:

`beautifulsoup-4, biopython, chardet, colorlover, flask, gensim, lxml, matplotlib, natsort, numpy, pandas, plotly, requests, scikit-learn, scipy, werkzeug`

Lexos works on Chrome and Firefox. Other browsers are not supported, and some features may not function.

## License Information

See the file LICENSE for information on the
Terms & Conditions for usage and a DISCLAIMER OF ALL WARRANTIES.

## Citation Information

Kleinman, S., LeBlanc, M.D., Drout, M., and Feng, W. (2019). _Lexos_. v4.0 [https://github.com/WheatonCS/Lexos/](https://github.com/WheatonCS/Lexos/).
doi:10.5281/zenodo.1403869.
