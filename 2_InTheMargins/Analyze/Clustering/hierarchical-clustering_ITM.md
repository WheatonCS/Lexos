The Lexos **Hierarchical Clustering** tool performs hierarchical agglomerative cluster analysis on your active documents and produces a visualization of this analysis in the form of a dendrogram (tree diagram). The most important options are the **Distance Metric** (method of measuring the distance between documents) and **Linkage Method** (method of determining when documents will be attached to a cluster) dropdown menus. Lexos uses Euclidean distance and average linkage as defaults. For further details about how to choose a distance metric and linkage method, see the topics discussion on [Hierarchical Clustering]().

The remaining options allow you to configure the appearance of the dendrogram. You may supply a **Dendrogram Title**, which will be displayed at the top of the graph and select the **Dendrogram Orientation** (vertical or horizontal). In our experience, vertically-oriented dendrograms are easier to interpret. However, when they have many leaves, the labels tend to overlap and become unreadable. Horizontal dendrograms may produce slightly better results. Another approach is to limit the **Number of Leaves** displayed in the dendrogram. Reducing this number will collapse the most closely related clusters (those lower down on the dendrogram), showing only the larger groups. A numbered label in parentheses will show how many leaves have been collapsed into single branch. See below for other strategies for producing more readable dendrograms.

The **Show Branch Height in Dendrogram** option will place red nodes at the top of each clade labelled with the height (length) of the clade branches from the leaf node. See the [How to Read a Dendrogram](how-to-read-a-dendrogram) video for the interpretation of branch height. The **Show Legends in Dendrogram** will add to the dendrogram image a series of annotations showing the options you have selected.

All of the [Advanced Options](advanced-options) for manipulating the Document-Term Matrix (DTM) are available in the **Hierarchical Clustering** tool. There are also options for generating  _Silhouette Score_,  measure of determining cluster robustness. **Silhouette Score Options** are discussed below.

Once you have selected your options, click the **Get Dendrogram** button. Once the dendrogram appears, you can click on it top open it in a new window.

### Silhouette Scores
Silhouette scores give a general indication of how well individual objects lie within their cluster and are thus one method of [measuring cluster robustness](establishing-robust-clusters). A score of 1 indicates tight, distinct clusters. Values near 0 indicate overlapping clusters. Negative values generally indicate that a sample has been assigned to the wrong cluster, as a different cluster is more similar.

To generate a silhouette score for your dendrogram, mouse over the **Silhouette Score** button. You may need to re-calculate the silhouette score by clicking the **Get Dendrogram** button. Further information can be found in the topics article on silhouette scores.

You can modify the method of calculating the silhouette score from the **Silhouette Score** menu. More information will be added here in the future.

The following are notes about silhouette scores:

Lexos uses scipy.cluster.hierarchy.fcluster(Z, t, criterion='inconsistent', depth=2, R=None, monocrit=None)

dendrogrammer.py runs scipy.cluster.hierarchy.fcluster(Z, t, criterion, monocrit)

1. Flatten the cluster as defined by the chosen linkage matrix
2. t is a float value that defines the threshold to apply when forming flat clusters.
3. criterion is an optional string designating the criterion to use in forming flat clusters. This can have the following values:

    inconsistent (default): If a cluster node and all its descendants have an inconsistent value less than or equal to t then all its leaf descendants belong to the same flat cluster. When no non-singleton cluster meets this criterion, every node is assigned to its own cluster. (Default)

    distance : Forms flat clusters so that the original observations in each flat cluster have no greater a cophenetic distance than t. [The cophenetic distance between two objects is the height of the dendrogram where the two branches that include the two objects merge into a single branch. Outside the context of a dendrogram, it is the distance between the largest two clusters that contain the two objects individually when they are merged into a single cluster that contains both.]
    
    maxclust : Finds a minimum threshold r so that the cophenetic distance between any two original observations in the same flat cluster is no more than r and no more than t flat clusters are formed.

    monocrit : Forms a flat cluster from a cluster node c with index i when monocrit[j] <= t. For example, to threshold on the maximum mean distance as computed in the inconsistency matrix R with a threshold of 0.8 do:

        MR = maxRstat(Z, R, 3)
        cluster(Z, t=0.8, criterion='monocrit', monocrit=MR)

    maxclust_monocrit : Forms a flat cluster from a non-singleton cluster node c when monocrit[i] <= r for all cluster indices i below and including c. r is minimized such that no more than t flat clusters are formed. monocrit must be monotonic. For example, to minimize the threshold t on maximum inconsistency values so that no more than 3 flat clusters are formed, do:

            MI = maxinconsts(Z, R)
            cluster(Z, t=3, criterion='maxclust_monocrit', monocrit=MI)

    depth is an optional integer indicating the maximum depth to perform the inconsistency calculation. It has no meaning for the other criteria. Default is 2.

    R is n optional inconsistency matrix to use for the ‘inconsistent’ criterion. This matrix is computed if not provided.

    monocrit is an optional array of length n-1. monocrit[i] is the statistics upon which non-singleton i is thresholded. The monocrit vector must be monotonic, i.e. given a node c with index i, for all node indices j corresponding to nodes below c, monocrit[i] >= monocrit[j].

Returns an array of length n. T[i] is the flat cluster number to which original observation i belongs.


### Downloading Dendrograms
Lexos allows you to download dendrogram images in a number of formats (PDF, PNG, and SVG). To download dendrogram image, click the appropriate button on the right side of the screen.

Lexos uses scipy's [clustering package](http://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.dendrogram.html) to plot dendrograms, and this has some severe limitations in the type of output available. There are many other tools available which allow you to explore and manipulate dendrograms once you have done your cluster analysis. These tools typically allow you to import pre-existing dendrogram (tree) structure in [Newick format](https://en.wikipedia.org/wiki/Newick_format): a text file representing the hierarchical structure using parentheses and commas. Lexos also provides **Newick** download button which will convert your dendrogram's structure to a text file in Newick format. You can then upload this file in external tools. Note, however, that many external dendrogram plotting tools do not seem to preserve branch height.  


