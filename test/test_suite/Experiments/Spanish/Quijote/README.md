EL_INGENIOSO_HIDALGO DON_QUIJOTE_DE_LA_MANCHA
=====================================================================

This experiment tests Lexos' ability to handle Spanish documents.

Keep the step order in mind: for cutting by milestone, your milestone might
be case sensitive. In this case, CUT before SCRUB.

Using the tools from:   http://lexos.wheatoncollege.edu
and the files found in the FilesToUse/ directory, you should
be able to produce a dendrogram as shown in ResultsToExpect/.

Steps
=====================================================================

(0) UPLOAD:

    EL_INGENIOSO_HIDALGO DON_QUIJOTE_DE_LA_MANCHA.txt

(1) CUT:

    (a) Check Cut by Milestone, enter "CHAPTER" (minus the quotes)
    This will lead to twenty segments

	Apply Cuts
(2) SCRUB:

    (a) Remove Punctuation
    (b) Make Lowercase
    (c) Remove Digits
    
    Apply Scrubbing
(3) ANALYZE - Clustering - Hierarchical Clustering:

	(a) Use the default metrics:
	    Distance Method: Euclidean
	    Linkage Method: Average
	(c) Edit Labels (optional)
	Get Dendrogram
	Compare your result with the .png found in the ResultsToExpect/ directory.


mjl - May 20, 2019
