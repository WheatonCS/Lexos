# Middle English Source Texts

+ Ancrene Wisse. Edited by Robert Hasenfratz (2003)
  http://www.lib.rochester.edu/camelot/teams/hasenfratz.htm

+ Hali Meiðhad. From the Middle English Compendium. Edited by O. Cockayne; rev. F.J. Furnivall (1922)
  http://quod.lib.umich.edu/cgi/t/text/text-idx?c=cme;cc=cme;view=toc;idno=HMaid

+ Juliana. From the Middle English Compendium. Edited by O. Cockayne (1872)
  http://quod.lib.umich.edu/cgi/t/text/text-idx?c=cme;cc=cme;view=toc;idno=Juliana
	  
+ Kentish Sermons. From the Middle English Compendium. Edited by R. Morris (1872)
  http://quod.lib.umich.edu/cgi/t/text/text-idx?c=cme;cc=cme;view=toc;idno=AHA6129.0001.001
	  
+ Lambeth Homilies. From the Middle English Compendium. Edited by R. Morris (1872)
  http://quod.lib.umich.edu/cgi/t/text/text-idx?c=cme;cc=cme;view=toc;idno=AHA2688.0001.001
	  
+ Sawles Warde. From the Middle English Compendium. Edited by R. Morris (1872)
  http://quod.lib.umich.edu/cgi/t/text/text-idx?c=cme;cc=cme;view=toc;idno=AHA2688.0001.001

A short experiment examining similarities between texts in the AB 
Language (with the Kentish Sermons as a control). Finding which texts 
are most similar  is the first step to examining from word clouds and 
bubble graphs which words contribute most to their similarity.

The experiment shows the sensitivity of Lexomics to orthography. For 
Middle English texts, segments almost always cluster with other 
segments from the same text, regardless of vocabulary, due to the 
large orthographic differences between different dialects. Note that 
the TEAMS edition of Ancrene Wisse changes thorn and yogh to "th" 
and "y", so the results from this experiment exaggerate the difference 
of this text. A possible approach to minimise this effect would be to 
scrub the text individually, replacing "th" and "y" with thorn and 
yogh, then download the scrub text and upload it in place of the 
original with the other texts. However, this is likely to affect 
occurrences of these letters where they should not be changed.

Using the tools from:   http://lexos.wheatoncollege.edu
and the files found in the FilesToUse/ directory, you should
be able to produce a dendrogram as shown in ResultsToExpect/.

Steps:
======================================================================
(0) UPLOAD:

    (1) AncreneWisse.txt
    (2) HaliMeidhadB.txt
    (3) Juliana.txt
    (4) KentishSermons.txt
    (5) LambethHom.txt
    (6) SawlesWardeB.txt

(1) SCRUB:

    (a) Remove Punctuation
    (b) Make Lowercase
    (c) Remove Digits
    (d) Under Consolidations:
        Enter "ð:þ" (without the quotation marks)

    Apply Scrubbing
(2) CUT:
 
    (a) Tokens/Segment with a Segment Size of 700
    (b) leave other options on their default values

    Apply Cuts
(3) ANALYZE - Clustering - Hierarchical Clustering:

    (a) Use the default metrics:
        Distance Method: Euclidean
        Linkage Method: Average
    (b) Assign Temoporary Labels, if desired
    (c) leave other options on their default values
    
    Get Dendrogram
    Compare your result with the .png found in the ResultsToExpect/ directory.
    This dendrogram will look quite cluttered, there are a lot of segments here.
(4) VISUALIZE - Word Cloud:

    (a) Select segments 1, 88, and 90 of Ancrene Wisse
    
    Get Graph
    Compare your result with the .png file found in the ResultsToExpect/ directory.
    
    (b)Select segments 2, 3, and 4 of Ancrene Wisse
    
    Get Graph
    Compare your result with the .png file found in the ResultsToExpect/ directory.
(5) VISUALIZE - BubbleViz:

    (a) Select all segments with Toggle All
        The graph may take a bit to render.
    (b) Mouse over the bubbles to view word counts
    
    BubbleViz does not currently have a download function, but you can compare your
    result with the screenshot in the ResultsToExpect/ directory.


sk - July 1, 2013
