The Lexos **Hierarchical Clustering** tool performs hierarchical agglomerative cluster analysis on your active documents and produces a visualization of this analysis in the form of a dendrogram (tree diagram). The most important options are the **Distance Metric** (method of measuring the distance between documents) and **Linkage Method** (method of determining when documents will be attached to a cluster) dropdown menus. Lexos uses Euclidean distance and average linkage as defaults. For further details about how to choose a distance metric and linkage method, see the topics discussion on [Hierarchical Clustering]().

The remaining options allow you to configure the appearance of the dendrogram. You may supply a **Dendrogram Title**, which will be displayed at the top of the graph and select the **Dendrogram Orientation** (vertical or horizontal). In our experience, vertically-oriented dendrograms are easier to interpret. However, when they have many leaves, the labels tend to overlap and become unreadable. Horizontal dendrograms may produce slightly better results. Another approach is to limit the **Number of Leaves** displayed in the dendrogram. Reducing this number will collapse the most closely related clusters (those lower down on the dendrogram), showing only the larger groups. A numbered label in parentheses will show how many leaves have been collapsed into single branch. See below for other strategies for producing more readable dendrograms.

The **Show Branch Height in Dendrogram** option will place red nodes at the top of each clade labelled with the height (length) of the clade branches from the leaf node. See the [How to Read a Dendrogram](how-to-read-a-dendrogram) video for the interpretation of branch height. The **Show Legends in Dendrogram** will add to the dendrogram image a series of annotations showing the options you have selected.

All of the [Advanced Options](advanced-options) for manipulating the Document-Term Matrix (DTM) are available in the **Hierarchical Clustering** tool. There are also options for generating  _Silhouette Score_,  measure of determining cluster robustness. **Silhouette Score Options** are discussed below.

Once you have selected your options, click the **Get Dendrogram** button. Once the dendrogram appears, you can click on it top open it in a new window.

###Silhouette Scores
Silhouette scores give a general indication of how well individual objects lie within their cluster and are thus one method of [measuring cluster robustness](establishing-robust-clusters). A score of 1 indicates tight, distinct clusters. Values near 0 indicate overlapping clusters. Negative values generally indicate that a sample has been assigned to the wrong cluster, as a different cluster is more similar.

To generate a silhouette score for your dendrogram, mouse over the **Silhouette Score** button. You may need to re-calculate the silhouette score by clicking the **Get Dendrogram** button. Further information can be found in the topics article on silhouette scores. 

## Dendrograms

* [Overview](#overview)
* [Features](#features)
* [Issues/Questions](#issues)

## <a name='overview'></a> Overview


   none
2. __Tool Tip Extended:__  
   Divides files by number of leaves to display the selected number of branches in the dendrogram.
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Show in Dendrogram
1. __Tool Tip:__
   * Based on the chosen distance metric, shows the y-axis value indicating the distance where two leaves or branches are joined.
   * none
2. __Tool Tip Extended:__
   * Show Branch Height in Dendrogram:  
   * Show Legends in Dendrogram: Selecting this option shows the silhouette score with a short explanation  
3. __Example:__

4. __Issue/Questions:__


## Silhouette Score Options
A silhouette score is a measure of fit for your clusters. It gives a general indication of how well individual objects lie within their cluster. A score of 1 indicates tight, distinct clusters. Values near 0 indicate overlapping clusters. Negative values generally indicate that a sample has been assigned to the wrong cluster, as a different cluster is more similar.  
### Criterion
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   * Maxclust:  
   * Inconsistent:  
   * Distance:  
   * Monocrit:  
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Threshold (t)
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Get Dendrogram
1. __Tool Tip:__  
   
2. __Tool Tip Extended:__  
   Button that generates the dendrogram
3. __Example:__  
   
4. __Issue/Questions:__  
   I was hoping here we could explain more, like what the dendrogram shows/how it's made

### Download
1. __Tool Tip:__
   none
2. __Tool Tip Extended:__
   * PDF:  
   * PNG:  
   * SVG:  
   * Newick:  
3. __Example:__

4. __Issue/Questions:__


## <a name='issues'></a> General Issues/Questions
There is a box with tokenize options on this page that has not been included in the discriptions because these should all be on the tokenize page already
