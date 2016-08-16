# Hierarchical Clustering
## Dendrograms

* [Overview](#overview)
* [Features](#features)
* [Issues/Questions](#issues)

## <a name='overview'></a> Overview

All of the [Advanced Options](advanced-options) for manipulating the Document-Term Matrix (DTM) are available.

## <a name='features'></a> Features
## Dendrogram Options

### Distance Metric
1. __Tool Tip:__  
   Different methods for measuring the distance/difference between documents.
2. __Tool Tip Extended:__  
   * Euclidean: is the "ordinary" (i.e. straight-line) distance between two points in Euclidean space.
   (more info: https://en.wikipedia.org/wiki/Euclidean_distance)  
   * Minkowski: a metric in a normed vector space which can be considered as a generalization of both the Euclidean distance and the Manhattan distance.
   (more info: https://en.wikipedia.org/wiki/Minkowski_distance)  
   * Manhattan: a form of geometry in which the usual distance function of metric or Euclidean geometry is replaced by a new metric in which the distance between two points is the sum of the absolute differences of their Cartesian coordinates.
   (More info: https://en.wikipedia.org/wiki/Taxicab_geometry)  
   * Standardized Euclidian: *need explaination*   
   * Squared Euclidean: The standard Euclidean distance can be squared in order to place progressively greater weight on objects that are farther apart.
   (more info: https://en.wikipedia.org/wiki/Euclidean_distance)  
   * Cosine: a measure of similarity between two vectors of an inner product space that measures the cosine of the angle between them.
   (more info: https://en.wikipedia.org/wiki/Cosine_similarity)  
   * Correlation: a measure of statistical dependence between two random variables or two random vectors of arbitrary, not necessarily equal dimension.
   (more info: https://en.wikipedia.org/wiki/Distance_correlation)  
   * Hamming: the Hamming distance between two strings of equal length is the number of positions at which the corresponding symbols are different.
   (more info: https://en.wikipedia.org/wiki/Hamming_distance)  
   * Chebyshev: a metric defined on a vector space where the distance between two vectors is the greatest of their differences along any coordinate dimension.
   (more info: https://en.wikipedia.org/wiki/Chebyshev_distance)  
   * Jaccard: The Jaccard coefficient measures similarity between finite sample sets, and is defined as the size of the intersection divided by the size of the union of the sample sets.
   (more info: https://en.wikipedia.org/wiki/Jaccard_index)  
   * Canberra: a numerical measure of the distance between pairs of points in a vector space. It is a weighted version of L₁ (Manhattan) distance.
   (more info: https://en.wikipedia.org/wiki/Canberra_distance)  
   * Braycurtis: a statistic used to quantify the compositional dissimilarity between two different sites, based on counts at each site.
   (more info:https://en.wikipedia.org/wiki/Bray%E2%80%93Curtis_dissimilarity)  
3. __Example:__  
   
4. __Issue/Questions:__  
   Standardized Euclidean still needs an explanation.

### Linkage Method
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   * Average: the distance between two clusters is the mean distance between an observation in one cluster and an observation in the other cluster. Whereas the single or complete linkage methods group clusters are based on single pair distances, the average linkage method uses a more central measure of location.  
   * Single: the distance between two clusters is the minimum distance between an observation in one cluster and an observation in the other cluster. The single linkage method is a good choice when clusters are obviously separated. When observations lie close together, the single linkage method tends to identify long chain-like clusters that can have a relatively large distance separating observations at either end of the chain.  
   * Complete:  the distance between two clusters is the maximum distance between an observation in one cluster and an observation in the other cluster. This method ensures that all observations in a cluster are within a maximum distance and tends to produce clusters with similar diameters. The results can be sensitive to outliers.
   (source: http://support.minitab.com/en-us/minitab/17/topic-library/modeling-statistics/multivariate/item-and-cluster-analyses/linkage-methods/)  
   * Weighted: needs explanation  

3. __Example:__  
   
4. __Issue/Questions:__  
   Weighted needs an explanation
   
### Dendrogram Title
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   The title of the dendrogram, it will be displayed at the top of the dendrogram and be used to name the files if they are downloaded.
3. __Example:__  
   Title: Dan_Az  
   PDF: den_Dan_Az.pdf  
   PNG: den_Dan_Az.png  
   SVG: den_Dan_Az.svg  
   Newick: den_Dan_Az.txt  

   If no title inputed:  
   PDF: dendrogram.pdf  
   PNG: dendrogram.png  
   SVG: dendrogram.svg  
   Newick: newNewickStr.txt  
4. __Issue/Questions:__
   
   
### Dendrogram Orientation
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   * Vertical: displays the dendrogram vertically with the filenames (leaves) at the bottom.  
   * Horizontal: displays the dendrogram horizontally with the filenames (leaves) to the right.  
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Number of Leaves
1. __Tool Tip:__  
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
