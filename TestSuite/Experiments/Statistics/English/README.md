# STATS for English

This is an example of using the statistics page to determine statistical
information of each document in English.  
You should finally get a data table that contains 
- the document name for each segment
- the Number of Distinct Terms
- the Number of Words Occurring Once
- the Total Term Count
- the Average Term Frequency (Total Term Count / Number of Distinct Terms). 


**File #1: heart_of_darkness.txt**

0. Upload heart_of_darkness.txt
1. Scrub using the default settings.
- Remove all Punct
- Make Lowercase
- Remove Digits
- Apply Scrubbing
2. Cut the file
- Select 'Segments/Document'
- Change the 'Number of Segments' to 10
- Apply Cuts 
- You should now have 10 segments of the original corpus
3. Generate statistics
- Go to Analyze>Statistics
- Do not change any options (the default for 'Select a File' should already have selected the 10 segments)
- Generate Statistics

See the png HoD_Results for a correctly generated example.



**File #2: catCaterpillar.txt**

0. Upload catCaterpillar.txt
STEP1: Scrub using the default settings.
1. Scrub using the default settings.
- Remove all Punct
- Make Lowercase
- Remove Digits
- Apply Scrubbing
2. Cut the file
- Select 'Tokens/Segment'
- Change the 'Segment Size' to 10
- Apply Cuts 
- You should now have 5 segments of the original corpus
3. Generate statistics
- Go to Analyze>Statistics
- Do not change any options (the default for 'Select a File' should already have selected the 10 segments)
- Generate Statistics

See the png catCaterpillar_Results for a correctly generated example.