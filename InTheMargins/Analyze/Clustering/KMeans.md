# K-Means Clustering

* [Overview](#overview)
* [Features](#features)
* [Issues/Questions](#issues)

## <a name='overview'></a> Overview



## <a name='features'></a> Features
## K-Means Options

### Number of Clusters (K value)
1. __Tool Tip:__  
   The number of clusters or the number of centroids. The K-value should be always less or equal to the number of active documents.
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   
### Method of Visualization
1. __Tool Tip:__  
   Choose either a Principal Component Analyais (PCA) graph of xy coordinates with document points colored to reflect document clusters or a Voronoi diagram with polygons drawn around them to represent document clusters.
2. __Tool Tip Extended:__  
   * Voroni:  
   * PCA:  
3. __Example:__  
   Kmeans() in lexos.py:
   if request.form['viz'] == 'PCA':
   ...
   elif request.form['viz'] == 'Voronoi':
   ...
   
4. __Issue/Questions:__  
   
## Advanced K-Means Options

### Maximum Number of Iterations
1. __Tool Tip:__  
   Maximum number of iterations of the k-means algorithm for a single run.
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Method of Initialization
1. __Tool Tip:__  
   'k-means++' selects initial cluster centers for k-means clustering in a smart way to speed up convergence. The 'random' chooses k observations (rows) at random from data for the initial centroids.
2. __Tool Tip Extended:__  
   * k-means++:  
   * random:  
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Number of Iterations with Different Centroids
1. __Tool Tip:__  
   The number of times the k-means algorithm will be run with different centroid seeds. The final results will be the best output of n_init consecutive runs in terms of inertia.
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   Fix tool tip: "time" to "times"
   
### Relative Tolerance
1. __Tool Tip:__  
   Decimal, relative tolerancewith respect to inertia to declare convergence.
2. __Tool Tip Extended:__  
   sklearn.cluster.KMeans
   _kmeans_single() in k_means_.py: Relative tolerance with regards to inertia to declare convergence
   
3. __Example:__  
   
4. __Issue/Questions:__  
  
   
## Silhouette Score Options
1. __Tool Tip:__  
   A silhouette score is a measure of fit for your clusters. It gives a general indication of how well individual objects lie within their cluster. A score of 1 indicates tight, distinct clusters. Values near 0 indicate overlapping clusters. Negative values generally indicate that a sample has been assigned to th wrong cluster, as a different cluster is more similar.
### Distance Metric
1. __Tool Tip:__  
   Different methods for measuring the distance/difference between documents.
2. __Tool Tip Extended:__  
   * Euclidean: is the "ordinary" (i.e. straight-line) distance between two points in Euclidean space.
   (more info: https://en.wikipedia.org/wiki/Euclidean_distance)  
   * Minkowski: is a metric in a normed vector space which can be considered as a generalization of both the Euclidean distance and the Manhattan distance.
   (more info: https://en.wikipedia.org/wiki/Minkowski_distance)  
   * Manhattan: is a form of geometry in which the usual distance function of metric or Euclidean geometry is replaced by a new metric in which the distance between two points is the sum of the absolute differences of their Cartesian coordinates.
   (More info: https://en.wikipedia.org/wiki/Taxicab_geometry)  
   * Standardized Euclidian:  
   * Squared Euclidean: The standard Euclidean distance can be squared in order to place progressively greater weight on objects that are farther apart.
   (more info: https://en.wikipedia.org/wiki/Euclidean_distance)  
   * Cosine: is a measure of similarity between two vectors of an inner product space that measures the cosine of the angle between them.
   (more info: https://en.wikipedia.org/wiki/Cosine_similarity)  
   * Correlation:is a measure of statistical dependence between two random variables or two random vectors of arbitrary, not necessarily equal dimension.
   (more info: https://en.wikipedia.org/wiki/Distance_correlation)  
   * Hamming: the Hamming distance between two strings of equal length is the number of positions at which the corresponding symbols are different.
   (more info: https://en.wikipedia.org/wiki/Hamming_distance)  
   * Chebyshev: is a metric defined on a vector space where the distance between two vectors is the greatest of their differences along any coordinate dimension.
   (more info: https://en.wikipedia.org/wiki/Chebyshev_distance)  
   * Jaccard: The Jaccard coefficient measures similarity between finite sample sets, and is defined as the size of the intersection divided by the size of the union of the sample sets.
   (more info: https://en.wikipedia.org/wiki/Jaccard_index)  
   * Canberra: a numerical measure of the distance between pairs of points in a vector space. It is a weighted version of L₁ (Manhattan) distance.
   (more info: https://en.wikipedia.org/wiki/Canberra_distance)  
   * Braycurtis: is a statistic used to quantify the compositional dissimilarity between two different sites, based on counts at each site.
   (more info:https://en.wikipedia.org/wiki/Bray%E2%80%93Curtis_dissimilarity)  
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Get K-Means
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   Button that genereates the graph
3. __Example:__  
   
4. __Issue/Questions:__  
   
## <a name='issues'></a> General Issues/Questions
Tokenize options on the page are not described here
