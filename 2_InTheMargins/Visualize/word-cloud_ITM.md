Word clouds are a method of visualizing the **Document-Term Matrix**. They present terms arranged at angles for compactness, with each term sized according to its frequency within the text. Word clouds enable you to get a sense of the content in your corpus, and they are very good for presentations. However, they also have some well-known limitations (see the topics article on [visualizing texts with word clouds]()). In some languages, individual tokens may not correspond to words, which will limit the usefulness of this method of visualization.

The Lexos **Word Cloud** tool uses Jason Davies' excellent [word cloud generator for d3.js](https://www.jasondavies.com/wordcloud/)&mdash;with a few modifications&mdash; to create beautiful, interactive word clouds. This implementation scales the size to ensure all terms fit within the layout. The color used for each does not convey meaning and is used only for aesthetic purposes.

### Generating Word Clouds
Lexos allows you to choose some or all of your active documents from which to generate a word cloud. Once you have selected your documents using the checkboxes at the top right, click the **Get Graph** button. After a few seconds, a word cloud will fade into view (be patient if you have selected large or many documents). Running your mouse cursor over each term in the word cloud will generate a tooltip showing the number of times it occurs in the documents you have selected. Click on the **View Counts Table** button next to **Get Graph** or below the word cloud to open a dialog containing a searchable, sortable table of the term counts in your word cloud.

**Warning**: The d3.js algorithm used by Lexos has an important limitation. It attempts to layout terms in as compact a manner as possible and is sometimes unable to find a fit for high frequency words. In these cases, these words are dropped from the word cloud. Because of this limitation, we highly recommend that you view the Counts Table in order to make sure that all the most frequent words are represented in the word cloud. If you find that this is not the case, try generating the word cloud again. Sometimes it will find a better layout in which the high frequency words fit. Using the layout options described below may also allow you to produce word clouds in which the missing words fit within the layout.

### Layout Options
Davies' word cloud generator offers some useful ways to modify the layout using the controls below the graph. After modifying the settings, you can re-generate the word cloud by clicking anywhere on the graph. Each of the settings is described in detail below:

#### Spiral
This refers to the method of calculating the angles and placement of terms in the layout. The **Archimedean** setting uses the [Archimedean spiral](https://en.wikipedia.org/wiki/Archimedean_spiral) to determine the layout. The **Rectangular** setting attempts to place terms within a rectangular shape.

#### Scale
This refers to how individual terms are sized relative to one another in the word cloud. Settings are `log n` (logarithmic scale), `√n` (square root scale), and `n`, where `n` refers to the number of times an individual term occurs. `log n` and `√n` are methods of transforming this number based on the possible minimum and maximum values. No single scaling is inherently superior to the others, but they will produce different effects in the layout. Using the `n` scale setting will preserve the original proportionality of the values as far as possible. `log n` may aid the differentiation of data that is not uniformly distributed. The square root transformation will inflate smaller numbers but stabilize the size of larger ones.

#### Font
You can change the appearance of your word cloud by setting the font here. This feature should work with any font installed on your system.

#### Orientation Settings
In the middle of the **Layout Options** controls is a form to set the number of different orientations terms can have in the layout. You can also set the range of angles, either by setting the number of degrees in the form fields or by dragging the angles in the image below them. 

#### Number of Words
By default, Lexos includes the top 250 terms in your documents. Use this setting to modify the number. Limiting the number of terms may help you to include high frequency terms which are dropped by the layout algorithm.

#### Download
Word clouds are downloadable in either SVG or PNG format. SVG images are very useful because they scale well in web browsers. If you click the SVG button, a new window will open with a copy of your word cloud. Use your browser's **Save as...** function to save the web page. If you click the PNG button, the image will open in a new window. The procedure for saving a PNG image is not standard in all browsers, so follow the instructions you see on the screen. 