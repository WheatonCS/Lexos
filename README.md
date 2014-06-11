# Lexos
# Summary
Lexos is an integrated workflow of tools to facilitate the computational analyses of texts, presented in a web-based interface. Functionality provided includes the ability to "scrub" texts (remove punctuation, lemmatize, consolidate characters, remove stopwords, etc), cut or segment texts, and a suite of options for analysis, including creating and downloading Document Term Matrices (DTM) of token counts (both word- and character-ngrams), making dendrograms (cluster analysis), rolling-window analyses of word usage, bubble visualizations, and word clouds. More functionality is being added on an ongoing basis.

## Audience
From the start, we have worked hard to build a workflow that is (i) easy to use, (ii) accepts texts in most languages, 
including non-Western character sets, and (iii) serves as a platform for teaching and learning the science and 
art of text mining. For example, we presently use Lexos in our interdisciplinary undergraduate digital humanities course 
[Computing for Poets](http://wheatoncollege.edu/lexomics/educational-material/).
Lexos is not intended for advanced text mining work such as might be accomplished by 
users of higher-end statistical languages like R (although those users might benefit from its pre-processing functions). 
Lexos functions are implemented in Python, which continues to impress us as an alternative to R, and our research group has made 
significant discoveries using tools with Lexos tools (see 
[References](http://wheatoncollege.edu/lexomics/publications-grants/).

## System Architecture (in brief)
Lexos is written primarily in Python 2.7.3 using the 
[Flask](http://flask.pocoo.org/) microframework, based on Werkzeug and Jinja 2. 
A heavy dose of Javascript and CSS is included on the front-end. We increasingly incorporate the wiz from 
[D3.js](http://d3js.org/) in our visualizations and the power in the 
[scilearn-kit](http://scikit-learn.org/stable/) modules for text and statistical processing. 
The INSTALLME file provides directions for setting up the development environment for testing (using localhost:5000) on your local machine.

## Dependencies
chardet, flask, matplotlib, numpy, pip, scikit-learn, scipy

## Contributors
Richard Neal proposed and designed our current architecture. Bryan Jensen is our current software lead. 
Clayton Rieck and Bryan upgraded our current UI components. Significant contributions were made in Summer 2014 by Bryan, 
Clayton, Scott Kleinman (California State, Northridge), Jinnan Ge, Lithia Helmreich, Qi (Sara) Zhang, and Mark LeBlanc. 
Previous iterations of our tools included contributions in 2013 by: Richard Neal, Bryan Jensen, Scott Kleinman, Devin Delfino, 
Julia Morneau, and Vicky Li; and in 2012 by: Alicia Herbert, Donald Bass, Doug Raffle, Christina Nelson, and Mike Kahn. The 
majority of these developers are or were undergraduate students in the Lexomics Research Group at Wheaton College (Norton, MA). 
Computer Science professors Tom Armstrong and Mark LeBlanc oversee the software team.

## License information
See the file LICENSE for information on the
terms & conditions for usage and a DISCLAIMER OF ALL WARRANTIES.

## References
[Lexomics Research Group](http://lexomics.wheatoncollege.edu/), Wheaton College, Norton, MA.

[Lexos tools](http://lexos.wheatoncollege.edu).

LeBlanc, M.D., Drout, M.D.C., Kahn, M., Herbert, A. '14, Neal, R. '14 (2013). ["Lexomics: Integrating the research and teaching spaces".](http://dh2013.unl.edu/abstracts/ab-293.html) Short paper presented at *Digital Humanities 2013*, University of Nebraska–Lincoln, July 17, 2013.

Drout, M.D.C., Kahn, M., LeBlanc, M.D., Nelson, C. '11 (2011). [Of Dendrogrammatology: Lexomic Methods for Analyzing the Relationships Among Old English Poems"](http://muse.jhu.edu/journals/journal_of_english_and_germanic_philology/summary/v110/110.3.drout.html), *Journal of English and Germanic Philology*, v110(3), July 2011, 301-336.


