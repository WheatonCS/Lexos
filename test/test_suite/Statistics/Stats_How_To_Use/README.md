# Stats How to Use

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

*Test file:* catCaterpillar.txt

*Result files:* catCaterpillar_Results_Table.csv, catCaterpillar_Results_Graph.png

1. Upload catCaterpillar.txt

2. Under the "Prepare" menu click "Scrub" and scrub using the default settings and click "Apply"
	- Remove Punctuation
	- Make Lowercase
	- Remove Digits
	
3. Under the "Prepare" menu click "Cut" 

4. Under "Cut Mode" select "Tokens"

5. Under "Cut Settings" change "Segment Size" to 10 (keep 'Overlap' and 'Threshold' as default)

6. Click "Apply"

7. You should now have 5 segments of the original corpus
	
8. Under the "Analyze" menu, click "Statistics"

9. Keep all settings as default and click "Generate"

### Test Two

*Test file:* Heart_of_Darkness.txt

*Result files:* HoD_Results_Table.csv, HoD_Results_Graph.png

1. Upload Heart_of_Darkness.txt

2. Under the "Prepare" menu click "Scrub" and scrub using the default settings and click "Apply"
	- Remove Punctuation
	- Make Lowercase
	- Remove Digits
	
3. Under the "Prepare" menu click "Cut" 

4. Under "Cut Mode" select "Segments"

5. Under "Cut Settings" change "Number of Segments" to 10 

6. Click "Apply"

7. You should now have 10 segments of the original corpus
	
8. Under the "Analyze" menu, click "Statistics"

9. Keep all settings as default and click "Generate"

### Test Three

*Test file:* DreamCH1.txt

*Result files:* DreamCH1_Results_Table.csv, DreamCH1_Results_Graph.png

1. Upload DreamCH1.txt

2. Under the "Prepare" menu click "Scrub" and scrub using the default settings and click "Apply"
	- Remove Punctuation
	- Make Lowercase
	- Remove Digits
	- Remove Spaces
	- Remove Tabs
	- Remove Newlines
	
3. Under the "Prepare" menu click "Cut" 

4. Under "Cut Mode" select "Characters"

5. Under "Cut Settings" change "Segment Size" to 650 (keep 'Overlap' and 'Threshold' as default)

6. Click "Apply"

7. You should now have 10 segments of the original corpus
	
8. Under the "Analyze" menu, click "Statistics"

9. Under "Tokenize" select "By Characters" and click "Generate"

### Test Four

*Test file:* HenryWP_ThePirate.txt

*Result files:* HenryWP_Results_Table.csv, HenryWP_Results_Graph.png

1. Upload HenryWP_ThePirate.txt

2. Under the "Prepare" menu click "Scrub" and scrub using the default settings and click "Apply"
	- Remove Punctuation
	- Make Lowercase
	- Remove Digits
	
3. Under the "Prepare" menu click "Cut" 

4. Under "Cut Mode" select "Lines"

5. Under "Cut Settings" change "Segment Size" to 10 (keep 'Overlap' and 'Threshold' as default)

6. Click "Apply"

7. You should now have 17 segments of the original corpus
	
8. Under the "Analyze" menu, click "Statistics"

9. Keep all settings as default and click "Generate"
