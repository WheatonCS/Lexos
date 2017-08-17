# DAZ

Corpus:  Anglo Saxon (Dictionary of Old English)

In order to test the effectiveness of our methods, we applied them to
texts in the Old English corpus whose relationships with each other are
already known. Here we show how cluster analysis can be used to identify the
section in a long poem that is most similar to a different poem:
ten chunks of the Anglo Saxon poem Daniel and the  
Anglo Saxon poem Azarias.  

Using the tools from:   http://lexos.wheatoncollege.edu
and the files found in the FilesToUse/ directory, you should
be able to produce a dendrogram as shown in ResultsToExpect/.

A fuller description of this example can be found in:

Drout, M.D.C., M. J. Kahn, M.D. LeBlanc, and Nelson, C. '11 (2011). 
Of Dendrogrammatology: Lexomic Methods for Analyzing the Relationships 
Among Old English Poems. Journal of English and Germanic Philology, 
July 2011, 301-336.

Steps:
=====================================================================
(0) UPLOAD A1.3_Dan_T00030.txt and A3.3_Az_T00130.txt

(1) SCRUB both:

	(a) Remove punctuation
	(b) Make Lowercase
	(c) Remove Digits
	(d) Scrub Tags (the default is to keep text within but remove <corr> and <foreign> tags)
	(e) Load the DAZ_lemma.txt file for Lemmas
	(f) Load the DAZ_consolidation.txt file for Consolidations
	(g) Set Special Characters to Dictionary of Old English (sgml)

    Apply Scrubbing
(2) CUT:
    (a) On the main (left) Default Cutting Options, select Segments/Document and Number of
    Segments as 1 (for Azarias)
    (b) For Daniel, select the Individual Options button (on right for Daniel) and a Segment Size: 450 word chunks, 
    zero Overlap, 50% Last Proportion;
    (this will lead to ten chunks of Daniel)

	Apply Cuts
(4) ANALYZE - Dendrogram

	(a) Use the default metrics Distance Method: Euclidean and Linkage Method: Average
	(b) Give a Title
	(c) Edit Labels - name the Azarias chunk as "AZ" and the Daniel chunks as "Dan1", "Dan2", etc.
	(d) Get Dendrogram
	(e) compare your result with the .pdf found in the ResultsToExpect/ directory.

mdl - July 19, 2016
mdl - June 24, 2013


