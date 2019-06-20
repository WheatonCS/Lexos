# Segment/Document

This function splits the text into a designated amount of segments with an even amount of tokens (words) in each segment.
If there is an uneven amount of words the remainder of the words will be spread out evenly starting with the first segment.
For languages that don't have spaces for words such as Chinese, this function will split it based on spaces found in the text.
i.e. BaJin_Autumn_1940.txt

*Test File:* BaJin_Autumn_1940.txt

*Result Folder:* ResultFiles_BaJin_Autumn_1940



## Test file: BaJin_Autumn_1940.txt

1. Upload BaJin_Autumn_1940.txt

2. Under the "Prepare" menu, select "Cut"

3. Set the cut mode to "Segments"

4. Set "Number of Segments" to 10

5. Click "Apply"

6. You should now have 10 documents, each a segment of the original, all equal in length

Results: ResultFiles_BaJin_Autumn_1940
