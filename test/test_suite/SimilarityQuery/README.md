# Similarity Query

#### Test Similarity Query

*Test files:* Chapter64.txt, Chapter67.txt, First80_without_64AND67.txt, First80Chapters.txt, Late40Chapters.txt

*Result file:* similarity-query-result.csv

Use the similarity query to find out how close Chapter 67 
is to all the other Chapters in the book.

1. UPLOAD all files 

2. Scrub using default settings

3. Similarity Query Rankings

    - Click Chapter67 which is use to compare with all other files
    - Token Type = by Characters 1 gram
    - Deselect the Remove words that only appear once option (optional)


The module used to produce this ranking employs Latent Semantic Analysis to 
generate unique vectors for each document. The cosine angle between your 
comparison document's vector and the vector of each document of your corpus is 
calculated and these values are then compared. Cosine similarity measures are
between 0 and 1. The lower the value the closer the comparison document's 
vector is to that document's vector as opposed to the other documents' vectors.

The ordering, from least similar to most similar, is Chapter64, First80_without, 
First80Chapters, and finally Late40Chapters

### NOTE ### 
    - The current PDF is not only WRONG but is also OUT OF DATE with the new UI
