# Tokenizer

#### Test Tokenizer

*Test files:* file_one.txt, file_two.txt, file_three.txt, file_four.txt

*Result files:* byTokensandPropCounts.csv, byTokensandRawCounts.csv,
byCharactersandRawCounts.csv

### Tokenize by Tokens
##### Tokenize by Proportional Counts

1. Upload all files

2. Under the "Prepare" menu click "Tokenize"

3. Using the default settings then click generate 
    - Documents as columns, terms as rows
    - Tokenize by tokens
    - Normalize, proportional

Result: results_defaults.csv

##### Tokenize by Raw Counts

1. Upload all files

2. Under the "Prepare" menu click "Tokenize"

3. Using the following settings then click generate 
    - Documents as columns, terms as rows (default)
    - Tokenize by tokens (default)
    - Normalize, Raw Counts

Result: results_rawCounts.csv

##### Tokenize using Bi-Grams

1. Upload all files

2. Under the "Prepare" menu click "Tokenize"

3. Using the following settings then click generate 
    - Documents as columns, terms as rows (default)
    - Tokenize by tokens, grams: 2
    - Normalize, proportional (default)

Result: results_biGrams.csv

##### Tokenize by Weighted Counts (TF-IDF)

1. Upload all files

2. Under the "Prepare" menu click "Tokenize"

3. Using the following settings then click generate 
    - Documents as columns, terms as rows (default)
    - Tokenize by tokens (default)
    - Normalize, TF-IDF

Result: results_weighted.csv

### Tokenize by Characters
##### Tokenize by Raw Counts

1. Upload all files

2. Under the "Prepare" menu click "Tokenize"

3. Using the following settings then click generate 
    - Documents as rows, terms as columns
        - *Note* You will not be able to see this change on the website. To see
        the changes you need to download the table.
    - Tokenize by characters
    - Normalize, Raw Counts

Result: results_characters.csv
