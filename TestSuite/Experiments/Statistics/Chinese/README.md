# STATS for Mandarin

This is an example of using the statistics page to determine statistical
information of each document in Mandarin.  
You should finally get a data table that contains 
- the document name for each segment
- the Number of Distinct Terms
- the Number of Words Occurring Once
- the Total Term Count
- the Average Term Frequency (Total Term Count / Number of Distinct Terms). 


**File #1: DreamCH1.txt**

0. Upload DreamCH1.txt

1. Scrub using the default settings.

	- Remove all Punct
	- Make Lowercase
	- Remove Digits
	- Apply Scrubbing
2. Cut the file

	- Select 'Characters/Segment'
	- Change the 'Segment Size' to 700 (keep 'Overlap' and 'Threshold' the same)
	- Apply Cuts 
	- You should now have 10 segments of the original corpus
3. Generate statistics

	- Go to Analyze>Statistics
	- Change the Tokenize options to 'by Characters'
	- Generate Statistics

You should now see a data table that contains the document name for each segment
with the corresponding Number of Distinct Terms, Number of Words Occurring Once,
Total Term Count, and Average Term Frequency. See the png Dream_Results for 
a correctly generated example. 

