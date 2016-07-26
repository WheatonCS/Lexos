# Topwords

* [Overview](#overview)
* [Features](#features)
* [Issues/Questions](#issues)

## <a name='overview'></a> Overview
Topword identifies tokens that appear with unique proportions when compared to other collections using a proportional z-test. A larger positive z-score indicates a token in this document or class is used more frequently than in the comparison group and a larger negative z-score indicates a relatively rarely used token.



## <a name='features'></a> Features

## Method for Test
   Selected option becomes the title above the topwords tables.
### Compare each document to all the documents as a whole
1. __Tool Tip:__  
   Comparing the proportion of each word in a document to that in all the documents as a whole. Example: Find Top Words in every chapter in one book.
2. __Tool Tip Extended:__  
   Always an option.
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Compare document against other class(es)
1. __Tool Tip:__  
   Comparing the proportion of each word in a document in one class to that in another class as a whole. Example: Having two books, find Top Words in every chapter from one of the books comparing to the other book.
2. __Tool Tip Extended:__  
   Only an option when documents are put into classes.
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Compare all the classes
1. __Tool Tip:__  
   Comparing the proportion of each word in one class to that in another class. Example: Find Top Words between two books with multiple chapters.
2. __Tool Tip Extended:__  
   Only an option when documents are put into classes. 
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
## Advanced Culling
1. __Tool Tip:__  
   More ways to cull the potential Top Words. Note: Culling will limit the amount of Top Words, but it is a favorable and crucial step.
2. __Tool Tip Extended:__  

3. __Example:__  
   
4. __Issue/Questions:__  

### All
1. __Tool Tip:__  
   Compare every single word.
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   

### Built-in Options
#### Standard Deviation
1. __Tool Tip:__  
   Cull outliers by the standard deviation from the mean on a normal distribution (bell-shaped curve) of frequencies of all words.
   * Use Top Outlier Only: Only compare words with rather high frequencies. 2 standard deviations above mean.  
   * Use Non Outlier Only: Only compare words with not too high or too low frequencies. Within 2 standard deviations from Mean.  
   * Use Low Outlier Only: Only compare words with rather low frequencies. 2 standard deviations below mean.  
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   

#### Interquartile Range (IQR)
1. __Tool Tip:__  
   Cull outliers by comparing to the interquartile range. The common way to find outliers in statistics. Note: sometimes there is no outliers on one side or both sides, when the data are skewed or compact.  
   * Use Top Outlier Only: Only compare words with unusually high frequencies which are at least 1.5 interquartile ranges above the third quartile (Q3).  
   * Use Non Outlier Only: Only compare words that are not outliers, whose frequencies are 1.5 interquartile ranges below the third quartile (Q3) and 1.5 interquartile ranges above the first quartile (Q1).  
   * Use Low Outlier Only: Only compare words with unusually low frequencies which are at least 1.5 interquartile ranges below the first quartile (Q1).  
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   
###Customize
1. __Tool Tip:__  
   Only Compare words within frequencies or row counts as inputted.
   * Proportional Counts: Word Frequencies  
   * Raw Counts: none
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   

### Get Topwords
1. __Tool Tip:__  
   
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   explain what topwords shows/does
   
### Download Matrix
1. __Tool Tip:__  
   
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   what is being downloaded in what format?
   

## <a name='issues'></a> General Issues/Questions
Tokenize options are not described on this page
