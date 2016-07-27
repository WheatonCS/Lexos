#Finding the Top Words

Topwords allows you to ask what terms are more prominent in a certain document or class of documents than in other classes of documents or the collection as a whole. It uses a z-test to identify these terms, allowing you to configure the criteria for determining the bounds of statistical prominence. Options for limiting the proportions to use in an analysis include commonly used metrics such as Standard Deviation and Interquartile Range, as well the ability to use customizable bounds. Topwords leverages the power of [class labels](link to discussion of class labels) to documents in the [Manage](link to manage directions) tool. There, you can right-click and set the class on all active documents or set each document's class individually. If you do not assign class labels to your active documents, Topwords will only allow you to compare the proportions of each term in a single document to their proportions in the overall set of active documents in our collection.

## How to read the results
  1. Only the top 20 statistically significant terms (those for which the z-score has an absolute value larger than 1.96) are shown. 
  2. A larger positive z-score indicates a term in this document or class is used more frequently than in the comparison group.
  3. A larger negative z-score indicates a term that is used relatively rarely.
  
## Using Topword results in Rolling Window Analysis (RWA)
The unique terms identified here in Topwords make good candidates to use in Vizualize: [Rolling Window](link to RWA material).
    
##Limitations: 
  1. Topwords assumes the distribution of term frequencies is a normal distribution (not the case for most data).
  2. Documents and/or document classes should have at least 100 tokens each. 
  3. 

##Method for Test
Topwords can seek unique terms in a document or class relative to other documents or classes in three different ways:
1. Compare each document to all the documents as a whole: Compare the proportions of terms in each document to the proportions of that term in the entire corpus (your current active documents). No class labels on the documents are needed here, so this option is always available.
2. Compare each document against other class(es): Comparing the proportion of each token in a document in one class to that in another class as a whole. Example: With two books (two classes), find topwords in every chapter (document) from one of the books compared to the entire other book (class). This option is only available when class labels are attached to your active documents.
3. Compare all the classes: Comparing the proportion of each term in one class to that in another class. Example: Find topwords between two books (classes). This option is only available when class labels are attached to your active documents.

##Use These Terms
Lexos provides additional ways to cull the potential list of topwords. Use Topword's Advanced Culling options (and/or the Tokenize Culling Options) to limit the number of potential topwords. Topword's Advanced Culling options enable you to cull terms with certain frequencies. For example, assuming our tokens are words (1-gram tokens), the most frequently used words are the so-called function words (e.g. articles, prepositions) while the least frequently used words are context-specific words. These culling options allow you to seek topwords from only those terms whose frequencies satisfy one of three options: All (no culling), Built-in Options, or Customized Options.

1. All (default): This default option means that no reduction is applied, that is, topwords uses all the term proportions that appear in both groups.
2. Built-in Options: Choose to find topwords using samples of term proportions from built-in outlier ranges.
  1. Standard Deviation: Choose outlier region: all defined by the standard deviation from the mean on a normal distribution (bell-shaped curve) of frequencies of all terms.
    * Top Outliers Only: Only compare terms with rather high frequencies: +2&#963; standard deviations above the mean.
    * Non-Outliers Only: Only compare terms with mid-range frequencies: frequences within +/-1&#963; around the mean.
    * Low  Outliers Only: Only compare terms with rather low frequencies: +2&#963; standard deviations below the mean.
  2. Interquartile Range (IQR): Choose to find topwords using samples of term proportions using the InterQuartile Range (IQR). All term proportions are ranked in increasing order and then divided into four equal parts. The values that divide each part are called the first, second, and third quartiles, denoted by Q1, Q2, and Q3, respectively. Q2 is the median. The IQR is equal to Q3 minus Q1. Outlier regions for terms are defined as following:
    * Top Outliers Only: Only compare terms with unusually high frequencies which are at least 1.5 interquartile ranges above the third quartile (Q3).
    * Non-Outliers Only: Only compare terms that are not outliers, whose frequencies are below (Q3 + 1.5 IQR) and above (Q1 - 1.5 IQR).
    * Low Outliers Only: Only compare terms with unusually low frequencies which are at least 1.5 interquartile ranges below the first quartile (Q1).
3. Customize: Use terms only within a user-defined range of proportions or raw counts.
  1. Proportional Counts: Using all term frequencies, you can set the range of proportions to use: \[Low..High\]
  2. Raw Counts:  Using all absolute (integer) term counts. Using all term counts, you can set the range of counts to use: \[Low..High\]
