# STATS COMPARE

We want to check whether the counting on STATS page work for large files and whether the data come out are correct, so we used two other tools to compare the result.

The two other tools are: 
- Voyant-Tools - [Link](https://voyant-tools.org/)
- Intelligent Archive - [Link](https://www.newcastle.edu.au/research-and-innovation/centre/education-arts/cllc/intelligent-archive)
    - need download to use (if possible try it on a mac since it was written in JAVA, otherwise you will need an operating system that supports Java)

Need to know:
- Voyant does not do scrubbing stuff, it counts the words as it appears in the original uploading files
    - How to Use:
        - Upload the file
        - In the lower left-hand corner under the summary, there should be the total words and unique word forms (Distinct Number of Terms)
        - The Vocabulary Density should be the inverse of the Average Number of Terms
        - On small documents (documents with 59 or less distinct number of terms) can find under Most frequent words in the corpus the number of terms occurring once if you slide the bar in the lower left-hand all the way to the right
- Intelligent Archive provides a space to let users edit the words to exclude from the process
    - How to Use:
        - After opening the .jar file, click Add New in the lower left-hand corner
        - The file has to have an Author and a Title (It doesn't matter what it is)
        - Click Word Frequencies and change Block Method to Text (If Chinese click Segment by Character)
        - Word Types should equal Distinct Number of Terms
        - Size should equal the Total Number of Terms
        - Can count the number of terms occurring once by setting the Output Size to one of the other tests' distinct number of terms (the larger one) and count how many words have the frequency one

Test files:
- catCaterpillar: original
- catCaterpillar(no_punc&lowercase&no_digits): scrubbed

- DreamCH1: original
- DreamCH1(no_punc&no_whitespace): scrubbed

- Fog(beginning): original
- Fog(beginning-no_punc&no_whitespace): scrubbed

- Heart_of_Darkness: original
- Heart_of_Darkness(no_punc&lowercase&no_digits): scrubbed

- OnetoTen: original
- OnetoTen(no_whitespace): scrubbed

- War and Peace: original
- War and Peace(no_punc&lowercase&no_digits): scrubbed

Go to "STATS_Compare.ods" in folder ResultsToExpect for results.
- The version of Intelligent Archive I used, the Segment by Character didn't work so that's why for the Mandarin documents the Intelligent Archive row is blank




