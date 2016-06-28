# Tokenize

* [Overview](#overview)
* [Features](#features)
* [Issues/Questions](#issues)

## <a name='overview'></a> Overview



## <a name='features'></a> Features
## Document-Term Matrix (DTM) Options
### Data Orientaion
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   * Documents as Columns, Terms as Rows:  
   * Documents as Rows, Terms as Columns:  
3. __Example:__  
   
4. __Issue/Questions:__  
   
   

### Regenerate Table
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Tokenize
1. __Tool Tip:__  
   empty
2. __Tool Tip Extended:__  
   * n-gram:  
   * by Token:  
   * by Characters:  
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Normalize
1. __Tool Tip:__  
   * Proportional Counts: none  
   * Raw Counts: none  
   * Weighted Counts (TF-IDF): Normalize the data for different document lengths using Term Frequency-Inverse Document Frequency (TF-IDF). Selecting TF-IDF allows you to choose the distance metric according to which each document vector is normalized. Lexos uses base e (natural log) as the default.  
2. __Tool Tip Extended:__  
   * Proportional Counts:  
   * Raw Counts:  
   * Weighted Counts:  
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Culling Options
1. __Tool Tip:__  
   * Most Frequent Words: Choose how many tokens are included in the document term matrix from the entire corpus, starting with the most frequent.  
   * Culling: Remove any tokens that do not appear in at least X of the current active segments.  
   * Grey Words: Check this box when segment lengths (token counts) differ significantly from one another. This option will disable (remove) the tokens with the lowest frequencies to attempt to remove bias from analyses.  
2. __Tool Tip Extended:__  
   * Most Frequent Words:  
   * Culling:  
   * Grey Words:  
3. __Example:__  
   
4. __Issue/Questions:__  
   
    
### Assign Temporary Labels
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
## <a name='issues'></a> General Issues/Questions

