# Milestones

Milestones are used to split the text at designated spots such as chapters. 
Words that are used in the .txt shouldn't be used as milestones.
As seen in testing of catBobcat.txt and catCaterpillar.txt, if the word cat is used as a milestone every instance of it concatenated or not is removed.

*Test Files:* catCaterpillar.txt, catBobcat.txt

*Result Folders:* ResultFiles_catBobcat, ResultFiles_catCaterpillar



## Test file: catBobcat.txt

0. UPLOAD catBobcat.txt

1. CUT: 

	- Select Cut by Milestones
	- Type in "cat"

Results:
- After the cut you should have 10 segments, cut on the string "cat"
- ResultFiles_catBobcat



## Test file: catCaterpillar.txt

0. UPLOAD catCaterpillar.txt

1. CUT: 

	- Select Cut by Milestones
	- Type in " cat " (cat surrounded by spaces)

Results:
- After the cut you should have 5 segments, cut on the string " cat " 
(caterpillar should be intact)
- ResultFiles_catCaterpillar
