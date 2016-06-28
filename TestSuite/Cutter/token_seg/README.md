# Tokens/Segment

This function splits the text by the number of tokens(words) to be put into each segment.
In languages that don't have spaces between tokens (words), such as Chinese, the function counts the "tokens" where it finds spaces.

####Test file: alphaSpace.txt

0. UPLOAD alphaSpace.txt

1. CUT: 

	- Select Tokens/Segment
	- Change the Segment Size to 2
	- Keep Overlap at 0
	- Keep Last Segment Size Threshold (%) at 50

Results:
- After the cut you should have two abc's in 11 segments.

####Test file: alphaSpace.txt

0. UPLOAD alphaSpace.txt

1. CUT: 

	- Select Tokens/Segment
	- Change the Segment Size to 4
	- Keep Overlap at 2
	- Keep Last Segment Size Threshold (%) at 50

Results:
- After the cut you should have four abc's in 10 segments.

####Test file: randomCharactersSpaced.txt

0. UPLOAD randomCharactersSpaced.txt

1. CUT: 

	- Select Tokens/Segment
	- Change the Segment Size to 5
	- Keep Overlap at 1
	- Keep Last Segment Size Threshold (%) at 20

Results:
- After the cut you should have three segments, two with 5 tokens, one with three
(the spaces are hard to see between the characters in the preview).


