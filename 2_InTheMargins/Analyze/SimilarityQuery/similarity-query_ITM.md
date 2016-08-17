#Similarity Query

Similarity Query is a good choice for an early exploration of your texts, in particular when you wish to rank the "closeness" between a single document and all other documents in your active set. As used here, the rankings are determined by "distance between documents", where small distances (near zero) represent documents that are "similar" and unlike documents have distances closer to one.

### Getting the Results of Similarity Query

1. On the left, select the radio button for the one document to serve as the comparison document. All other active documents will be compared to this document.
2. In the panel on the right, you may configure the [Advanced Options](advanced-options) for manipulating the Document-Term Matrix (DTM). Note: cosine similarity always uses proportions of tokens so no Normalization options are available here.
3. Select the green **Get Similarity Rankings** button. The results will be shown below in a table, which may be sorted by column by clicking on the column headers. An icon will indicate which column is being used for sorting and whether the sort direction is ascending or descending. Use the **Display** dropdown menu to display more than the default 10 rows per page. Note that if you change your comparison document, you must click the **Get Similarity Rankings** button again. If you have documents on multiple pages, you can quickly find a document by typing the first few letters of the document name.
4. The table can be downloaded as a comma-separated-value (CSV) file by clicking the blue **Download Similarity CSV**. The file with all results will appear in your local Download directory/folder and may be opened with Excel for further work.

More details on the internal workings of our implementation of Similarity Query can be found [here](#itm-topic)

## ITM Topic
Cosine simularity is computed between the target document and all other active segments and/or documents. More specificaly, Lexos calls skiKit learn's cosine similarity utility to compute the cosine of the angle between two vector of word counts from the Document Term Matrix. All vectors are positive (in the first quadrant) and thus the angle between any two vectors is in the range [0,pi/2]. Said differently, the value for Cosine Similarity (the cosine of the two vectors) will always be in the range of [0,1], where a higher similarity value indicates that the two document vectors are "closer" to each other. Values approaching zero indicate that the two vectors are further apart when comparing them (i.e., orthogonal). Note that this metric is a measurement of orientation between vectors, not magnitude. 

In detail, the cosine similarity is the normalized dot product of two vectors (of counts or proportions) from the Document Term Matrix (DTM). For example, between documents x and y, let X and Y represent the vectors from the DTM for these two documents, x and y, respectively. The Cosine Similarity between vectors X and Y is:      

         X•Y / ( |X| * |Y| )      dot product of X and Y divided by the product of vector norms

The distance between documents, as shown in the Lexos output, is then defined as:

        distance = (1 - CosineSimilarity),  where 0 <= distance <= 1 

        0 = small distance, "LIKE" vectors

        1 = high distance, "UNLIKE" vectors

Thus, two documents with "similar" counts where the documents contain only two words, such as: <1,0> and <2,0> would have a distance measure of zero(0) (they are "LIKE") whereas two documents with completely unlike word counts of <0,1> and <2,0> would form a 90-degree angle between two orthogonal vectors and thus (1 - cos(90) ) = (1 - 0) = +1 distance (they are "UNLIKE").

 
More reading:

[Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity): Wikipedia

Perone, Christian S. (2013). Machine Learning::Cosine Similarity for Vector Space Models (Part III). Terra Incognita.

[Scikit-learn](http://scikit-learn.org/dev/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html): Machine Learning in Python, Pedregosa et al., JMLR 12, pp. 2825-2830, 2011.

