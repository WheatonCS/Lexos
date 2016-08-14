The Lexos **Cutter** tool allows you to divide your texts into multiple segments. Each segment is treated by Lexos exactly like any other document. You can perform individual scrubbing actions, create word clouds of segments, and cluster the segments of documents just as you would any other text.

### Cutting Options
Lexos gives you numerous options for designating where document should be cut into segments. The options are detailed below.

#### Characters/Segment
This option allows you to designate the number of characters you wish to be included in each segment. When the **Characters/Segment** radio button is clicked, the **Segment Size**, **Overlap**, and **Last Segment Size Threshold** options become visible. **Segment Size** refers to the number of characters you wish to include in each segment. Lexos will begin a new segment when it reaches the number of characters you designate before starting over at the next segment. **Overlap** allows you to specify an area of overlap between each segment. For instance, if you choose a segment size of 1000 characters and an overlap of 10 characters. Segment 1 will end at 1000 and Segment 2 will begin at 990. The **Last Segment Size Threshold** option provides a method of handling circumstances where the final segment does not reach the number of characters in the designated segment size. The default setting is to treat this final segment as a separate segment if it is 50% or more of the length of the designated segment size. If not, the entire final segment will be attached to the previous one. Changing the **Last Segment Size Threshold** percentage allows you to customize this behavior.

#### Lines/Segment
If your documents contain line breaks, you may use them to indicate where Lexos performs cutting actions. The **Segment Size** option allows you to choose the number of lines after which Lexos will perform a cut. All the other options work exactly the same as for the **Characters/Segment** option, except that they work by counting lines instead of characters.

#### Tokens/Segment
Lexos can perform cutting actions based on the number of tokens per segment. By default, it treats space-separated strings of characters as tokens, but this behavior can be modified by changing the settings in the **Tokenizer** tool. This will allow you to use n-grams as your tokens. Apart from using tokens as the unit for measuring segment size, all other options work exactly the same as for the **Characters/Segment** option.

#### Segments/Document
This option divides documents into a designated number of evenly-sized segments, regardless of the length of the document. Where the last segment is shorter than the others, Lexos applies a 50% **Last Segment Size Threshold** percentage as described under **Characters/Segment** above.

#### Cut by Milestone
This option allows you to assign a text string occurring in the document to use as a delimiter between segments. Typically, these "milestone" strings will be placed at appropriate locations in text files before they are uploaded to Lexos. For instance, you might add the string "CHAPTER" at the beginning of every chapter in a novel and then supply "CHAPTER" as the milestone term. Lexos will then perform a cut everytime it encounters this term, allowing you to divide your novel into individual documents for each chapter. Note that you must be careful to select a milestone term that does not occur anywhere as part of the text of your documents. Milestones are not counted as terms in the Document-Term Matrix (DTM).

### Cutting your Documents
Once you have selected the cutting options you desire, click the **Preview Cuts** button to see the results in the preview window. If you are happy with the cuts performed by Lexos, click the **Apply Cuts** button. This will create new documents with the same name as the original followed by a number for each segment. Each segment will appear as a new document in the **Manage** tool. Once cutting is applied, the original document is de-activated and the new segments are made active documents. In addition, once cuts are applied, each segment acquires an **Individual Options** button in the preview window. Clicking this button opens a version of the cutting options form in the main Cutter tool which allows you to apply cuts to each segment individually.

You can download the new document segments by clicking the **Download Cut Files** button.