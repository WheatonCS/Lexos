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
seperately from the first 80 chapters in the dendrogram.

Though the K-Means clustering method with 12 clustsers, the Lexos tool groups
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

    OR if testing individual chapters:
    (c) all files in Individual_Chapters folder

(1) SCRUB:

    (a) Remove Punctuation
    (b) Remove Digits

    Apply Scrubbing
(2) CUT:

    (a) Default Cutting Options - Segments/Documents - Number of Segments: 1
    (b) Individual Cutting Options: (next to the document title in the Preview window) 
        First80Chapters - Segments/Documents - Number of Segments: 8
        Late40Chapters - Segments/Documents - Number of Segments: 4

    Apply Cuts
(3) ANALYZE - Clustering - Hierarchical Clustering:

    (a) Use the default metrics:
        Distance Method: Euclidean
        Linkage Method: Average
    (b) Choose Tokenize - 2 - gram, by Characters
    (c) Choose Normalize - Proportional Counts (default)
    
    Get Dendrogram
    Compare your result with the .png found in the ResultsToExpect/ directory.

####(IF TESTING INDIVIDUAL CHAPTERS)

Do not forget to SCRUB the individual chapter files (see above)

(4) ANALYZE - Clustering - K-Means Clustering:

     (a) K Value: 12
     (b) Advanced K-Means Options:
            Maximum Number of Iterations: 1000
     (c) Choose Tokenize - 2 - gram, by Characters
     (d) Choose Normalize - Proportional Counts (default)
     
     Get K-Means Result
     Compare your result with the .png found in the ResultsToExpect/ directory.
        Do not expect a perfect match, but it should be quite similar.

Reference:
Tu, Hsieh-Chang; Hsiang, Jieh (2013).  A Text-Mining Approach to the Authorship 
Attribution Problem of Dream of the Red Chamber. July 18, 2013.
(http://dh2013.unl.edu/abstracts/ab-162.html)


jg - June 30, 2014
