File to use: heart_of_darkness.txt

This is an example of using the statistics page to determine statistical
information about segments of an entire corpus.   

================================================================================
STEP0: Upload heart_of_darkness.txt
================================================================================
STEP1: Scrub using the default settings.
    -Remove all Punct
    -Make Lowercase
    -Remove Digits
    -Apply Scrubbing
================================================================================
STEP2: Cut the file
    -Select 'Segments/Document'
    -Change the 'Number of Segments' to 10
    -Apply Cuts 
    -You should now have 10 segments of the original corpus
================================================================================
STEP3: Generate statistics
    -Go to Analyze>Statistics
    -Do not change any options (the default for 'Select a File' should already
    have selected the 10 segments)
    -Generate Statistics

You should now see a data table that contains the document name for each segment
with the corresponding Number of Distinct Terms, Number of Words Occurring Once,
Total Term Count, and Average(raw counts). See the ResultsToExpect for a correctly
generated example. 

    
JLA 6/30/15
