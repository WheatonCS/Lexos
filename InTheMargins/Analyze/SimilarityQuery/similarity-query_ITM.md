Similarity Query

Similarity Query is a good choice for an early exploration when you wish to rank the "closeness" between a single document and all other documents in your active set. As used here, the rankings are determined by "distance between documents", where small distances (near zero) represent documents that are "similar" and unlike documents have distances closer to one.

Usage:
1. On the left, select the radio button for the one document to serve as the comparison document. All other active documents will be compared to this document.
2. On the right, select how documents should be tokenized, e.g., 1-gram by Tokens will form vectors of single-word counts. More details on tokenization and culling can be found on the [Tokenization page](link to tokenize_ITM). Note: cosine simularity always uses proportions of tokens so no Normalization options are available here.
3. Select the green 'Get Similarity Rankings' button. The results will be shown below in a table. The rows can be sorted in ascending or descending order by clicking on the up/down arrows in the Distance column header. Note that if you change your comparison document, you must select this 'Get Similarity Rankings' button again.
4. (optional) You can use the Search field on the top-right of the table to select rows that match your search criteria and/or you can change the number of entries to show in the top-left pull-down menu in the table. Either of these options will automatically refresh the table or results, that is, you do not have to select the 'Get Similarity Rankings' button again.
5. (optional) Select the blue 'Download Similarity CSV' button to download a comma-separated-value (csv) file. The file with all results will appear in your local Download directory/folder and may be opened with Excel for futher work.


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

