
Corpus:  Anglo Saxon (Dictionary of Old English)

Finding divisions within a poem is a problem at
least related to the one we had addressed in the Daniel/Azarias analyses.
Here we analyze the Anglo-Saxon poem Genesis to see
if our lexomic methods distinguish the sections of the (one) Genesis poem
where the two sections are known as Genesis A and Genesis B.

Using the tools from:   http://lexos.wheatoncollege.edu
and the files found in the FilesToUse/ directory, you should
be able to produce a dendrogram as shown in ResultsToExpect/.

A fuller description of this example can be found in:

Drout, M.D.C., M. J. Kahn, M.D. LeBlanc, and Nelson, C. '11 (2011). 
Of Dendrogrammatology: Lexomic Methods for Analyzing the Relationships 
Among Old English Poems. Journal of English and Germanic Philology, 
July 2011, 301-336.

HERE

Steps:
=====================================================================
(0) UPLOAD A1.1_GenAB_T00010.txt
=====================================================================
(1) SCRUB both:
    (a) Remove punctuation
    (b) Make Lowercase
    (c) Remove Digits
    (d) Keep Words Between corr/foreign Tags

    (e) Set Special Characters to Dictionary of Old English (sgml)

    Apply Scrubbing
=====================================================================
(2) CUT A1.1_GenAB_T00010.txt into 1500 word chunks.

(4) Apply Cuts
=====================================================================
(5) ANALYZE - Dendrogram
     (a) Use the default metrics Distance Method: Euclidean and Linkage Method: Average
     (b) Give a Title
     (c) Edit Labels (optional, but recommended)

     (d) Get Dendrogram
     (e) compare your result with the .pdf found in the ResultsToExpect/ directory.
=====================================================================

mdl - June 24, 2013


