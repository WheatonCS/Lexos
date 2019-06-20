# Scrubbing


A list of Unicode categories can be viewed from http://www.fileformat.info/info/unicode/category/index.htm

Order Of Implementations:

    1. lower
    2. special characters
    3. tags
    4. punctuation
    5. digits
    6. consolidations
    7. lemmatize
    8. stop words/keep words

### Function Descriptions

Ampersands:
- If this option is selected any ampersands are preserved. 

Apostrophes: 
- Only accessible once remove punctuation is selected
- If this option is selected any word internal apostrophes are preserved. 

Consolidations:
- Scrubber function should convert the first character under consolidations.txt to the second character. 

Digits:
- Digits folder includes all digits including Arabic language, Chinese, Roman Numerals, etc. 

Hyphens:
- Hyphens folder includes all hyphens in the Unicode category.
- For more references, please see the Unicode category under [Pc] and [Pd].

Lemma:
- lemmas.txt contains all the testing characters that we want to convert. Scrubber function will convert the first character to the second character separated with ','.

Lower:
- 'Lower' text files should be converted to all lower case. 

Punctuation:
- Punctuation test files are under [Pc], [Pd], [Pe], [Pf],[Pi], [Po], [Ps] in the unicode category. 

Special Characters:
- Designed for users' folder. 

StopWords & KeepWords:
- Scrubber should remove all the stopwords under the stopwords.txt file
- After scrubbing, all the words under stopwords.txt will be removed. 

Tags:
- Tags will be removed if we click "Remove Tags" option. 

*See additional explanations for each of the files inside of each of the directories.*
