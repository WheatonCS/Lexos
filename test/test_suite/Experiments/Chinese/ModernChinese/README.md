# Modern Chinese

Sample Test
---------------------------------------------------------------------
In order to test if Lexos can analyze Modern Chinese literature, we 
chose the "Turbulent Stream" trilogy and the "Love" trilogy written 
by Ba Jin, along with two novels written by Jia Pingwa. Here we show how 
cluster analysis can be used to identify authorship, and to 
show how a certain writer's writing style changes over the years.

Using the tools from:   http://lexos.wheatoncollege.edu
and the files found in the FilesToUse/SampleTest/ directory, you 
should be able to produce a dendrogram as shown in ResultsToExpect/.

#### Sample Files:
Ba Jin's Turbulent Stream Trilogy

* (1) BaJin_TheFamily_1933.txt
* (2) BaJin_Spring_1938.txt
* (3) BaJin_Autumn_1940.txt

Ba Jin's Love Trilogy

* (4) BaJin_Fog_1931.txt
* (5) BaJin_Rain_1933.txt
* (6) BaJin_Lightning_1935.txt

Jia Pingwa's Novels

* (7) JiaPingwa_MissingWolves_2000.txt
* (8) JiaPingwa_ShaanxiOpera _2005.txt


Steps:
=====================================================================
(0) UPLOAD:

    The above 8 sample files.

(1) SCRUB:

    (a) Remove Punctuation
    (b) Remove Digits
    
    Apply Scrubbing
(2) CUT: 

    (a) Set cut mode to "Segments"
    (b) Set "Number of Segments" to 2
    
    Apply Cuts
    (There should be 16 Active Documents after cutting)
(3) ANALYZE - Dendrogram:

    (a) Use the following metrics:
        - Distance Method: Euclidean (default)
        - Linkage Method: Average (default)
        - Orientation: Bottom
    (b) Tokenize:
        - By Characters
        - Change grams to 2
    (c) Normalize:
        - Choose TF-IDF
    
    Generate Dendrogram
    Compare your result with the .png found in the ResultsToExpect/ directory.




mjl - May 20, 2019
LA - Aug 15, 2017
qz - June 9, 2014
