# Content Analysis Tool
### How to test Sentiment Analysis

*Files to use:* Melville_MobyDick.txt, negative.txt, positive.txt

Positive and negative sourced dictionaries sourced from these papers:

   Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." 
       Proceedings of the ACM SIGKDD International Conference on Knowledge 
       Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, 
       Washington, USA.
       
   Bing Liu, Minqing Hu and Junsheng Cheng. "Opinion Observer: Analyzing 
       and Comparing Opinions on the Web." Proceedings of the 14th 
       International World Wide Web conference (WWW-2005), May 10-14, 
       2005, Chiba, Japan.

The dictionaries are distributed with the following disclaimer:

The appearance of an opinion word in a sentence does not necessarily mean that
the sentence expresses a positive or negative opinion. 
See the paper below:

Bing Liu. "Sentiment Analysis and Subjectivity." An chapter in 
    Handbook of Natural Language Processing, Second Edition, 
    (editors: N. Indurkhya and F. J. Damerau), 2010.
    
    
    
The Lexomics Research Group does not necessarily endorse the content of these
dictionaries; a discussion of the inclusion of certain words here may be meaningful
as you use this tool or construct your own dictionaries.

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
