# Advanced Features

* [Overview](#overview)
* [Features](#features)
* [Issues/Questions](#issues)

## <a name='overview'></a> Overview

The Advanced Features options are found in the top right portion of Tokenize, Statistics, Hierarchical Clustering, K-Means Clustering, Similarity Query and TopWord. The main headings are Tokenize, Normalize, Culling, and Temporary Labels.

## <a name='features'></a> Features

### Tokenize 
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__ This feature the text into n-grams of the user's desired length, by tokens or characters.
 
3. __Example:__  
   Example: if the text is:  "the dog ran", Word 1-grams use individual terms (words) as tokens whereas Word 2-grams would use pairs of terms: [the dog] and [dog ran]. Character Ngrams of size 2 would create tokens [th], [he], [e ], etc.
   
4. __Issue/Questions:__  
   

### Normalize  
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__
This feature allows the user to perform analysis based on the term raw counts in their DTM or to attempt to account for document length by using proportional or TF-IDF weighted counts.
   
3. __Example:__  
   
4. __Issue/Questions:__  
   Currently, there is no explanation for the three different forms TF-IDF. Also, the label "Norm:None" should be changed to something meaningful, as it is simply repeat of the argument fed to the scipy function.
   
### Culling Options -- Most Frequent Words
1. __Tool Tip:__  
   Use only the most frequently occuring terms in the DTM.
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   

### Culling Options -- Culling
1. __Tool Tip:__  
   Set the minimum number of documents in which terms must occur to be included in the DTM.
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  

### Culling Options -- Grey Words
1. __Tool Tip:__  
   Exclude the terms with the lowest frequencies from the DTM.
2. __Tool Tip Extended:__  
   This feature attempts to lessen the impact of significantly different document lengths on subsequent analysis.
3. __Example:__  
   
4. __Issue/Questions:__  
   In some ways this is technically a normalisation feature. It's probably best left where it is because it operates through culling, but some discussion of how it operates as normalisation might be called for, and the discussion of the Normalize feature might also recommend it as a strategy.

   This is also really a "Least Frequent Words" feature. It is not clear how Lexos decides the threshold for the number of terms removed.
  
### Assign Temporary Labels
1. __Tool Tip:__  
   Assign temporary names of documents for use in tables and graphs produced by Lexos tools that use the Tokenize, Normalize, and Culling options.
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   Perhaps there needs to be some discussion stating that this feature allows you to substitute labels (e.g. shorter ones) for your document names in graphs and tables of tools that use the Advanced Features. Document names may be changed universally using the Manage Tool.
   
## <a name='issues'></a> General Issues/Questions
Advanced Features options are cached so that they may be set in one tool (e.g. Tokenize) and applied in another (e.g. Hierarchical Clustering). The user may not be aware of this (especially since Culling is closed by default) and may think that they are clustering the full Document-Term Matrix, when in fact they have previously set the Most Frequent Words option. We will need to provide a warning about this in the documentation.
