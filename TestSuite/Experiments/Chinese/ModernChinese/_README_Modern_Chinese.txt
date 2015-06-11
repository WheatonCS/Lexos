Modern Chinese

In order to test if Lexos can analyze Modern Chinese literature, We chose the "Turbulent Stream" trilogy and the "Love" trilogy written by Ba jin, and two novels written by Jia Pingwa.
Here we show how cluster analysis can be used to identify the authorships, and to show certain writer's writing style changes over the years.

Using the tools from:   http://lexos.wheatoncollege.edu
and the files found in the FilesToUse/ directory, you should
be able to produce a dendrogram as shown in ResultsToExpect/.

Sample Files:
=====================================================================
Ba Jin's Turbulent Stream Trilogy
(1) Ba Jin: The Family (1933).txt
(2) Ba Jin: Spring (1938).txt
(3) Ba Jin: Autumn (1940).txt

Ba Jin's Love Trilogy
(4) Ba Jin: Fog (1931).txt
(5) Ba Jin: Rain (1933).txt
(6) Ba Jin: Lightning (1935).txt

(7) Jia Pingwa: Missing Wolves (2000).txt
(8) Jia Pingwa: Shaanxi Opera (2005).txt


Steps:
=====================================================================
(0) UPLOAD 8 sample files
=====================================================================
(1) SCRUB 
    (a) Move punctuation
    (b) Remove Digits
    (c) Apply Scrubbing
=====================================================================
(2) CUT 
    (a) Cut all the files into 2 chunks
        (this will lead to 16 chunks in total)
    (b) Apply Cuts
=====================================================================
(3) ANALYZE - Dendrogram
    (a) Use the default metrics Distance Method: Euclidean and Linkage Method: Average
    (b) Give a Title
    (c) Tokenize: 2-gram by Characters Only within words
    (d) Normalize: Weighted Counts (TF/IDF) 
    (e) Get Dendrogram
    (f) compare your result with the .pdf found in the ResultsToExpect/ directory.
=====================================================================

qz - June 9, 2014