# Similarity Query

#### Test Similarity Query

*Test files:* Chapter64.txt, Chapter67.txt, First80_without_64AND67.txt, First80Chapters.txt, Late40Chapters.txt

*Result file:* similarity-query-result.csv

Use the similarity query to find out how close Chapter 67 
is to all the other Chapters in the book.

1. Upload all files 

2. Under the "Prepare" menu, go to the "Scrub" page, and using the default settings, click "Apply"
    - Make Lowercase
    - Remove Digits
    - Remove Punctuation

3. Under the "Analyze" menu, go to the "Similarity Query" page

4. In the "Comparison Document" section, click "Select" and use "Chapter67" as the comparison document.

5. Under "Tokenize" select "By Characters"

6. Click "Generate". 

Expected Results are in the file: similarity-query-result.csv. 

The module used to produce this ranking employs Latent Semantic Analysis to 
generate unique vectors for each document. The cosine angle between your 
comparison document's vector and the vector of each document of your corpus is 
calculated and these values are then compared. Cosine similarity measures are
between 0 and 1. The lower the value the closer the comparison document's 
vector is to that document's vector as opposed to the other documents' vectors.

The ordering, from least similar to most similar, is Chapter64, First80_without_64AND67, 
First80Chapters, and finally Late40Chapters
