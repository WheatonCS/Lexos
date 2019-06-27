# Content Analysis Tool
### How to test Sentiment Analysis

*Files to use:* Melville_MobyDick.txt, negative.txt, positive.txt


*Expected Results:* Result.pdf

****

**Follow the steps provided below to perform a sentiment analysis on Herman Melville's *Moby Dick***

1. Upload Melville_MobyDick.txt

2. Scrubbing has already been applied using the default settings
    - Remove Punctuation
    - Make Lowercase
    - Remove Digits

3. Under the "Analyze" menu, select "Content Analysis"

4. Select "Upload Files" under Dictionaries and select the two provided dictionary files: positive.txt, negative.txt

5. Using the calculator under Formula, set formula to **[positive] - [negative]**

6. To get your results, click "Analyze". The first table you see should be what is shown in the ResultsToExpect folder
