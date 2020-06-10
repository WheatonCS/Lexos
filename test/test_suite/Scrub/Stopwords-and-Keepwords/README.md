Stop Words & Keep Words
==========

There is no "correct" list of stop words for a given set of texts, although some standard list of stop words are available. Some places to start looking are [Stop words for 50 languages](https://github.com/6/stopwords-json), and for historical languages, the [Classical Language Toolkit (CLTK) project](https://github.com/cltk/cltk/tree/master/cltk/stop). Lexos provides a copy of the NLTK English stop words list.

Another important source of information on stop words and their use is [Stop Word Lists in Free Open-source Software Packages (Yothman, Qin, Yurchak 2018)](https://aclweb.org/anthology/W18-2502).

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


