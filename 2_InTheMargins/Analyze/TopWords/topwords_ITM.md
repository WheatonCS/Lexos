#Finding the Top Words

Topword identifies tokens that appear with unique proportions when compared to other collections using a proportional z-test to identify tokens in documents or document classes with proportions significantly differently from those same tokens in all documents or document classes. Topwords allows you to ask what tokens (words) appear abundantly more in one document than all other documents? What tokens appear most infrequently in one document than others? If we attach [class labels](link to discussion of class labels) to collections of documents (classes), what tokens appear abundantly (or infrequently) in one class vs. proportions found in other classes? 

Note: when comparing some documents to a group (class) of other documents, you will need to assign class labels to each document. In the [Manage](link to manage directions) page, you can right-click and set the class on all active documents or set each document's class individually. If you do not assign class labels to your active documents, topwords will only allow you to compare each document to all the documents as a whole.

## How to read the results
Only the top 20 statistically significant topwords (absolute values larger than 1.96) are shown. A larger positive z-score indicates a token in this document or class is used more frequently than in the comparison group and a larger negative z-score indicates a relatively rarely used token.
    
##Limitations: 
  1. Topwords assumes the distribution of token frequencies is a normal distribution (not the case for most data).
  2. Documents and/or document classes should have at least 100 tokens each. 

##Method for Test
Topword can seek unique tokens in a document or class relative to other documents or classes in three different ways:
1. Compare each document to all the documents as a whole: Compare the proportions of tokens in each document to the proportions of that token in the entire corpus (your current active documents). No class labels on the documents are needed here, so this option is always available.
2. Compare each document against other class(es): Comparing the proportion of each token in a document in one class to that in another class as a whole. Example: With two books (two classes), find topwords in every chapter (document) from one of the books compared to the entire other book (class). This option is only available when class labels are attached to your active documents.
3. Compare all the classes: Comparing the proportion of each token in one class to that in another class. Example: Find topwords between two books (classes). This option is only available when class labels are attached to your active documents.

##Advanced Culling

