

## Ribbon Diagrams and Document Location Mapping
A "ribbon diagram" is a type of visualisation that will help us make sense of iterative cluster analysis. Essentially, it consists of rows of documents organised by cluster membership. These rows are supplemented by the page or poetic line numbers of the original text and perhaps user-annotations helping to classify the clusters.

We have also been using "ribbon diagram" as a kind of shorthand for the structural changes needed to implement the visualisation, changes that can also be used to produce other types of functions such as a reader that displays the original text prior to scrubbing. I call the central component of these changes "document location mapping", although "indexing" might be an appropriate term. Essentially, document location mapping means that a sequence of tokens in a scrubbed text can be mapped to a span in the original text, along with any associated milestones. Hence the original page or line numbers, along with the original text, can be displayed by Lexos for any scrubbed document. This ability is essential for generating the ribbon diagram, but, once in place, it could be available for any Lexos tool. For instance, Document Location Mapping would thus allow us to display original page and line numbers in dendrograms and rolling windows. Currently, we can only do this if we cut by milestone. We'll want to expand this functionality to transform xml tags into milestones so that, for instance, a TEI text with chapter divisions can be used.

Ideally, we'd have some sort of index that keeps track of the token ranges for the divisions in the current session. The main challenge is that, once a document is scrubbed and/or tokenised, its feature vector is not the same as the original. Sometimes the token count can be significantly reduced (or occasionally increased). So mapping token ranges onto document strings becomes a sequence alignment problem. The discussion below provides some ideas about how we might implement this.

Before going on, it is worth stating that the proposed solutions address many other issues in the Lexos workflow and are useful for other types of functionality.

## Workplace Storage
As a first step, we would move the workspace storage format from pickle to JSON. This will provide better processing speeds and greater interoperability with other tools. In order to address document location mapping issues, the JSON serialisation would provide keys for the start and end positions in documents. Here is an example of the relevant portion of a workspace file:

```json
{
	"document": [{
		"id": 0,
		"label": "Doctor Faustus",
		"startPos": 0,
		"endPos": 400,
		"segments": [{
			"id": 1,
			"startPos": 0,
			"endPos": 200
		}, {
			"id": 2,
			"startPos": 201,
			"endPos": 400
		}],
		"milestones": [{
			"id": 1,
			"startPos": 0,
			"endPos": 200
		}, {
			"id": 2,
			"startPos": 201,
			"endPos": 400
		}],
		"milestoneLabel": "page"
	}]
}
```

This is a single document cut into two 200-token segments. Note that we record the positions of the starting and ending tokens for each segment. In this version, we have cut the document at each page, so we record the start and end positions for each page in the document. For the output, we record a `milestoneLabel`, which might be "line", "chapter", or some other term defined by the user. Whenever the user scrubs or cuts their documents, this JSON structure is updated with new starting and ending positions. The information in this structure is then used in tandem with a pandas dataframe containing the token sequence.

## Pandas Dataframe
When a file is uploaded, Lexos will automatically construct a pandas dataframe with the token sequence, using default tokenisation rules. Should the user change the settings, the dataframe will be reconstructed. When Lexos produces a DTM, it will work from the token sequence in the dataframe, **not the original text file**. As a result, the original file will be untouched and will preserve all its original formatting. The dataframe would look something like this:

| pos  | token    | term     |
|------|----------|----------|
| 0    | Was      | was      |
| 1    | this     | this     |
| 2    | the      |          |
| 3    | face     | face     |
| 4    | that     | that     |
| 5    | launched | launched |
| 6    | a        |          |
| 7    | thousand | thousand |
| 8    | ships    | ships    |
| 9    | ?        |          |
| etc. |          |          |

Here "pos" is the position of the token in the token sequence before any scrubbing. "token" is the original form of the token before scrubbing. "term" is a countable version of the token **after** scrubbing. Note that stop words, stripped punctuation, etc. are NULL (I think pandas actually represents this as N/A, if I recall).

In earlier versions of this schema, there were further columns for documents, segments, and milestones, but I think it is more memory efficient to use the information in the workspace JSON array to select slices of the dataframe, rather than storing the information in the dataframe itself.

Hence, if the user wanted to construct a DTM from an unscrubbed version of the text above, Lexos would grab the `tokens` column; otherwise, it would grab the `terms` column. If they cut the document, Lexos would iteratively grab slices from the starting and ending positions of each segment as recorded in the JSON array. This is relatively easy to do in pandas.

Because the starting and ending positions for the **unscrubbed** text are recorded when Lexos constructs the DTM, it should always be possible to display the original token sequence and its milestones. A side benefit of all this, is that it would be really easy to implement an "Undo Scrubbing" option (although multiple undos would still be tricky).

This solves the problem of mapping segments onto the original page or line numbers from which they are derived. However, we don't really want to explain the original token sequence; we want to display the original _text_&mdash;with all its paragraph line breaks and other white space. This is extremely tricky. Two possible approaches are inserting tags in the original file and detecting position based on diff between the original file and the token sequence. Both are probably going to fail occasionally because of whitespace issues.

## Indexing with Whoosh as an Alternative or Supplementary Approach
This last issue has been tackled by software designers working on search and retrieval technologies, and it may be worth investigating their solutions. Probably the easiest to implement in a Python environment is [Whoosh](https://whoosh.readthedocs.io/en/latest/). Whoosh is a programmer library for creating a search engine. Whoosh lets you index free-form or structured text and then quickly find matching documents based on simple or complex search criteria. It uses search engine ranking algorithms to identify key words in the original text, and this may be an effective method of grabbing the correct portion of the original text from a known token sequence. 

Whoosh can store all sorts of information about term positions in the original document, which that it is worth exploring whether it can function in the same capacity as the pandas dataframe proposed above. Additionally, Whoosh ca apply stop word filters, accent folding, different types of tokenization, stemming, lemmatization, and so on. While this duplicates Lexos scrubbing features, it may be worthwhile to partially re-implement and enhance them through Whoosh. I have identified the following pages in the documentation as useful reading:

* [Stemming](http://whoosh.readthedocs.io/en/latest/stemming.html)
* [Advanced Schema Setup](http://whoosh.readthedocs.io/en/latest/schema.html#advanced-schema-setup)
* [Recipes--Global Information](http://whoosh.readthedocs.io/en/latest/recipes.html#global-information)

## Additional Issues
These are not issues that relate to the core challenges of document location mapping, but things that came up in the course of investigation.

### CJK Tokenisation
[TinySegmenter](http://masatohagiwara.net/tinysegmenter-in-python.html) seems like an easy-to-implement. The author claims that his Javascript project, [Rakuten MA](https://github.com/rakuten-nlp/rakutenma) is better, but it's not feasible for us to do this on the client side (maybe someone wants to port it to Python?).

### Workspaces and Projects
The sample JSON above only demonstrated portion of the workspace file devoted to handling token sequences and milestones. But we might consider how to structure the workspace JSON file as a whole in a way that makes workflow transparent and enhances interoperability.

Consider that a workspace is a snap shot of the state of Lexos at a given moment. Schematically, it contains a record of the user's Collection, Processes (Lexos option settings), and any Outputs (such as data or images). Ideally, a user saving the workspace would be able to supply some metadata, such as the author, the date, and the project to which the workspace belongs.

Projects don't exist within Lexos. They are just a way of archiving multiple related Lexos workspaces. Lexos could do a lot with this information, but the lowest hanging fruit would be to insert project metadata in the workspace metadata. An external script could grab that information from the workspace JSON file and, for instance, create a "manifest" of workspaces under a single project heading.

Here is a sample workspace excerpt, reresented in YAML, rather than JSON, for readability. The user has generated a word cloud after removing stop words. The workspace was last saved on January 2, and the user wants it associated with a project created on January 1.

```yaml
- name: workspace0
- metadata:
  - project: MyProject
    - author: Scott Kleinman
    - date: 2017-01-01
  - date: 2017-01-02
- collection:
  - doc1
  - doc2
- processes:
  - scrubbing:
    - stopwords-removed: True
- outputs:
  - images:
    - wordcloud.png
```

The reason for associating a workspace with a project is that a user can have a project called "My Beowulf Project", which might contain several workspaces generated as part of a study of _Beowulf_.