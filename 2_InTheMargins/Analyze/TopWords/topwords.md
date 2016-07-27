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
   Comparing the proportion of each token in a document to that token in all the documents as a whole. Example: Find topwords for one chapter compared to the entire book.
2. __Tool Tip Extended:__  
   Always an option.
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Compare document against other class(es)
1. __Tool Tip:__  
   Comparing the proportion of each token in a document in one class to that in another class as a whole. Example: With two books (two classes), find topwords in every chapter (document) from one of the books compared to the entire other book (class).
2. __Tool Tip Extended:__  
   Only an option when documents are put into classes.
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Compare all the classes
1. __Tool Tip:__  
   Comparing the proportion of each token in one class to that in another class. Example: Find topwords between two books (classes).
2. __Tool Tip Extended:__  
   Only an option when documents are put into classes. 
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
## Use These Terms
1. __Tool Tip:__  
 More ways to reduce the potential list of topwords. Use these options (and/or Tokenize Culling Options) to limit the number of topwords. 
2. __Tool Tip Extended:__  

3. __Example:__  
   
4. __Issue/Questions:__  

### All
1. __Tool Tip:__  
Use all terms that appear in both groups.
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   

### Built-in Options
#### Standard Deviation
1. __Tool Tip:__  
Built-in Options: Choose to find topwords using samples of term proportions from built-in outlier ranges.
  1. Standard Deviation: Choose outlier region: all defined by the standard deviation from the mean on a normal distribution (bell-shaped curve) of frequencies of all terms.
    * Only compare terms with rather high frequencies: +2&#963; standard deviations above the mean.
    * Only compare terms with mid-range frequencies: frequences within +/-1&#963; around the mean.
    * Only compare terms with rather low frequencies: +2&#963; standard deviations below the mean.
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   

#### Interquartile Range
1. __Tool Tip:__  
   Choose to find topwords using samples of term proportions using the InterQuartile Range (IQR).
   * Use Top Outlier Only: Only compare terms with unusually high frequencies which are at least 1.5 interquartile ranges above the third quartile (Q3).  
   * Use Non Outlier Only: Only compare terms that are not outliers, whose frequencies are below (Q3 + 1.5 IQR) and above (Q1 - 1.5 IQR).  
   * Use Low Outlier: Only compare terms with unusually low frequencies which are at least 1.5 interquartile ranges below the first quartile (Q1). 
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
