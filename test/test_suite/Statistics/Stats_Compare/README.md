# Stats Compare

In order to verify the correctness of the Lexos Statistics tool, we used two other tools
to compare data.

The tools used were:
- Voyant-Tools 
    * https://voyant-tools.org/
- Intelligent Archive 
    * https://www.newcastle.edu.au/research-and-innovation/centre/education-arts/cllc/intelligent-archive
    * Download required (best used with MacOS or other Java supporting OS)

### How to use Voyant

*Note:* Voyant does not scrub files, it counts the words as it appears in the original uploading files

1. Upload your file

2. In the summary window, there is a sentence describing the total words (e.g. This corpus has 1 document
 with 5,389 total words and 1,809 unique word forms). The total words should be equal to Lexos' count
 of Total Terms and Voyant's "unique word forms" should equal Lexos' "Distinct Terms"

3. The Vocabulary Density should be equal to Lexos' Vocabulary Density

4. On small documents (documents with 59 or less distinct terms) Voyant can find the number of Single-Occurance
terms by sliding the "items" scale all the way to the right and looking at the counts under "Most frequent
words in the corpus" in Voyant's "Summary" window. 

### How to use Intelligent Archive 

*Note:* Intelligent Archive provides a space to let users edit the words to exclude from the process

1. After opening the .jar file, click "Add New"

2. Give the file an Author and a Title

3. Click "Word Frequencies" and change "Block Method" to "Text" (If your file is in Chinese click "Segment by Character")

4. "Word Types" should equal Lexos' count of "Distinct Terms"

5. "Size" should equal the "Total Terms"

6. To count Single-Occurrence terms, set the "Output Size" to one of the other tests' distinct number of terms 
(the larger one) and count how many words have the frequency one

Test files:
- catCaterpillar: original
- catCaterpillar(scrubbed)

- DreamCH1: original
- DreamCH1(scrubbed)

- Fog(beginning): original
- Fog(beginning-scrubbed)

- Heart_of_Darkness: original
- Heart_of_Darkness(scrubbed)

- OnetoTen: original
- OnetoTen(scrubbed)

- War and Peace: original
- War and Peace(scrubbed)

Go to "STATS_Compare.csv" and "STATS_Compare.png" in folder ResultsToExpect for results.




