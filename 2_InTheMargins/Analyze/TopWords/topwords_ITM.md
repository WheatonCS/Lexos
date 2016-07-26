#Finding the Top Words

Topword identifies tokens that appear with unique proportions when compared to other collections using a proportional z-test to identify tokens in documents or document classes with proportions significantly differently from those same tokens in all documents or document classes. Topwords allows you to ask what tokens (words) appear abundantly more in one document than all other documents? What tokens appear most infrequently in one document than others? If we attach [class labels](link to discussion of class labels) to collections of documents (classes), what tokens appear abundantly (or infrequently) in one class vs. proportions found in other classes? 

Note: when comparing some documents to a group (class) of other documents, you will need to assign class labels to each document. In the [Manage](link to manage directions) page, you can right-click and set the class on all active documents or set each document's class individually. If you do not assign class labels to your active documents, topwords will only allow you to compare each document to all the documents as a whole.

## How to read the results
Only the top 20 statistically significant topwords (absolute values larger than 1.96) are shown. A larger positive z-score indicates a token in this document or class is used more frequently than in the comparison group and a larger negative z-score indicates a relatively rarely used token.


    
##Limitations: 
  1. Topwords assumes the distribution of token frequencies is a normal distribution (not the case for most data).
  2. Documents and/or document classes should have at least 100 tokens each. 

##Topword Options


