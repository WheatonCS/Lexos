# Lines/Segment

In this function the segments are divided based on the number of lines per segment (counted by each new line character). 

####Test file: Sentences.txt

0. UPLOAD Sentences.txt

1. CUT: 

	- Select Lines/Segment
	- Change the Segment Size to 3
	- Keep Overlap at 0
	- Keep Last Segment Size Threshold (%) at 50

Results:
- After the cut you should have 4 segments, three with 3 lines and one with 4 lines.

####Test file: Sentences.txt

0. UPLOAD Sentences.txt

1. CUT: 

	- Select Lines/Segment
	- Change the Segment Size to 5
	- Keep Overlap at 2
	- Keep Last Segment Size Threshold (%) at 50

Results:
- After the cut you should have 4 segments, three with 5 lines and one with 4 lines.

####Test file: dog_cat.txt

0. UPLOAD dog_cat.txt

1. CUT: 

	- Select Lines/Segment
	- Change the Segment Size to 2
	- Keep Overlap at 1
	- Keep Last Segment Size Threshold (%) at 15

Results:
- After the cut you should have 8 segments, all with 2 lines.

