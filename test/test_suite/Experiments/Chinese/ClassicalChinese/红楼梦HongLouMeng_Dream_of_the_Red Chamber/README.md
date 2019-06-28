# Classical Chinese - _红楼梦HongLouMeng (Dream of the Red Chamber)_

The Lexos tool can be used to confirm the controversial authorship of one of
China's Four Great Classical Novels. Written in the middle of the 18th century
during the Qing Dynasty, "Dream of the Red Chamber" is considered a masterpiece
of Chinese literature. The author, Cao Xueqin(曹雪芹), passed away before finishing 
the novel. It is commonly accepted that the first eighty chapters were written
by him, while the remaining forty chapters were written by Gao E(高鶚). Meanwhile,
some scholars claimed that Chapter 64 and 67, two chapters missing from the oldest
edition, could also have been written by someone other than Cao Xueqin. (Tu and
Hsiang, 2013)

Here, we analyze two segments of files including one with the first 80 chapters and
the other one with the remaining 40 chapters. After cutting them into pieces (each
with approximately 10 chapters) you can observe that the last 40 chapters cluster
separately from the first 80 chapters in the dendrogram.

Though the K-Means clustering method with 12 clusters, the Lexos tool groups
different stories in each cluster, with the last 40 chapters almost grouped
together in one cluster.

The test files are:

* First80Chapters.txt
* Late40Chapters.txt

(If testing individual chapters:)
* __ALL__ files in Individual_Chapters folder

Using the tools from:   http://lexos.wheatoncollege.edu
and the files found in the FilesToUse/ directory, you should be able to
produce a dendrogram and a K-Means cluster as shown in ResultsToExpect/.

Steps:
=====================================================================
(0) UPLOAD:

    (a) First80Chapters.txt
    (b) Last40Chapters.txt

(1) SCRUB:

    (a) Remove Punctuation
    (b) Remove Digits

    Apply Scrubbing
(2) CUT:

    (a) Go to manage and deselect Late40Chapters so that First80Chapters is the only active document
    (b) Cut the First80Chapters using these settings:
        - Set Cut Mode to "Segments"
        - Set "Number of Segments" to 8
        - Click Apply
    (c) Go back to manage and deselect all documents except Late40Chapters
    (d) Cut the Late40Chapters using these settings:
        - Set Cut Mode to "Segments"
        - Set "Number of Segments" to 4
        - Click Apply
    (e) Go back to manage and select all of the documents that were cut (everything except the original documents)
    
    You should have 12 Active Documents
(3) ANALYZE - Dendrogram:

    (a) Use the default metrics:
        - Distance Method: Euclidean (default)
        - Linkage Method: Average (default)
        - Orientation: Bottom
    (b) Tokenize
        - By Characters
        - Change grams to 2
    
    Generate Dendrogram
    Compare your result with the .png found in the ResultsToExpect/ directory.

IF TESTING INDIVIDUAL CHAPTERS:
=====================================================================

(0) UPLOAD:
    
    (a) All files in the Individual_Chapters folder
    
(1) SCRUB:

    (a) Remove Punctuation
    (b) Remove Digits

    Apply Scrubbing
(2) ANALYZE - K-Means

     (a) Options - change Clusters to 12
     (b) Advanced - change Maximum Iterations: 1000
     (c) Tokenize - choose By Characters, change grams to 2
     
     Generate K-Means Result
     Compare your result with the .png found in the ResultsToExpect/ directory.
        Do not expect a perfect match, but it should be quite similar.

Reference:
Tu, Hsieh-Chang; Hsiang, Jieh (2013).  A Text-Mining Approach to the Authorship 
Attribution Problem of Dream of the Red Chamber. July 18, 2013.
(http://dh2013.unl.edu/abstracts/ab-162.html)


ms - June 27, 2019
mjl - May 20, 2019
jg - June 30, 2014
