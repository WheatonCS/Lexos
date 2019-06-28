# Classical Chinese (Including Consolidations) - 鸿门宴_通假字ChineseConsolidations

Most classical Chinese texts include 通假字 (phonetic loan characters), which
can be replaced with several characters for the understanding purpose. Using
the consolidations option in scrubbing in Lexos, they can be easily replaced
with desired characters when being studied.

Specific file used here:
鸿门宴HongMenYan.txt

Using the tools from:   http://lexos.wheatoncollege.edu
and the files found in the FilesToUse/ directory, you should
be able to reproduce the file shown in ResultsToExpect/.

Steps:
=====================================================================
(0) UPLOAD:

    鸿门宴HongMenYan.txt

(1) SCRUB:

    (a) Remove Punctuation
    (b) Remove Digits
    (c) Consolidations - Upload the Chinese_consolidations.txt file
    
    Apply Scrubbing
To compare the two files, you can:

    Download Scrubbed Files for a manual compare.
OR

    (a) Upload 鸿门宴HongMenYan_without_consolidations.txt in the ResultsToExpect folder
    (b) Go to Analyze - Similarity Query
    (c) Tokenize - by Characters
    
    Get Similarity Rankings: the two files should be identical and should have a
    similarity score of 0.

ms - June 27, 2019
mjl - May 20, 2019
jg - June 10, 2014
