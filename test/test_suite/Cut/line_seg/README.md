# Lines/Segment

In this function, the segments are divided based on the number of lines per segment 
(counted by each new line character). 


*Test Files:* Sentences.txt, dog_cat.txt

*Result Folders:* ResultFiles_Sentences_1, ResultFiles_Sentences_2
ResultFiles_dog_cat



## Test file: Sentences.txt
1. Upload Sentences.txt

2. Under the "Prepare" menu, select "Cut"

3. Set the cut mode to "Lines"

4. Set the "Segment Size" to 3

5. Keep "Overlap" at 0

6. Keep Merge % as the default

7. Click "Apply"

8. You should now have 4 documents, each a segment of the original, three with 3
 lines and one with 4 lines.

Results: ResultFiles_Sentences_1

## Test file: Sentences.txt

1. Upload Sentences.txt

2. Under the "Prepare" menu, select "Cut"

3. Set the cut mode to "Lines"

4. Set the "Segment Size" to 5

5. Change "Overlap" to 2

6. Keep Merge % as the default

7. Click "Apply"

8. You should now have 4 documents, each a segment of the original, three with 5 
lines and one with 4 lines.

Results: ResultFiles_Sentences_2

## Test file: dog_cat.txt

1. Upload dog_cat.txt

2. Under the "Prepare" menu, select "Cut"

3. Set the cut mode to "Lines"

4. Set the "Segment Size" to 2

5. Change "Overlap" to 1

6. Change Merge % to 15

7. Click "Apply"

8. You should now have 9 documents, each a segment of the original, all with 2 lines 
except the last one.

Results: ResultFiles_dog_cat
