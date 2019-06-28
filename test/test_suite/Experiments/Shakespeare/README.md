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

    (a) Select "Henry VI_Part1", "Henry_VI_Part2", and "Henry_VI_Part3" only
        (Right click, deactivate all, then click on those three parts)
    (b) Right click on any of the files and select Merge Active
        Name the merge "Henry_VI" (this will create a new file)
    (c) Merge the two parts of Tamburlaine as "Marlowe_Tamburlaine_the_Great"
    (d) Delete the partial documents (you should be left with 13 documents)
    (e) Right-click and select Activate All
        

(3) ANALYZE - Similarity Query:

    (a) Comparison Documet - Select Henry_VI
    
    Generate Similarity Rankings
    Compare your results with the .csv in the ResultsToExpect/ directory.
(4) ANALYZE - Dendrogram

    (a) Use the following metrics:
        - Distance Method: Euclidean
        - Linkage Method: Average
        - Orientation: Bottom
    
    Generate Dendrogram
    Compare your results with the .png in the ResultsToExpect/ directory.
(5) ANALYZE - K-Means

    (a) Change Clusters to 6
    
    Generate K-Means Result
    Compare your results with the .png in the ResultsToExpect/ directory.

ms - June 27, 2019
mjl - May 20, 2019
