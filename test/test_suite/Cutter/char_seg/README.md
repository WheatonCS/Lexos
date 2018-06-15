# Characters/Segment

This function cuts the text into segments based on the number of characters in each segment.

*Test Files:*  1_alpha.txt, 2_numbered.txt, 3_numbered_large.txt
*Result Files:*  


## Test file: 1_alpha.txt

0. UPLOAD 1_alpha.txt

1. CUT: 

	- Select Characters/Segment
	- Change the Segment Size to 10
	- Change Overlap to 3
	- Keep Last Segment Size Threshold (%) at 50

Results:
- After the cut you should have 13 different segments containing 10 characters 
each with an overlap of 3 characters. 


## Test file: 2_numbered.txt

0. UPLOAD 2_numbered.txt

1. CUT: 

	- Select Characters/Segment
	- Change the Segment Size to 3
	- Keep Overlap at 0
	- Keep Last Segment Size Threshold (%) at 50

Results:
- After the cut you should have 16 different segments containing 2-3 characters each. 


## Test file: 3_numbered_large.txt

0. UPLOAD 3_numbered_large.txt

1. CUT: 

	- Select Characters/Segment
	- Change the Segment Size to 100
	- Keep Overlap at 0
	- Keep Last Segment Size Threshold (%) at 50

Results:
- After the cut you should have 5 different segments containing 100 characters 
except for the last one which is shorter


## Test file: 4_randomCharacters.txt

0. UPLOAD 4_randomCharacters.txt

1. CUT: 

	- Select Characters/Segment
	- Change the Segment Size to 5
	- Change Overlap at 2
	- Keep Last Segment Size Threshold (%) at 50

Results:
- After the cut you should have 20 different segments containing 5 characters 
except for the last one which is shorter, overlapping by 2

