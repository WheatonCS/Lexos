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
2. __Tool Tip Extended:__ This feature divides the DTM into n-grams of the users desired length, by tokens or characters.
 
3. __Example:__  
   
4. __Issue/Questions:__  
   In tool tip: The term "Ngram" is used. Be consistent with the form "n-gram".

### Normalize  
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__
This feature allows the user to perform analysis based on the raw counts in their DTM or to attempt to account for document length by using proportional or weighted counts.
   
3. __Example:__  
   
4. __Issue/Questions:__  
   Currently, the options do not work, except for Norm:None, which needs to be explained.
   
### Culling Options -- Most Frequent Words
1. __Tool Tip:__  
   Change "N=100 means top-100 most frequent terms across all active segments" to "N=100 means the top 100 most frequent terms across all active documents".
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   Technically, this should be "Most Frequent Terms", but I think we can let this one slide.

### Culling Options -- Culling
1. __Tool Tip:__  
   Change "Remove any tokens that do not appear in at least X of the current active segments" to "Remove any terms that do not appear in at least X number of the current active documents".
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  

### Culling Options -- Grey Words
1. __Tool Tip:__  
   Change to "Remove the terms with the lowest frequencies from the Document-Term Matrix".
2. __Tool Tip Extended:__  
   This feature attempts to lessen the impact of significantly different document lengths on subsequent analysis.
3. __Example:__  
   
4. __Issue/Questions:__  
   In some ways this is technically a normalisation feature. It's probably best left where it is because it operates through culling, but some discussion of how it operates as normalisation might be called for, and the discussion of the Normalize feature might also recommend it as a strategy.

   This is also really a "Least Frequent Words" feature. It is not clear how Lexos decides the threshold for the number of terms removed.
  
### Assign Temporary Labels
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   Perhaps there needs to be some discussion stating that this feature allows you to substitute labels (e.g. shorter ones) for your document names in graphs and tables of tools that use the Advanced Features. Document names may be changed universally using the Manage Tool.
   
## <a name='issues'></a> General Issues/Questions
Advanced Features options are cached so that they may be set in one tool (e.g. Tokenize) and applied in another (e.g. Hierarchical Clustering). The user may not be aware of this (especially since Culling is closed by default) and may think that they are clustering the full Document-Term Matrix, when in fact they have previously set the Most Frequent Words option. We will need to provide a warning about this in the documentation.
