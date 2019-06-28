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
	    (the default is Remove Tag)
	(e) Lemmas: upload the DAZ_lemma.txt file
	(f) Consolidations: upload the DAZ_consolidation.txt file
	(g) Special Characters - choose Old English SGML

    Apply Scrubbing
(2) CUT:

    (a) Go to Manange (this is optional)
        - Right Click on A1.3_Dan_T00030 and edit its name to "Dan" (without the quotes)
        - Right Click on A3.3_Az_T00130 and edit its name to "AZ" (without the quotes)
    (b) On manage, deselect AZ so Dan is the only active document
    (c) Cut Dan using these settings:
        - Set Cut Mode to "Tokens"
        - Set "Segment Size" to 450
        - This should lead to ten segments of Daniel
    (d) Go back to manage and select Az so you have 11 active documents
    
(4) ANALYZE - Dendrogram

	(a) Use the following metrics:
	    - Distance Method: Euclidean
	    - Linkage Method: Average
	    - Orientation: Bottom
	
	Get Dendrogram
	Compare your result with the .png found in the ResultsToExpect/ directory.

ms - June 26, 2019
mjl - May 20, 2019
mdl - July 19, 2016
mdl - June 24, 2013


