# Genesis A and B

Corpus:  Anglo Saxon (Dictionary of Old English)

Finding divisions within a poem is a problem, at least related to the one we 
had addressed in the Daniel/Azarias analysis.

Here we analyze the Anglo-Saxon poem Genesis to see
if our lexomics methods distinguish the sections of the (one) Genesis poem
where the two sections are known as Genesis A and Genesis B.

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

    A1.1_GenAB_T00010.txt

(1) SCRUB:

    (a) Remove Punctuation
    (b) Make Lowercase
    (c) Remove Digits
    (d) Scrub Tags and change the options to:
        - Set all tags to:   Remove Tag (default)
        - Set teiheader tag to:  Remove All
        - Click OK
    (e) Special Characters - choose Old English SGML

    Apply Scrubbing
(2) CUT:

    (a) Set cut mode to "Tokens" (default)
    (b) Set "Segment Size" to 1500

    Apply Cuts
    (This should cut the document into 11 segments)
(3) ANALYZE - Dendrogram:

    (a) Use the following metrics:
        - Distance Method: Euclidean
        - Linkage Method: Average
        - Orientation: Bottom
    
    Generate Dendrogram
    Compare your result with the .png found in the ResultsToExpect/ directory.

ms - June 26, 2019
mjl - May 20, 2019
mdl - June 28, 2016


