# Genesis A and B

Corpus:  Anglo Saxon (Dictionary of Old English)

Finding divisions within a poem is a problem at
least related to the one we had addressed in the Daniel/Azarias analyses.
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
    (d) Scrub Tags and then Tag Options:
        (the gear for Tag Options will appear after selecting Scrub Tags)
    - Set all tags to:   Remove Tag Only (default)
    - Set teiheader tag to:  Remove Element and All Its Contents
    - Save Changes and then Close
    (e) Set Special Characters - Pre-Defined Rule Sets:
        Dictionary of Old English SGML

    Apply Scrubbing
(2) CUT:

    (a) Tokens/Segment with a Segment Size of 1500
    (b) leave other options with their default option values

    Apply Cuts
(3) ANALYZE - Clustering - Hierarchical Clustering:

    (a) Use the default metrics Distance Method: Euclidean and Linkage Method: Average
    (b) Assign Temporary Labels (optional, but recommended)
        Note that each segment ends in an underscore followed by a number
        That number is the order of the sections, removing it is not recommended
    (c) Choose the default Tokenization (token 1-grams)
    (d) Choose the default Normalization (Proportional)
    
    Get Dendrogram
    Compare your result with the .png found in the ResultsToExpect/ directory.


mdl - June 28, 2016


