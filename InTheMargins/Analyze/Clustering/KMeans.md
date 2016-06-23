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
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Get K-Means
1. __Tool Tip:__  
   
2. __Tool Tip Extended:__  
   Button that genereates the graph
3. __Example:__  
   
4. __Issue/Questions:__  
   
## <a name='issues'></a> General Issues/Questions
Tokenize options on the page are not described here
