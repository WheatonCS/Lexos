The Lexos **Statistics** tool provides a basic overview of statistical content in your collection,
in addition to the specific term counts/proportions available in the Document-Term Matrix (DTM) provided in **Tokenizer**.

**Statistics** generates a table containing the number of distinct terms, the number of
terms occurring once (_hapax legomena_), the total term count, and the average term frequency
in each document. You may generate statistics on all of your active files or you may select a subset
of your active documents by using the **Select Document(s)** checkboxes. All of the [Advanced Options](advanced-options)
for manipulating the Document-Term Matrix (DTM) are available. When you have chosen your settings,
click the **Generate Statistics** button.

### Using the Statistics Table
The statistics table may be sorted by column by clicking on the column headers.
An icon will indicate which column is being used for sorting and whether the sort
direction is ascending or descending.
(Note: the first click will sort that column in increasing order; click again to sort in decreasing order.)
Use the **Display** dropdown menu to display
more than the default 10 rows per page. The statistics table may be copied to your computer's
clipboard by clicking the **Copy** button. It may also be downloaded as an Excel spreadsheet,
Comma-Separated Values (CSV) file, Tab-Separated Values (TSV) file, or a PDF.

### Statistics for the Entire Corpus
When you generate the statistics table, Lexos also calculates the average,
median, and interquartile range (IQR) of your documents' sizes (based on term counts).
This information is used to
determine if any of the document sizes are anomalously large or small, that is, if any of your document sizes are outliers.
Outliers are those document sizes that fall below Q1 - 1.5(IQR) or above Q3 + 1.5(IQR) [https://en.wikipedia.org/wiki/Interquartile_range].
Following a display of the average and median values, Lexos provides a warning for each document with
a size that is particularly large or small compared to the rest of your corpus.
You should consider removing outlier documents from subsequent analyses and/or consider additional cutting
of some documents to make term counts more uniform.