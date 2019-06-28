# Milestones

Milestones are used to split the text at designated spots such as chapters. 
Words that are used in the .txt shouldn't be used as milestones.
As seen in the testing of catBobcat.txt and catCaterpillar.txt, if the word cat is
 used as a milestone every instance of it concatenated or not is removed.

*Test Files:* catCaterpillar.txt, catBobcat.txt

*Result Folders:* ResultFiles_catBobcat, ResultFiles_catCaterpillar



## Test file: catBobcat.txt

1. Upload catBobcat.txt

2. Under the "Prepare" menu, select "Cut"

3. Set the cut mode to "Milestones"

4. Set the "Milestone" to "cat"

5. Click "Apply"

6. You should now have 10 documents, each a segment of the original, cut on the string
"cat"

Results: ResultFiles_catBobcat


## Test file: catCaterpillar.txt

1. Upload catCaterpillar.txt

2. Under the "Prepare" menu, select "Cut"

3. Set the cut mode to "Milestones"

4. Set the "Milestone" to " cat " (cat surrounded by spaces)

5. Click "Apply"

6. You should now have 5 documents, each a segment of the original, cut on the string " cat " 
(caterpillar should be intact)

Results: ResultFiles_catCaterpillar
