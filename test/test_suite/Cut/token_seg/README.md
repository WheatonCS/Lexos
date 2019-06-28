# Tokens/Segment

This function splits the text by the number of tokens(words) to be put into each segment.
In languages that don't have spaces between tokens(words), such as Chinese, the 
function counts the "tokens" where it finds spaces.

*Test Files:* alphaSpace.txt, randomCharactersSpaced.txt

*Result Folder:* ResultFiles_alphaSpace_1, ResultFiles_alphaSpace_2, 
ResultFiles_randomCharactersSpaced

## Test file: alphaSpace.txt

1. Upload alphaSpace.txt

2. Under the "Prepare" menu, select "Cut"

3. Set the cut mode to "Tokens"

4. Set the "Segment Size" to 2

5. Keep "Overlap" at 0

6. Keep Merge % as the default

7. Click "Apply"

8. You should now have 11 documents, each a segment of the original containing two abc's each.

Results: ResultFiles_alphaSpace_1

## Test file: alphaSpace.txt

1. Upload alphaSpace.txt

2. Under the "Prepare" menu, select "Cut"

3. Set the cut mode to "Tokens"

4. Set the "Segment Size" to 4

5. Change "Overlap" to 2

6. Keep Merge % as the default

7. Click "Apply"

8. After the cut you should have 11 documents, each a segment of the original 
containing four abc's each except the last segment which should contain two abc's.

Results: ResultFiles_alphaSpace_2

## Test file: randomCharactersSpaced.txt

1. Upload randomCharactersSpaced.txt

2. Under the "Prepare" menu, select "Cut"

3. Set the cut mode to "Tokens"

4. Set the "Segment Size" to 5

5. Change "Overlap" to 1

6. Change Merge % to 20

7. Click "Apply"

8. After the cut you should have three segments, two with 5 tokens, one with three
(the spaces are hard to see between the characters in the preview).

Results: ResultFiles_randomCharactersSpaced


