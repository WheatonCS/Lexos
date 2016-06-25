# Similarity Query

* [Overview](#overview)
* [Features](#features)
* [Issues/Questions](#issues)

## <a name='overview'></a> Overview



## <a name='features'></a> Features

### Select Comparision Document
1. __Tool Tip:__  
   Select one document to be the external comparison. All other documents shown below will be used to make the model, and will be ranked in order of most to least similar to the comparison document in your results.
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   In tool tip: remove "," before "and"

### Get Similarity Rankings
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   what does this generate and what does it mean?
   
### Download Similarity CSV
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   what will this include?
   
### Similarity Rankings
1. __Tool Tip:__  
   The module used to produce this ranking employs Latent Semantic Analysis to generate unique vectors for each document. The cosine angle between your comparison document's vector and the vector of each document of your corpus is calculated, and these values are then compared. Cosine similarity measures can be between (0, 1), and the higher the value, the closer the comparison document's vector is to that document's vector as opposed to the other documents' vectors.
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   explain "latent semantic analysis"
   
## <a name='issues'></a> General Issues/Questions
Tokenize options are not described on this page
