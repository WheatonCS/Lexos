Similarity Query

Similarity Query as implemented here is a good first test to rank the "closeness" between a single document and all other documents in your active set. We sometimes apply it early in exploratory analyses and study the ranking. Note: It is easy to use and easy to over-interpret the results, but again it is nice metric between (segments of) documents. 

Similarity Query supports the comparison of one document to all other active documents, after the user selects the target document name and tokenize options. Cosine simularity is computed between the target document  and all other active segments and/or documents. More specificaly, Lexos calls skiKit learn's cosine similarity utility to compute the cosine of the angle between two vector of word counts from the Document Term Matrix. All vectors are positive (in the first quadrant) and thus the angle between any two vectors is in the range [0,pi/2]. Said differently, the value for Cosine Similarity (the cosine of the two vectors) will always be in the range of [0,1], where a higher similarity value indicates that the two document vectors are "closer" to each other. Values approaching zero indicate that the two vectors are further apart when comparing them (i.e., orthogonal). Note that this metric is a measurement of orientation between vectors, not magnitude. 



Ok, if you've read this far, the cosine similarity is the normalized dot product of two vectors of counts from the Document Term Matrix (DTM), for example between documents X and Y:
The Cosine Similarity between two vectors X and Y:      

         X•Y / ( |X| * |Y| )      dot product of X and Y divided by the product of vector norms

The distance between documents, as shown in the Lexos output, is then defined as:

        distance = (1 - CosineSimilarity), where 0 <= distance <= 1 

        0 = small distance, LIKE vectors

        1 = high distance, UNLIKE vectors

Thus, two documents with "similar" counts of two words: <1,0> and <2,0> would have a distance measure = 0 (they are LIKE) whereas two documents with completely unlike word counts of <0,1> and <2,0> would form a 90-degree angle between two orthogonal vectors and thus (1 - cos(90) ) = +1 distance.


Tutorial:
 
TBD
 
 
More reading:

Cosine Similarity: Wikipedia

Perone, Christian S. (2013). Machine Learning::Cosine Similarity for Vector Space Models (Part III). Terra Incognita.

Scikit-learn: Machine Learning in Python, Pedregosa et al., JMLR 12, pp. 2825-2830, 2011.

