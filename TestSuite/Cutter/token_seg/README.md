# Tokens/Segment

This function splits the text by the number of tokens(words) to be put into each segment.
In languages that don't have spaces between tokens (words), such as Chinese, the function counts the "tokens" where it finds spaces.
=====================================
Test: alphaSpace.txt
=====================================
0) Select Tokens/Segment
1) Segment Size: 2
2) Overlap: 0
3) Last Seg Threshold: 50%
Result: Two abc's in 11 segments

====================================
Test: alphaSpace.txt
====================================
0) Select Tokens/Segment
1) Segment Size: 4
2) Overlap: 2
3) Last Seg Threshold: 50%
Result: Four abc's in 10 segments

===================================
Test: randomCharactersSpaced.txt
===================================
0) Do not scrub
1) Select Tokens/Segment
2) Segment Size: 5
3) Overlap: 1
4) Last Seg Threshold: 20%
Result: Three segments, two with 5 tokens, one with three
(the spaces are hard to see between the characters in the preview)


