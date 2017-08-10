# Modern Chinese

1. Sample Test
---------------------------------------------------------------------
In order to test if Lexos can analyze Modern Chinese literature, We 
chose the "Turbulent Stream" trilogy and the "Love" trilogy written 
by Ba jin, and two novels written by Jia Pingwa. Here we show how 
cluster analysis can be used to identify the authorships, and to 
show certain writer's writing style changes over the years.

Using the tools from:   http://lexos.wheatoncollege.edu
and the files found in the FilesToUse/SampleTest/ directory, you 
should be able to produce a dendrogram as shown in ResultsToExpect/.

###Sample Files:
Ba Jin's Turbulent Stream Trilogy

(1) BaJin_TheFamily_1933.txt
(2) BaJin_Spring_1938.txt
(3) BaJin_Autumn_1940.txt

Ba Jin's Love Trilogy

(4) BaJin_Fog_1931.txt
(5) BaJin_Rain_1933.txt
(6) BaJin_Lightning_1935.txt

(7) JiaPingwa_MissingWolves_2000.txt
(8) JiaPingwa_ShaanxiOpera _2005.txt


Steps:
=====================================================================
(0) UPLOAD 8 sample files

(1) SCRUB 

    (a) Remove punctuation
    (b) Remove Digits
    (c) Apply Scrubbing
(2) CUT 

    (a) Cut all the files into 2 segments
        (this will lead to 16 segments in total)
    (b) Apply Cuts
(3) ANALYZE - Dendrogram

    (a) Use the default metrics Distance Method: Euclidean and Linkage Method: Average
    (b) Give a Title
    (c) Tokenize: 2-gram by Characters
    (d) Normalize: Weighted Counts (TF/IDF) 
    (e) Get Dendrogram
    (f) Compare your result with the .pdf found in the 
        ResultsToExpect/ directory.

2. More Modern Chinese Files
---------------------------------------------------------------------
(1) Liu Cixin: Three Body (2007).txt



qz - June 9, 2014
