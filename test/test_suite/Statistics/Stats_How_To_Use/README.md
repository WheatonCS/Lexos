# Statistics

#### Test Statistics for English and Mandarin 

You should get:
- A scatter plot of the Total Term Count for each segment
- A box plot of the Total Term Count for all of the segments
- A data table that contains:
    - the document name for each segment
    - the Number of Distinct Terms
    - the Number of Words Occurring Once
    - the Total Term Count
    - the Average Term Frequency (Total Term Count / Number of Distinct Terms)
- Corpus Statistics that contains:
    - the average document size
    - the standard deviation of document sizes
    - the Interquartile range of document sizes
    - any anomaly detected by the standard error test
    - any anomaly detected by the interquartile range test

### Test One

*Test file:* [catCaterpillar.txt](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/FilesToUse/catCaterpillar.txt)

*Result files:* [catCaterpillarResults.pdf](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/ResultsToExpect/catCaterpillarResults.pdf), [catCaterpillarResults.png](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/ResultsToExpect/catCaterpillarResults.png)

1. Upload catCaterpillar.txt

2. Scrub using the default settings
	- Remove all Punctuation
	- Make Lowercase
	- Remove Digits
	- Apply Scrubbing
	
3. Cut the file
	- Select 'Tokens/Segment'
	- Change the 'Segment Size' to 10 (keep 'Overlap' and 'Threshold' as default)
	- Apply Cuts 
	- You should now have 5 segments of the original corpus
	
4. Generate statistics
	- Go to Analyze->Statistics
	- Tokenize by Tokens 
	- Generate Statistics

### Test Two

*Test file:* [Heart_of_Darkness.txt](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/FilesToUse/Heart_of_Darkness.txt)

*Result files:* [HoD_Results.pdf](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/ResultsToExpect/HoD_Results.pdf), [HoD_Results.png](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/ResultsToExpect/HoD_Results.png)

1. Upload Heart_of_Darkness.txt

2. Scrub using the default settings
	- Remove all Punctuation
	- Make Lowercase
	- Remove Digits
	- Apply Scrubbing
	
3. Cut the file
	- Select 'Segments/Document'
	- Change the 'Segment Size' to 10
	- Apply Cuts 
	- You should now have 10 segments of the original corpus
	
4. Generate statistics
	- Go to Analyze->Statistics
	- Tokenize by Tokens 
	- Generate Statistics


### Test Three

*Test file:* [DreamCH1.txt](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/FilesToUse/DreamCH1.txt)

*Result files:* [DreamCH1_Results.pdf](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/ResultsToExpect/DreamCH1_Results.pdf), [DreamCH1_Results.png](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/ResultsToExpect/DreamCH1_Results.png)

1. Upload DreamCH1.txt

2. Scrub using the following settings
	- Remove all Punctuation
	- Make Lowercase
	- Remove Digits
	- Remove White Space
	- Apply Scrubbing
	
3. Cut the file
	- Select 'Characters/Segment'
	- Change the 'Segment Size' to 650 (keep 'Overlap' and 'Threshold' as default)
	- Apply Cuts 
	- You should now have 10 segments of the original corpus
	
4. Generate statistics
	- Go to Analyze->Statistics
	- Tokenize by Characters
	- Generate Statistics

### Test Four

*Test file:* [HenryWP_ThePirate.txt](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/FilesToUse/HenryWP_ThePirate.txt)

*Result files:* [HenryWP_Results.pdf](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/ResultsToExpect/HenryWP_Results.pdf), [HenryWP_Results.png](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/ResultsToExpect/HenryWP_Results.png)

1. Upload HenryWP_ThePirate.txt

2. Scrub using the default settings
	- Remove all Punctuation
	- Make Lowercase
	- Remove Digits
	- Apply Scrubbing
	
3. Cut the file
	- Select 'Lines/Segment'
	- Change the 'Segment Size' to 10 (keep 'Overlap' and 'Threshold' as default)
	- Apply Cuts 
	- You should now have 16 segments of the original corpus
	
4. Generate statistics
	- Go to Analyze->Statistics
	- Change the Tokenize options to 'by Characters'
	- Generate Statistics
