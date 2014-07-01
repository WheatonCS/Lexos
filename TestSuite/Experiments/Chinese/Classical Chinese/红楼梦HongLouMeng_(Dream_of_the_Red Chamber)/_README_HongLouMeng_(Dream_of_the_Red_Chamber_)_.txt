
Corpus:  Classical Chinese - 红楼梦HongLouMeng_(Dream_of_the_Red_Chamber)

The lexomics tool can be used to confirm the controversial authorship of one of
China's Four Great Classical Novels. Written in the middle of the 18th century
during the Qing Dynasty, "Dream of the Red Chamber" is considered a masterpiece
of Chinese literature. The author, Cao Xueqin(曹雪芹), passed away before finishing 
the novel. It is commonly accepted that the first eighty chapters were written
by him, while the remaining fourty chapters were written by Gao E(高鶚). Meanwhile,
some scholars claimed that Chapter 64 and 67, two chapters missing from the oldest
edition, could also have been written by someone other than Cao Xueqin. (Tu and
Hsiang, 2013)

Here, we analyze two chunck of files including one with the first 80 chapters and
the other one with the remaining 40 chapters. After cutting them into pieces each
with 10 chapters, it is shown from the dendrogram that the late 40 chapters show
up seperately from the first 80 chapters.

Though the K-Means clustering method with 12 clustsers, lexomics tool also groups
each cluster with different stories of the main characters, and with the late 40
chapters almost grouped together in one cluster.

These test files are:

First80Chapters.txt
Late40Chapters.txt

(If testing individual chapters:)
all files in Individual_Chapters folder

Using the tools from:   http://lexos.wheatoncollege.edu
and the files found in the FilesToUse/ directory, you should
be able to produce a dendrogram as shown in ResultsToExpect/.

Steps:
=====================================================================
(0) UPLOAD 
    (a) First80Chapters.txt
    (b) Late40Chapters.txt

    OR if testing individual chapters:
    (c) all files in Individual_Chapters folder
=====================================================================
(1) SCRUB:
    (a) Remove punctuation
    (b) Remove Digits

    Apply Scrubbing
=====================================================================
(2) CUT:
    (a) Default Cutting Options - Chunks/File - Number of Chuncks: 1
    (b) Individual Cutting Options:
        First80Chapters - Chuncks/File - Number of Chuncks: 8
        Late40Chapters - Chuncks/File - Number of Chuncks: 4

    Apply Cuts
=====================================================================
(3) ANALYZE - Hierarchical Clustering - Dendrogram
     (a) Use the default metrics Distance Method: Euclidean 
         and Linkage Method: Average
     (b) Give a Title
     (c) Choose Tokenize - 2 - gram, by Characters, check the box Only within words
     (d) Choose normalize - Proportional Counts (default)

     (e) Get Dendrogram
     (f) compare your result with the .pdf found in the ResultsToExpect/ directory.
=====================================================================
(IF TESTING INDIVIDUAL CHAPTERS)
(4) ANALYZE - K-Means Clustering
     (a) K Value: 12
     (b) Maximum Number of Iterations: 1000
     (c) Choose Tokenize - 2 - gram, by Characters, check the box Only within words
     (d) Choose normalize - Proportional Counts (default)

     (e) Get K-Means
=====================================================================

Reference:
Tu, Hsieh-Chang; Hsiang, Jieh (2013).  A Text-Mining Approach to the Authorship 
Attribution Problem of Dream of the Red Chamber. July 18, 2013.
(http://dh2013.unl.edu/abstracts/ab-162.html)


jg - June 30, 2014