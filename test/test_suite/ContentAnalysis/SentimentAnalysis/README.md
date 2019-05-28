# Content Analysis Tool
### How to test Sentiment Analysis

*Files to use:* [Melville_MobyDick.txt](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/ContentAnalysis/SentimentAnalysis/FilesToUse/Melville_MobyDick.txt), [negative.txt](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/ContentAnalysis/SentimentAnalysis/FilesToUse/negative.txt), [positive.txt](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/ContentAnalysis/SentimentAnalysis/FilesToUse/positive.txt)

<!-- Moby Dick is not currently in the repo -->

*Expected Results:* [Result.pdf](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/ContentAnalysis/SentimentAnalysis/ResultsToExpect/Results.pdf)

****

**Follow the steps provided below to perform a sentiment analysis on Herman Melville's *Moby Dick***

1. From the [Upload page](http://lexos.wheatoncollege.edu/upload), select "Browse" and upload the provided file: Melville_MobyDick.txt

2. Under the "Prepare" menu, select "Scrub"

3. Apply scrubbing the document using default settings
    - Remove all Punctuation
    - Make Lowercase
    - Remove Digits

4. Under the "Analyze" menu, select "Content Analysis"

5. Select "Upload Files" under Dictionaries and select the two provided dictionary files: positive.txt, negative.txt

6. Using the calculator under Formula, set formula to **[positive] - [negative]**

7. To get your results, click "Analyze". The first table you see should be what is shown in the [Result.pdf](https://github.com/WheatonCS/Lexos/blob/master/test/test_suite/ContentAnalysis/SentimentAnalysis/ResultsToExpect/Results.pdf) file.

