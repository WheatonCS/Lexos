# Description of Ribbon Diagram

We're calling this tool "Ribbon Diagram", but it is really an indexing function that could eventually be used for a variety of purposes, including producing diagrams. The schema for a Lexos index would be something like the list of dictionaries below:

```python
[
	{id: 0, token: "The", counted: true, document: 1, segment: 1, chapter: 1, page: 1},  
	{id: 1, token: "quick", counted: true, document: 1, segment: 1, chapter: 1, page: 1},  
	{id: 2, token: "brown", counted: true, document: 1, segment: 1, chapter: 1, page: 1}, 
	{id: 3, token: "fox", counted: true, document: 1, segment: 1, chapter: 1, page: 1}, 
	{id: 4, token: "jumped", counted: true, document: 1, segment: 1, chapter: 1, page: 1},  
	{id: 5, token: "over", counted: true, document: 1, segment: 1, chapter: 1, page: 1}, 
	{id: 6, token: "the", counted: true, document: 1, segment: 1, chapter: 1, page: 1},  
	{id: 7, token: "lazy", counted: true, document: 1, segment: 1, chapter: 1, page: 1},  
	{id: 8, token: "dog", counted: true, document: 1, segment: 1, chapter: 1, page: 1},  
	{id: 9, token: ".", counted: false, document: 1, segment: 1, chapter: 1, page: 1},  
	{id: 10, token: "He", counted: true, document: 1, segment: 1, chapter: 1, page: 1},  
	{id: 11, token: "escaped", counted: true, document: 1, segment: 2, chapter: 1, page: 1},  
	{id: 12, token: ".", counted: false, document: 1, segment: 2, chapter: 1, page: 1}
]
```
**Notes:**
1. The `counted` Boolean is used to determine whether the token is used by Lexos in its token counts. For instance, a user may scrub punctuation before cutting, clustering, etc., but the index will keep track of its original location. See notes below on preserving the original text.
2. The `segment` property is created when the user cuts the original document. This leads to an issue with when the index is created and maintained. Obviously, scrubbing will require the Boolean to be flipped in some cases and cutting will require the addition of the `segment` property.
3. In the above example `chapter` and `page` are provided as possible structural divisions. Other structural divisions, such as poetic lines, might be used, but these would have to be provided by the user in the uploaded document. The last stage of development for the xml handling function will be to convert angle-bracket tag delimiters into milestones for cutting properties for indexing. The index function should also be able to include our current milestone regex patterns as non-counted tokens.
4. The user could presumably annotate sections of their text with tags like `<monster-slaying></monster-slaying>`, which the Lexos could then map to other structural divisions. Eventually, it would be possible to do the reverse on the front end: the user would select a range of text or segments, give it a name, and the annotation would be added to the index.

# Preserving the Original Text
An important feature of the tool would be to map scrubbed and cut documents to the original text. For instance, a simple token list after scrubbing punctuation might be considerably shorter than the unscrubbed text. Let's say the user scrubbed the text in the example above and cut it into segments every ten tokens. Segment 1, as analysed in, say, a dendrogram, would be based on a token list with 10 items: `["the", "quick", "brown", "fox", "jumped", "over", "the", "lazy", "dog", "he"]`. However, if he wanted to know what this corresponded to in the original *text*, the answer would be "The quick brown fox jumped over the lay dog. He". So it is important to maintain the original document and to be able map token, segment, or other types of ranges onto it based on information in the index.

Currently, we de-activate the original document when we cut it into segments. If the user decides to delete the original document, we need to check whether it has any child segments and preserve a hidden copy if it does. Scrub appears to modify the original file, so we may need to create a scrubbed copy to function as a child of the original document.

# Dealing with the Size of the Index
This part is potentially scary. Index files could be extremely large and slow to parse. Ideally, documents would be indexed when the file is uploaded and then updated whenever scrubbing and cutting takes place. Since this could be slow, we could give the user the option to turn off indexing in the settings dialog. Another option is to provide an indexing tool to which the user would go when they were ready to create an index an use its functionality.

# Next Steps
Feel free to update this document with other thoughts and ideas.
