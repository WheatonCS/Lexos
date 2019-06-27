# Lines/Segment

In this function the segments are divided based on the number of lines per segment (counted by each new line character). 


*Test Files:* Sentences.txt, dog_cat.txt

*Result Folders:* ResultFiles_Sentences_1, ResultFiles_Sentences_2
ResultFiles_dog_cat



## Test file: Sentences.txt

0. UPLOAD Sentences.txt

1. CUT: 

	- Select Lines/Segment
	- Change the Segment Size to 3
	- Keep Overlap at 0
	- Keep Last Segment Size Threshold (%) at 50

Results:
- After the cut you should have 4 segments, three with 3 lines and one with 4 lines.
- ResultFiles_Sentences_1

## Test file: Sentences.txt

0. UPLOAD Sentences.txt

1. CUT: 

	- Select Lines/Segment
	- Change the Segment Size to 5
	- Change Overlap to 2
	- Keep Last Segment Size Threshold (%) at 50

Results:
- After the cut you should have 4 segments, three with 5 lines and one with 4 lines.
- ResultFiles_Sentences_2

## Test file: dog_cat.txt

0. UPLOAD dog_cat.txt

1. CUT: 

	- Select Lines/Segment
	- Change the Segment Size to 2
	- change Overlap to 1
	- Change Last Segment Size Threshold (%) to 15

Results:
- After the cut you should have 9 segments, all with 2 lines except last one.
- ResultFiles_dog_cat

