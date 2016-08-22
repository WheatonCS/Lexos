The Lexos **K-Means Clustering** tool partitions your active documents into flat clusters in a way that minimizes the variation within the clusters. It produces a scatterplot graph in which you can visualize the distance between documents or clusters. The "K" in "K-Means" refers to the number of partitions. For instance, if you wish to cluster your documents into three groups, you would set `K=3`. The default is the number of active documents, but you will probably want to set this to a smaller number. There is no obvious way to choose the number of clusters. It can be helpful to perform hierarchical clustering before performing K-Means clustering, as the resulting dendrogram may suggest a certain number of clusters that is likely to produce meaningful results. The K-means procedure is very sensitive to the position of the initial seeds, although employing the **K-means++** setting can help to constrain this placement.

Lexos provides two methods of visualizing K-means cluster analyses. The default **Voronoi Cells** identifies a centroid (central point) in each cluster and draws a trapezoidal polygon around it. This is helpful in allowing you to see which points fall into which cluster. Select **PCA** in the **Method of Visualization** dropdown to view the graph as a _[Principal Component Analysis](https://en.wikipedia.org/wiki/Principal_component_analysis)_, where dots on the plane are colored to mark their cluster membership. Both visualization approaches can you judge distances between clusters.

### Generating and Reading a K-Means Cluster Analysis

Simply click the **Get K-Means** button to perform a K-means cluster analysis. If you wish, you can modify the default settings using the **Advanced K-Means Options** and **Silhouette Score Options** menus described below.

K-Means cluster analyses can contain a lot of points that are very close together, making the graph difficult to read. In order to aid the process, Lexos provides a table to the left of the graph which displays your documents and color codes them to indicate which cluster they belong to. The same colors are used in the graph. In the Voronoi cell graph, you can move your mouse cursor over the document in the table or a point on the graph to reveal a tooltip label showing the document's name.

#### Advanced K-Means Options

Since cluster membership is adjusted at each stage of the process by the re-location of the centroids, the number of iterations required and other factors can be adjusted to select a cutoff point for the algorithm or a desired threshold for convergence of different clusters. These adjustments are handled by the **Advanced K-Means Options**: **Maximum Number of Iterations**, **Method of Initialization**, **Number of Iterations with Different Centroids**, and **Relative Tolerance**. As with the initial choice of cluster numbers, there are no hard and fast rules for how these factors should be applied. The default settings should serve most users' purposes. However, here are some brief descriptions of the purposes of each option:

<u>Maximum number of iterations:</u> The K-means algorithm will continue to re-compute centroids for each cluster until all documents settle down into "final" clusters. It is possible that a situation occurs where a document continues to toggle back and forth between two clusters. Setting this value avoids an endless, or at least an unnecessary number of repetitions of the algorithm with little change.

<u>Method of Initialization:</u> Your results of using K-means on a collection of documents can vary significantly depending on the initial choice of centroids. In Lexos the user is offered two choices: **K-Means++** and **Random**. When using the default **K-Means++** setting, Lexos chooses the first of the K clusters at random (typically by picking any one of the documents in the starting set as representative of a center of a future cluster). The remaining (K-1) cluster centers are then chosen from the remaining documents by computing a probability proportional to the distances of the centers already chosen. Once all centroids are chosen, normal K-Means clustering takes place. The **Random** setting employs a "random seed" approach in which the locations of _all_ centroids at the initial stage are generated randomly. It is best to experiment multiple times with different random seeds.

<u>Number of Iterations with Different Centroids:</u> Documentation of this feature is not yet available.

<u>Relative Tolerance:</u> Documentation of this feature is not yet available.

#### Silhouette Score Options

Silhouette scores give a general indication of how well individual objects lie within their cluster and are thus one method of [measuring cluster robustness](establishing-robust-clusters). A score of 1 indicates tight, distinct clusters. Values near 0 indicate overlapping clusters. Negative values generally indicate that a sample has been assigned to the wrong cluster, as a different cluster is more similar

To generate a silhouette score for your dendrogram, click on the **Silhouette Score Options** menu. The only option is to change the **Distance Metric** used for measuring the distance between points. For further information, see [Choosing a Distance Metric](choosing-a-distance-metric). Once you have selected a distance metric, click the **Get K-Means** button and the silhouette score will appear below the button when the process is complete.

### Downloading K-Means Graphs

There is currently no method for downloading Voronoi graphs, and we recommend taking screen shots. For PCA graphs, you can right-click and use your browser's **Save image as...** function. We recommend clicking the **Enlarge Graph** button to open the image in a new window.