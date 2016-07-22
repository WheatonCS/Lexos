# Word Cloud

* [Overview](#overview)
* [Features](#features)
* [Issues/Questions](#issues)

## <a name='overview'></a> Overview
This type of visualization will give you one area filled with words from all of the selected active files.


## <a name='features'></a> Features

### Select a Document
1. __Tool Tip:__  
   none (Large graphs can take a while to render.)
2. __Tool Tip Extended:__  
   Here you can select as many of your active files as you like to be included in the Word Cloud. Words from any selected document may or may not be used in the visualization.
3. __Example:__  
   
4. __Issue/Questions:__  
   

### Get Graph
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   Selecting this option will give you a Word Cloud using default settings and words selected documents.
3. __Example:__  
   
4. __Issue/Questions:__  
   This doesn't always look like it has the number of words selected, especially with the default. I think there might be a cap on the number of words they can fit in the Word Cloud and the words selected may be any of the most frequent words up to the number of words you selected.

### View Word Counts
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   Selecting this tool will give you a pop-up with all of the terms in your selected documents and the number of times those terms appear.
3. __Example:__  
   
4. __Issue/Questions:__  
The d3.js algorithm used to create word clouds drops high frequency words if they cannot fit within the layout. Users are advised to check the table of term counts to make sure that the highest ranked words are in the clouds produced by Lexos. Sometimes re-generating the clouds with different settings will cause the terms to appear in the new layout.

### Spiral
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   * Archimedian:  
   * Rectangular:  
3. __Example:__  
   
4. __Issue/Questions:__  
   I can't tell what this does

### Scale
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   * log n:  
   * √n:  
   * n:  
3. __Example:__  
   
4. __Issue/Questions:__  
   not sure what these change

### Font
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   not sure this works, Impact on default or san serif with blank box

### Orientations
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   These options change the number of orientations the words will be in and the range of angles they can be in. To see these changes either drag the arrows on the protractor or click on the Word Cloud.
3. __Example:__  
   
4. __Issue/Questions:__  
   

### Number of Words
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   see get graph

### Download
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   You can save your Word Cloud image as either a SVG or a PNG.
3. __Example:__  
   
4. __Issue/Questions:__  
   

## <a name='issues'></a> General Issues/Questions

