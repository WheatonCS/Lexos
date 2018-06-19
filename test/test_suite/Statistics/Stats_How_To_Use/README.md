# STATS for English and Mandarin

=======================================================================================

This part is an example of using the statistics page to determine statistical
information about each document in English.  

You should get a data table that contains:
- the document name for each segment
- the Number of Distinct Terms
- the Number of Words Occurring Once
- the Total Term Count
- the Average Term Frequency (Total Term Count / Number of Distinct Terms) 


*Test file:* catCaterpillar.txt

*Result file:* catCaterpillar_Results.pdf, catCaterpillar_Results.png

1. Upload catCaterpillar.txt

2. Scrub using the default settings
	- Remove all Punct
	- Make Lowercase
	- Remove Digits
	- Apply Scrubbing
	
3. Cut the file
	- Select 'Segments/Document'
	- Change the 'Number of Segments' to 10
	- Apply Cuts 
	- You should now have 10 segments of the original corpus
	
3. Generate statistics
	- Go to Analyze->Statistics
	- Do not change any options 
	- Generate Statistics



This part is an example of using the statistics page to determine statistical
information of each document in Mandarin.  
You should finally get a data table that contains 
- the document name for each segment
- the Number of Distinct Terms
- the Number of Words Occurring Once
- the Total Term Count
- the Average Term Frequency (Total Term Count / Number of Distinct Terms). 


**File #1: DreamCH1.txt**

0. Upload DreamCH1.txt(can be found in folder Lexos/TestSuite/Statistics/Stats_Compare/FilesToUse)

1. Scrub using the following settings.

	- Remove all Punct
	- Make Lowercase
	- Remove Digits
	- Remove White Space
	- Apply Scrubbing
2. Cut the file

	- Select 'Characters/Segment'
	- Change the 'Segment Size' to 650 (keep 'Overlap' and 'Threshold' as default)
	- Apply Cuts 
	- You should now have 10 segments of the original corpus
3. Generate statistics

	- Go to Analyze->Statistics
	- Change the Tokenize options to 'by Characters'
	- Generate Statistics

You should now see a data table that contains the document name for each segment
with the corresponding Number of Distinct Terms, Number of Words Occurring Once,
Total Term Count, and Average Term Frequency. 
See the png DreamCH1_Results for a correctly generated example. 

