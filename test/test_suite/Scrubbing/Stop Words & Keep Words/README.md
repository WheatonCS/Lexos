Stop Words & Keep Words
==========


## Lexos Provided Stop Words

1. Upload files you wish to remove stop words

2. Scrub: 
    - Select your desired scrub settings

3. Under "Stop/Keep Words" select "Stop" and upload the provided file
    - **NLTK_English_stopwords.txt**
    
4. Click "Apply"

#### Test Stop Words & Keep Words

*Test files:* sw_kw_text.txt, sw_kw_words.txt

*Result files:* kw_experimentResults.txt, sw_experimentResults.txt

1. Upload: 
    - Upload sw_kw_text.txt

2. Scrub: 
    - Select Remove All Punctuation
    - Select Make Lowercase
    - Select Remove Digits
    - Stop Words/Keep Words: select either option and upload sw_kw_words.txt
    
3. Results:
    - File should contain *only* the keep words, or *everything but* the stop words.
    - See ResultsToExpect


