#### Tokenize
By default Lexos splits strings of text into tokens every time it encounters a space character. For Western languages, this means that each token generally corresponds to a word. Click the **by Characters** radio button to treat every character as a separate token. If you wish to use n-grams, increase the **1-gram** incrementer to 2, 3, 4, etc. For example, "the dog ran" would produce the 1-gram tokens _the_, _dog_, _ran_., the 2-grams _the dog_, _dog ran_, and so on. 2-grams tokenized by characters would begin _th_, _he_, _e&nbsp;_, and so on.

Note that increasing the n-gram size my produce a larger DTM, and the table will thus take longer to build.

#### Culling Options
"Culling Options" is a generic term we use for methods of decreasing the number of terms used to generate the DTM based on statistical criteria (as opposed to something like applying a stopword list in **Scrubber**). Lexos offer three different methods:

1. **Most Frequent Words**: This method takes a slice of the DTM containing only the top N most frequently occurring terms. The default setting is 100.
2. **Culling**: This method builds the DTM using only terms that occur in at least N documents. The default setting is 1.
3. **Greywords**: This method removes from the DTM those terms occurring in particularly low frequencies. Lexos calculates the cut-off point based on the average length of your documents.
[more elaborate: This method removes from the DTM those terms that occur in particularly low frequencies across all active segments. For each segment, Lexos calculates a low-frequency, cut-off point and notes those terms with frequencies less than this boundary. If a term falls below the boundary in every segment, this term is considered to be a "non-functioning" (or grey) word and is removed from the DTM.]

#### Normalize
By default, Lexos displays the frequency of the occurrence of terms in your documents as a proportion of the entire text. If you wish to see the actual number of occurrences, click the **Raw Counts** radio button, followed by the **Regenerate Table** button. You may also attempt to take into account differences in the lengths of your documents by calculating their [Term Frequency-Inverse Document Frequency (TF-IDF)](https://en.wikipedia.org/wiki/Tf%E2%80%93idf). Lexos offers three different methods of calculating TF-IDF based on **Euclidean Distance**, **Manhattan Distance**, or without using a distance metric (**Norm: None**). For further discussion on these options, see the topics article on [TF-IDF](http://scalar.usc.edu/works/lexos/tf-idf).

#### Assign Temporary Labels
Lexos automatically uses the label in the "Document Name" column in the **Manage** tool as the document label. However, you may change the label used in your table by entering a new value for it in the forms displayed in **Assign Temporary Labels**. This is particularly useful if you want to save different labels when you download your DTM. Keep in mind that whatever labels you set will be applied in all other Lexos tools that use the Advanced Options. However, the original document name in **Manage** will not be affected. After assigning temporary labels in **Tokenizer**, click the **Regenerate Table** button to rebuild the table with the new labels.