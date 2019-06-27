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
(0) UPLOAD:

    (1) A1.3_Dan_T00030.txt
    (2) A3.3_Az_T00130.txt

(1) SCRUB:

	(a) Remove punctuation
	(b) Make Lowercase
	(c) Remove Digits
	(d) Scrub Tags - keep default options
	    (the default is to keep text within but remove <corr> and <foreign> tags)
	(e) Lemmas: upload the DAZ_lemma.txt file
	(f) Consolidations: upload the DAZ_consolidation.txt file
	(g) Set Special Characters - Pre-Defined Rule Set to Dictionary of Old English SGML

    Apply Scrubbing
(2) CUT:

    (a) Choose Default Cutting Options, select Segments/Document and Number of
        Segments as 1 (we don't want to cut Azarias)
    (b) For Daniel, select the Individual Options button (by its title in the Preview
        window) and select Segments/Document: Segment Size: 450 word chunks,
        zero Overlap, 50% Last Proportion
    This will lead to ten segments of Daniel

	Apply Cuts
(4) ANALYZE - Dendrogram

	(a) Use the default metrics:
	    Distance Method: Euclidean
	    Linkage Method: Average
	(b) Assign Temporary Labels: (recommended, but not required)
	    Name the Azarias chunk as "AZ"
	    Name the Daniel chunks as "Dan1", "Dan2", etc.
	
	Get Dendrogram
	Compare your result with the .png found in the ResultsToExpect/ directory.

mjl - May 20, 2019
mdl - July 19, 2016
mdl - June 24, 2013


