The cutter is a powerful tool to break up a text into different "chunks". 
A chunk is a segment of the original text as tokenized by a letter 
(character n-gram) or word (word n-gram) size that is
determined by the user's choices on the cutter page.

Lexos allows the user to choose between 4 different cutting operations:

(A) Letters/Chunk - Letters per chunk divides the corpus into chunks with a specific
number of letters per chunk. (Note that for non-western languages, characters
are a better label than “letters”)

(B) Words/Chunk - Words per chunks divides a text into chunks containing
a set number of words in each of the chunks.

(C) Lines/Chunk - Lines per chunk divides a text into chunks with a specific
number of lines per chunk.

(D) Chunks/File - Chunks per file divides the corpus into as many chunks as the user
specifies.   

Cutting a file using Letters/Chunk:
=====================================================================
(0) UPLOAD numbered.txt
=====================================================================
(1) CUT: 
    (a) Select Letter/Chunk
    (b) Change the Chunk Size to 3
    (c) Keep Overlap at 0
    (d) Keep Last Chunk Size Threshhold (%) at 50

    Results
=====================================================================
    After the cut you should have 16 different chunks containing 2-3 letters 
    each. 
    



Cutting a file using Letters/Chunk with Overlap:
=====================================================================
(0) UPLOAD numbered.txt
=====================================================================
(1) CUT: 
    (a) Select Letter/Chunk
    (b) Change the Chunk Size to 5
    (c) Change Overlap to 3
    (d) Keep Last Chunk Size Threshhold (%) at 50

    Results
=====================================================================
    After the cut you should have 23 different chunks containing 3-5 letters 
    each. 


ja - June 8, 2015


