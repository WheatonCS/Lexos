File to use: Dream of the Red Chamber - Chapter 1

This is an example of using the statistics page to determine statistical
information about segments of an entire corpus in Mandarin.  

================================================================================
STEP0: Upload DreamCH1.txt
================================================================================
STEP1: Scrub using the default settings.
    -Remove all Punct
    -Make Lowercase
    -Remove Digits
    -Apply Scrubbing
================================================================================
STEP2: Cut the file
    -Select 'Characters/Segment'
    -Change the 'Segment Size' to 700 (keep 'Overlap' and 'Threshold' the same)
    -Apply Cuts 
    -You should now have 10 segments of the original corpus
================================================================================
STEP3: Generate statistics
    -Go to Analyze>Statistics
    -Change the Tokenize options to 'by Characters'
    -Generate Statistics

You should now see a data table that contains the document name for each segment
with the corresponding Number of Distinct Terms, Number of Words Occurring Once,
Total Term Count, and Average(raw counts). See the ResultsToExpect for a correctly
generated example. 

    
JLA 6/30/15
