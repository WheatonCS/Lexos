# Rolling Window

File to use: BeowulfFullLines.txt

This is an example shown to me by the English kids. 
It shows the clear divide between the two scribes of
Beowolf by graphing the difference in their 
preference to use either more þ or ð's in their
writing.  

================================================================================
STEP0: Upload BeowulfFullLines.txt
================================================================================
STEP1: Scrub using default settings, although it it not required for this exp.
    -Remove all Punct
    -Make Lowercase
    -Remove Digits
================================================================================
STEP2: Rolling Window Graph
    -Count Type = Rolling Ratio
    -Window Type = Window of Words
    -Token Type = Strings
    -Seach Tokens  þ:ð
    -Window Size = 1000
    -(Optional) Hide Individual Points (sacrifices extra info for increased 
        speed and readability)
    -(Optional) Black and White Only (If you wanted to download the SVG for
        publishing in a journal)

*Notice the drastic change in frequency which begins at aproximately word 10,000
    This is what the English kids have determined is the crossover between the 
    two different scribes who were responsible for writing Beowulf


================================================================================
================================================================================

File to Use: pride_and_prejudice_ms.txt

This is an example file which shows the functionality of 
the 'Document has Milestones' button in the Rolling Window 
options.  The Sample text is marked with 61 'MILESTONE's, 
one at the beginning of each chapter. This is a useful 
technique for analyzing texts in rolling window becuase 
you can cleary see the divisions of your text along with 
the graph data


================================================================================
STEP0: Upload pride_and_prejudice_ms.txt
================================================================================
STEP1: Rolling Window Graph
    -Search for whatever you want (i.e. Average of 'the')
    -Window Size  1000
    -Window type = words
    -Token type = string
    -Document Has Milestones = Checked
    -Milestone Delimeter = MILESTONE
    -(Optional) Hide Individual Points
    
*The 61 vertical lines coorespond to the locations of the 61 instances of 
    'MILESTONE' in the text, one at the beginning of each chapter.
**For an additional test, change the milestone delimeter to 'Chapter' to confirm 
    that the milestones are in the right places.
    
CGW 6/23/151
