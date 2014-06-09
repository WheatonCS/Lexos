# Lexos
# Summary
Lexos is an integrated workflow of tools to facilitate the
computational analyses of texts. Functionality provided includes
the ability to "scrub" texts (remove punctuation, lemmatize,
consolidate characters, remove stopwords, etc), cut or segment texts,
and a suite of options for analysis, including
creating and downloading Document Term Matrices (DTM) of token counts
(both word- and character-ngrams), making dendrograms (cluster analysis), 
bubble visualizations, and word clouds. More functionality is being added 
on an ongoing basis.

## System Architecture (in brief)
Lexos is written primarily in Python 2.7.3 using the Flask microframework,
based on Werkzeug and Jinja 2. A heavy dose of Javascript and CSS
is included. The INSTALLME file provides directions for setting up the
development environment for testing using localhost:5000 in your local browser.

## Contributors
Richard Neal proposed and designed our current architecture. 
Bryan Jensen is our current software lead. 
Clayton Rieck and Bryan upgraded our current UI components.
Significant contributions were made in Summer 2014 by
Bryan, Clayton, Scott Kleinman (CalState-Northridge), 
Jinnan Ge, Lithia Helmreich, Qi (Sara) Zhang, and Mark LeBlanc.
Previous iterations of our tools included contributions by
2013: Richard Neal, Bryan Jensen, Scott Kleinman, Devin Delfino, Julia Morneau, 
and Vicky Li;
2012: Alicia Herbert, Donald Bass, Doug Raffle, Christina Nelson, and Mike Kahn.
The majority of these developers are undergraduate students in the
Lexomics Research Group at Wheaton College (Norton, MA).
Computer Science professors Tom Armstrong and Mark LeBlanc oversee the software team.

## References
[Lexomics Research Group](http://lexomics.wheatoncollege.edu/ "Lexomics Research Group"), Wheaton College, Norton, MA.

[Lexos tools](http://lexos.wheatoncollege.edu "Lexos tools").

LeBlanc, M.D., Drout, M.D.C., Kahn, M., Herbert, A. '14, Neal, R. '14 (2013). ["Lexomics: Integrating the research and teaching spaces".](http://dh2013.unl.edu/abstracts/ab-293.html "DH 2013") Short paper presented at *Digital Humanities 2013*, University of Nebraska–Lincoln, July 17, 2013.

Drout, M.D.C., Kahn, M., LeBlanc, M.D., Nelson, C. '11 (2011). [Of Dendrogrammatology: Lexomic Methods for Analyzing the Relationships Among Old English Poems"](http://muse.jhu.edu/journals/journal_of_english_and_germanic_philology/summary/v110/110.3.drout.html), *Journal of English and Germanic Philology*, v110(3), July 2011, 301-336.


