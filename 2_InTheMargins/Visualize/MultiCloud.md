# Multicloud

* [Overview](#overview)
* [Features](#features)
* [Issues/Questions](#issues)

## <a name='overview'></a> Overview



## <a name='features'></a> Features

### Document Clouds
1. __Tool Tip:__  
   Document clouds are word clouds based on the documents you select from your uploaded documents. Topic clouds are word clouds generate clouds from the .txt output from MALLET. You may use either the output of the "--words-topic-counts-file" command or the unzipped file produced by the "--output_state" command.
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   

#### Select a Document
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   

### Topic Clouds
1. __Tool Tip:__  
   Document clouds are word clouds based on the documents you select from your uploaded documents. Topic clouds are word clouds generate clouds from the .txt output from MALLET. You may use either the output of the "--words-topic-counts-file" command or the unzipped file produced by the "--output_state" command.
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   

#### Upload a MALLET Topic File
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Get Graph (Document Cloud)
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   This tool creates a vizualization for each selected document. Each vizualization includes tokens varying in size and color based on how often they appear in the file. Larger and more yellow tokens appear more often in the file while smaller and more blure tokens appear less often.
3. __Example:__  
   
4. __Issue/Questions:__  
   

## <a name='issues'></a> General Issues/Questions
The d3.js algorithm used to create word clouds drops high frequency words if they cannot fit within the layout. Users are advised to compare their results to the table in Tokenize to make sure that the highest ranked words are in the clouds produced by Lexos. Sometimes generating individual clouds in Word Cloud will cause the terms to appear in the new layout (although Word Cloud has the same possibility of dropping terms). BubbleViz may also be used to check that the word cloud is accurate.
