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
are most similar is the first step to examining from word clouds and 
bubble graphs which words contribute most to their similarity.

The experiment shows the sensitivity of Lexomics to orthography. For 
Middle English texts, segments almost always cluster with other 
segments from the same text, regardless of vocabulary, due to the 
large orthographic differences between different dialects. Note that 
the TEAMS edition of Ancrene Wisse changes thorn and yogh to "th" 
and "y", so the results from this experiment exaggerate the difference 
of this text. A possible approach to minimize this effect would be to 
scrub the text individually, replacing "th" and "y" with thorn and 
yogh, then download the scrub text and upload it in place of the 
original with the other texts. However, this is likely to affect 
the occurrences of these letters where they should not be changed.

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
    
    (a) Set cut mode to "Tokens" (default)
    (b) Set "Segment Size" to 700
    
    Apply Cuts
(3) ANALYZE - Dendrogram:

    (a) Use the following metrics:
        - Distance Method: Euclidean
        - Linkage Method: Average
        - Orientation: Bottom
    
    Generate Dendrogram
    Compare your result with the .png found in the ResultsToExpect/ directory.
    This dendrogram will look quite cluttered, there are a lot of segments here.
(4) VISUALIZE - Word Cloud:

    (a) Go to manage
        - Right Click and deactivate all 
        - Select segments 1, 88, and 90 of Ancrene Wisse
    (b) Go to Word Cloud
    (c) Change color to "Tie-Dye"
    
    Generate Graph
    Compare your result with the .png file found in the ResultsToExpect/ directory.
    
    
    (c) Go back to manage
        - Right Click and deactivate all
        - select segments 2, 3, and 4 of Ancrene Wisse
    (d) Go to Word Cloud
    (e) Change color to "Tie-Dye"
    
    Generate Graph
    Compare your result with the .png file found in the ResultsToExpect/ directory.
(5) VISUALIZE - BubbleViz:

    (a) Go to manage
        - Right Click and deactivate all
        - Select the 6 original documents only
    (b) Go to BubbleViz and generate the graph
    (c) Change color to "Tie-Dye"
    (d) Mouse over the bubbles to view word counts
    
    Compare your result with the .png in the ResultsToExpect/ directory.

ms - June 27, 2019
mjl - May 20, 2019
sk - July 1, 2013
