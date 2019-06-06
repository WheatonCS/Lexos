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
    - the interquartile range of document sizes
    - any anomaly detected by the standard error test
    - any anomaly detected by the interquartile range test

### Test One

*Test file:* [catCaterpillar.txt](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/FilesToUse/catCaterpillar.txt)

*Result files:* [catCaterpillar_Results_Table.pdf](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/ResultsToExpect/catCaterpillar_Results_Table.pdf), [catCaterpillar_Results_Graph.png](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/ResultsToExpect/catCaterpillar_Results_Graph.png)

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

*Result files:* [HoD_Results_Table.pdf](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/ResultsToExpect/HoD_Results_Table.pdf), [HoD_Results_Graph.png](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/ResultsToExpect/HoD_Results_Graph.png)

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

*Result files:* [DreamCH1_Results_Table.pdf](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/ResultsToExpect/DreamCH1_Results_Table.pdf), [DreamCH1_Results_Graph.png](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/ResultsToExpect/DreamCH1_Results_Grapj.png)

1. Upload DreamCH1.txt

2. Scrub using the following settings
	- Remove all Punctuation
	- Make Lowercase
	- Remove Digits
	- Remove Whitespace
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

*Result files:* [HenryWP_Results_Table.pdf](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/ResultsToExpect/HenryWP_Results_Table.pdf), [HenryWP_Results_Graph.png](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/Statistics/Stats_How_To_Use/ResultsToExpect/HenryWP_Results_Graph.png)

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
	- You should now have 17 segments of the original corpus
	
4. Generate statistics
	- Go to Analyze->Statistics
	- Tokenize by Tokens 
	- Generate Statistics
