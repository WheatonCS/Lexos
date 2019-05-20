Shakespeare
=====================================================================

This experiment uses Lexos to observe some authorship attribution.

Shakespeare is a legendary Elizabethan playwright, but he has been confirmed
to have collaborated for some of his work. In particular, an authorship
attribution algorithm has been used to conclude that _Henry VI_ should be
jointly attributed to William Shakespeare and Christopher Marlowe, a contemporary
of the Bard.

Here, we will use Lexos to help show the collaborative relationship between
Shakespeare and Marlowe, using _Henry VI_.

Additionally, this experiment offers a brief look at the merge feature on
Lexos' Manage page.

Texts used: (16 total documents)

1. _Henry VI_ (3 parts)
2. Marlowe's _Edward the Second_
3. Marlowe's _Massacre at Paris_
4. Marlowe's _Tamburlaine the Great_ (2 parts)
5. Marlowe's _The Tragedy of Queen Dido of Carthage_
6. Marlowe's _The Tragical History of Doctor Faustus_
7. Shakespeare's _Henry VIII_
8. Shakespeare's _King Lear_
9. Shakespeare's _Macbeth_
10. Shakespeare's _Othello_
11. Shakespeare's _Richard II_
12. Shakespeare's _Timon of Athens_
13. Shakespeare's _Two Noble Kinsmen_

Using the tools from:   http://lexos.wheatoncollege.edu
and the files found in the FilesToUse/ directory, you should be able to
produce a dendrogram and a K-Means cluster as shown in ResultsToExpect/.

Steps
=====================================================================

(0) UPLOAD:

    (a) ALL files in the FilesToUse/ directory
(1) SCRUB:

    (a) Remove Punctuation
    (b) Make Lowercase
    (c) Remove Digits
    
    Apply Scrubbing
(2) MANAGE:

    Some alterations can be made to documents in the Manage tab.
        Recommended: select Display All Documents
    (a) Select "Henry VI_Part1", "Henry_VI_Part2", and "Henry_VI_Part3"
        (deselect all, select one part, shift click to select the others in between)
    (b) Right click on any of the files and select Merge Selected Documents
        Name the merge "Henry_VI" (this will create a new file)
    (c) Merge the two parts of Tambulaine as "Marlowe_Tambulaine_the_Great"
    (d) OPTIONAL: delete the partial documents (you should be left with 13 documents)
      (If you skip this step, make sure the 5 documents are not selected as you work)
        

(3) ANALYZE - Similarity Query:

    (a) Choose "Henry_VI" as the comparison document
    
    Get Similarity Rankings
    Compare your results with the .png in the ResultsToExpect/ directory.
(4) ANALYZE - Clustering - Hierarchical Clustering:

    (a) Use the default metrics:
        Distance Method: Euclidean
        Linkage Method: Average
    (b) Choose Tokenize - 1 - gram, by Tokens (default)
    (c) Choose Normalize - Proportional Counts (default)
    
    Get Dendrogram
    Compare your results with the .png in the ResultsToExpect/ directory.
(5) ANALYZE - Clustering - K-Means Clustering

    (a) Choose Number of Clusters: 6
    
    Get K-Means Result
    Compare your results with the .png in the ResultsToExpect/ directory.
