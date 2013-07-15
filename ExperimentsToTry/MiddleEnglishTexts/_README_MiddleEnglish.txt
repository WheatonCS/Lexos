Source Texts:

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
=====================================================================
(0) UPLOAD the texts below:

+ AncreneWisse.txt
+ HaliMeidhadB.txt
+ Juliana.txt
+ KentishSermons.txt
+ LambethHom.txt
+ SawlesWardeB.txt
=====================================================================
(1) SCRUB both:
    (a) Remove punctuation
    (b) Make Lowercase
    (c) Remove Digits
	(d) Click "Consolidations". Enter "ð,þ" (without the quotation marks)

    Apply Scrubbing
=====================================================================
(2) CUT all texts into 700 word chunks.

(3) Apply Cuts
=====================================================================
(5) ANALYZE - Dendrogram
     (a) Use the default metrics Distance Method: Euclidean and Linkage Method: Average
     (b) Give a Title
     (c) Edit Labels, if desired
     (d) Get Dendrogram. Download Diagram.
	 (e) Enter "25" in the "Leaves to Display" field. Get and download the dendrogram again.
     (f) Compare your result with the .pdf found in the ResultsToExpect/ directory.
=====================================================================
(6) ANALYZE - Word Cloud
     (a) Select segments 1, 88, and 90 of Ancrene Wisse and click Get Graph. Click the Download PNG
	     link to save the image. Select segments 2, 3, and 4 of Ancrene Wisse and click Get Graph.
		 Download the PNG.
     (b) Compare your result with the .png files found in the ResultsToExpect/ directory.
=====================================================================
(6) ANALYZE - BubbleViz
     (a) Select all segments by clicking "Check All" in the dropdown menu. The graph will take about 
	     10 seconds to render.
     (b) Mouse over the bubbles to view word counts. If a bubble is too small to display the word 
	     label, mousing over the bubble will also display the word it represents.
	 (c) BubbleViz does not currently have a download function, but you can compare your result with the 
	     screenshot in the ResultsToExpect/ directory.


sk - July 1, 2013
