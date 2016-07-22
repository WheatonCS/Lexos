# Language Guide

The following glossary will be useful in developing documentation for Lexos or in producing other forms of public facing writing about Lexos. We should aim for as much consistency as possible.

**Text:** This term generally refers to a work of literature when it is being discussed as a literary phenomenon. As a data structure manipulated by Lexos, the term "document" should be used.

**File:** The storage form for a text or document which has been uploaded by the user.

**Document:** The text contained in a file *or* a segment of the text contained in a file.

**Segment:** A cut portion of a document. **Important: all segments are themselves documents.

**Token:** An individual string of characters that may occur any number of times in a document. Tokens can be characters, words, or n-grams (strings of one or more characters or words).

**Term:** The unique form of a token. If a **token** "cat" occurs two times in a document, the **term** count for "cat" is 2. In computational linguistics, terms are sometimes called "types", but we avoid this usage for consistency.

**Lemma:** The dictionary headword form of a term. For instance, "cat" is the lemma for "cat", "cats", "cat's", and "cats'".

**Word:** A term that is used somewhat imprecisely to refer to a token, a term, or a lemma, depending on the context. Since some Lexos users may be analysing characters or n-grams, we should avoid using the term "word" unless we are talking about a usage in which we are interpreting one of these character strings as equivalent to the semantic category of words.

**Document-Term Matrix (DTM)**: A matrix counting the counts (or proportions) of each term for each document.

**N-Gram**: A string of one or more tokens delimited by length. N-Grams can be characters or larger tokens (e.g. space-bounded strings typically equivalent to words in Western languages). A one-character n-gram is described as a 1-gram or uni-gram. There are also 2-grams (bi-grams), 3-grams (tri-grams), 4-grams, and 5-grams. Larger n-grams are rarely used.