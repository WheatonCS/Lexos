# Segment/Document

This function splits the text into a designated amount of segments with the an even amount of tokens (words) in each segment.
If there is an uneven amount of words the remainder of the words will be spread out evenly starting with the first segment.
For languages that don't have spaces for words such as Chinese, this function will split it based on spaces found in the text.
i.e. BaJin_Autumn_1940.txt
