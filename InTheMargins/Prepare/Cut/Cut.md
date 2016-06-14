# Cut

* [Overview](#overview)
* [Features](#features)
* [Issues/Questions](#issues)

## <a name='overview'></a> Overview
On this page you can cut your active documents in segments by number of characters, tokens, or lines. Documents can also be divided into a certain number of segments or by milestones.


## <a name='features'></a> Features

### Characters/Segment
1. Tool Tip:  
   None.
2. Tool Tip Extended:  
   By selecting characters per segment, you can cut your text into sections based on the number of characters(letters and spaces) you want in each section. 
3. Example:  
   None.   
4. Issue/Questions:  
   None.

### Tokens/Segment
1. Tool Tip:  
   None.
2. Tool Tip Extended:  
   By selecting tokens per segment, you can cut your text into sections based on the number of tokens you want in each section. A group of letters between two spaces or a new line and a space are counted as one token. 
3. Example:  
   None.
4. Issue/Questions:  
   None.

### Lines/Segment
1. Tool Tip:  
   None.
2. Tool Tip Extended:  
   By selecting lines per segment, you can cut your text into sections based on the number of lines you want in each section. A group of tokens before a new line character counts as one line.
3. Example:  
   None.
4. Issue/Questions:  
   None.

### Segments/Document
1. Tool Tip:  
   None.
2. Tool Tip Extended:  
   By selecting segments per document, you can cut your text into a selected number of sections. The number of tokens in the text are divided evenly into the number of segments selected. If the number of tokens isn't evenly divisible by the number of segments, then the remaining tokens will be split evenly starting from the first segment.
3. Example:  
   If you have a text with 22 tokens, and you select 5 segments per document, then the number of tokens in each segment from segment 1 to segment 5 is 5, 5, 4, 4, 4.
4. Issue/Questions:  
   None.

### Segment Size/Number of Segments
1. Tool Tip:  
    A positive integer used to divide up the text (e.g. either the number of letters, words, or lines per segment, or the number of segments per document).
2. Tool Tip Extended:  
   Segment size appears for Characters, Tokens, or Lines per Segment. Number of segments appears when Segments per Document is selected.
3. Example:  
   None.
4. Issue/Questions:  
   None.

### Overlap
1. Tool Tip:  
   Amount of overlapping content at segment bondaries (a number smaller than the overall size of the segment).
2. Tool Tip Extended:  
   The amount of overlap is the number of tokens repeated from the previous section to next section.
3. Example:  
   If the text, "The dog ran very far away." is split into 2 tokens per segment with 1 token overlap it would be split into 5 segments, "The dog", "dog ran", "ran very", "very far", and "far away."
4. Issue/Questions:  
   None.

### Last Segment Size Threshold
1. Tool Tip:  
   The value the last segment has to reach relative to the others in order to be considered a separate segment.
2. Tool Tip Extended:  
   
3. Example:  
   
4. Issue/Questions:  
   

### Cut by Milestone
1. Tool Tip:  
   Splits the document into segments at each appearance of the provided string. Child segments will not contain the Milestone delimiter.
2. Tool Tip Extended:  
   
3. Example:  
   
4. Issue/Questions:  

### Preview Cuts
1. Tool Tip:  
   
2. Tool Tip Extended:  
   
3. Example:  
   
4. Issue/Questions:  
   
### Apply Cuts
1. Tool Tip:  
   
2. Tool Tip Extended:  
   
3. Example:  
   
4. Issue/Questions:  
   
### Download Cut Files
1. Tool Tip:  
   
2. Tool Tip Extended:  
   
3. Example:  
   
4. Issue/Questions:  
   

## <a name='issues'></a> General Issues/Questions

