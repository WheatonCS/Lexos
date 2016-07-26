#Finding the Top Words

Topwords identifies tokens that appear with unique proportions when compared to other collections. The method uses a proportional z-test to identify tokens in documents or document classes with proportions significantly differently from those same tokens in all documents or document classes. Topwords allows you to ask what tokens (words) appear abundantly more in one document than all other documents? What tokens appear most infrequently in one document than others? If we attach [class labels](link to discussion of class labels) to collections of documents (classes), what tokens appear abundantly (or infrequently) in one class vs. proportions found in other classes? 

Note: when comparing some documents to a group (class) of other documents, you will need to assign class labels to each document. In the [Manage](link to manage directions) page, you can right-click and set the class on all active documents or set each document's class individually. If you do not assign class labels to your active documents, Topwords will only allow you to compare each token proportions in one document to all the documents as a whole.

## How to read the results
  1. Only the top 20 statistically significant topwords (z-score absolute values larger than 1.96) are shown. 
  2. A larger positive z-score indicates a token in this document or class is used more frequently than in the comparison group.
  3. A larger negative z-score indicates a relatively rarely used token.
  
## Where next? Using topwords in Rolling Window Analysis (RWA)
The unique words identified here in Topwords make good candidates to use in Vizualize: [Rolling Window](link to RWA material).
    
##Limitations: 
  1. Topwords assumes the distribution of token frequencies is a normal distribution (not the case for most data).
  2. Documents and/or document classes should have at least 100 tokens each. 
  3. 

##Method for Test
Topword can seek unique tokens in a document or class relative to other documents or classes in three different ways:
1. Compare each document to all the documents as a whole: Compare the proportions of tokens in each document to the proportions of that token in the entire corpus (your current active documents). No class labels on the documents are needed here, so this option is always available.
2. Compare each document against other class(es): Comparing the proportion of each token in a document in one class to that in another class as a whole. Example: With two books (two classes), find topwords in every chapter (document) from one of the books compared to the entire other book (class). This option is only available when class labels are attached to your active documents.
3. Compare all the classes: Comparing the proportion of each token in one class to that in another class. Example: Find topwords between two books (classes). This option is only available when class labels are attached to your active documents.

##Advanced Culling
Lexos provides additional ways to cull the potential list of topwords. Use Topword's Advanced Culling options (and/or the Tokenize Culling Options) to limit the number of potential topwords. Topword's Advanced Culling options enable you to cull tokens with certain frequencies. For example, assuming our tokens are words (1-gram tokens), most frequently used words are  the so-called functional words while the least frequently used words are context-specific words. These culling options allow you to seek topwords from only those tokens who frequencies satisfy one of three options: All (no culling), Built-in Options, or Customize.
1. All (default): This default option means that no culling is applied, that is, topwords uses all the token proportions that appear in both groups.
2. Built-in Options
  1. Standard Deviation: Cull outliers by the standard deviation from the mean on a normal distribution (bell-shaped curve) of the frequencies of all tokens.
   * Use Top Outlier Only: Only compare words with rather high frequencies. 2 standard deviations above mean.  
   * Use Non Outlier Only: Only compare words with not too high or too low frequencies. Within 2 standard deviations from Mean.  
   * Use Low Outlier Only: Only compare words with rather low frequencies. 2 standard deviations below mean.  
