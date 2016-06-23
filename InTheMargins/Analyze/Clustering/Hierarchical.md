# Hierarchical Clustering
## Dendrograms

* [Overview](#overview)
* [Features](#features)
* [Issues/Questions](#issues)

## <a name='overview'></a> Overview



## <a name='features'></a> Features
## Dendrogram Options

### Distance Metric
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   Euclidean: is the "ordinary" (i.e. straight-line) distance between two points in Euclidean space.
   (more info: https://en.wikipedia.org/wiki/Euclidean_distance)
   Minkowski: is a metric in a normed vector space which can be considered as a generalization of both the Euclidean distance and the Manhattan distance.
   (more info: https://en.wikipedia.org/wiki/Minkowski_distance)
   Manhattan: is a form of geometry in which the usual distance function of metric or Euclidean geometry is replaced by a new metric in which the distance between two points is the sum of the absolute differences of their Cartesian coordinates.
   (More info: https://en.wikipedia.org/wiki/Taxicab_geometry)
   Standardized Euclidian:
   Squared Euclidean: The standard Euclidean distance can be squared in order to place progressively greater weight on objects that are farther apart.
   (more info: https://en.wikipedia.org/wiki/Euclidean_distance)
   Cosine: is a measure of similarity between two vectors of an inner product space that measures the cosine of the angle between them.
   (more info: https://en.wikipedia.org/wiki/Cosine_similarity)
   Correlation:is a measure of statistical dependence between two random variables or two random vectors of arbitrary, not necessarily equal dimension.
   (more info: https://en.wikipedia.org/wiki/Distance_correlation)
   Hamming: the Hamming distance between two strings of equal length is the number of positions at which the corresponding symbols are different.
   (more info: https://en.wikipedia.org/wiki/Hamming_distance)
   Chebyshev: is a metric defined on a vector space where the distance between two vectors is the greatest of their differences along any coordinate dimension.
   (more info: https://en.wikipedia.org/wiki/Chebyshev_distance)
   Jaccard: The Jaccard coefficient measures similarity between finite sample sets, and is defined as the size of the intersection divided by the size of the union of the sample sets.
   (more info: https://en.wikipedia.org/wiki/Jaccard_index)
   Canberra: is a numerical measure of the distance between pairs of points in a vector space. It is a weighted version of L₁ (Manhattan) distance.
   (more info: https://en.wikipedia.org/wiki/Canberra_distance)
   Braycurtis: is a statistic used to quantify the compositional dissimilarity between two different sites, based on counts at each site.
   (more info:https://en.wikipedia.org/wiki/Bray%E2%80%93Curtis_dissimilarity)
3. __Example:__  
   
4. __Issue/Questions:__  
   

### Linkage Method
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   Average: the distance between two clusters is the mean distance between an observation in one cluster and an observation in the other cluster. Whereas the single or complete linkage methods group clusters are based on single pair distances, the average linkage method uses a more central measure of location.
   Single: the distance between two clusters is the minimum distance between an observation in one cluster and an observation in the other cluster. The single linkage method is a good choice when clusters are obviously separated. When observations lie close together, the single linkage method tends to identify long chain-like clusters that can have a relatively large distance separating observations at either end of the chain.
   Complete:  the distance between two clusters is the maximum distance between an observation in one cluster and an observation in the other cluster. This method ensures that all observations in a cluster are within a maximum distance and tends to produce clusters with similar diameters. The results can be sensitive to outliers.
   (source: http://support.minitab.com/en-us/minitab/17/topic-library/modeling-statistics/multivariate/item-and-cluster-analyses/linkage-methods/)
   Could not find Weighted linkage method

3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Dendrogram Title
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   The title of the dendrogram, it will be dispalyed in top of the dendrogram, and it will be used to name the files to download.
3. __Example:__  
   title: Dan_Az
   pdf: den_Dan_Az.pdf
   png: den_Dan_Az.png
   svg: den_Dan_Az.svg
   newick: den_Dan_Az.txt

   If no title inputed:
   pdf: dendrogram.pdf
   png: dendrogram.png
   svg: dendrogram.svg
   newick: newNewickStr.txt
4. __Issue/Questions:__
   
   
### Dendrogram Orientation
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   Vertical: displays the dendrogram vertically with the filenames(leafs) in the bottom
   Horixontal: displays the dendrogram horizontally with the filenames(leafs) in the right
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Number of Leaves
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   divides files by number of leaves to display that many leaves
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Show in Dendrogram
1. __Tool Tip:__
   empty
   none
2. __Tool Tip Extended:__
   * Show Branch Height in Dendrogram:
   * Show Legends in Dendrogram:
3. __Example:__

4. __Issue/Questions:__


## Silhouette Score Options

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
