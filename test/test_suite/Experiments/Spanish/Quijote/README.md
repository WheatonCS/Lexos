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

    (a) Set cut mode to "Milestones"
    (b) Set "Milestone" to "CHAPTER" (not in quotes)

	Apply Cuts
	(You should have 20 segments of the original document)
(2) SCRUB:

    (a) Remove Punctuation
    (b) Make Lowercase
    (c) Remove Digits
    
    Apply Scrubbing
(3) ANALYZE - Dendrogram:

	(a) Use the following metrics:
	    - Distance Method: Euclidean
	    - Linkage Method: Average
	    - Orientation: Bottom
	    
	Generate Dendrogram
	Compare your result with the .png found in the ResultsToExpect/ directory.

ms - June 27, 2019
mjl - May 20, 2019
