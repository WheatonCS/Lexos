# Workflow for Authoring _In the Margins_ Pages

## Transferring Issues from GitHub
Discussion in GitHub issues often ends with a recommendation that the issue be documented in _In the Margins_. In these cases, the issue should be labelled with the "In the Margins" label. Periodically, issues with this label should have the recommendation transferred to an appropriate "working notes" file in the `InTheMargins` folder. The GitHub issues can then be closed, as the recommendations is now part of the _In the Margins_ authoring pipeline.

## Working Notes Files
Each tool in Lexos has a corresponding file in the `InTheMargins` folder. This file contains an account of the tool's features and options. It also contains recommendations for changes to labels and tooltips, or other UI features, along with general observations or questions. _In the Margins_ pages will be developed from the working notes files once any bugs or issues they identify in Lexos are resolved.

## _In the Margins_ Pages
_In the Margins_ pages are draft version of Scalar. They are generally stored as Markdown documents in the `InTheMargins` folder, but they may also be other types of media, such as images (which can be independent nodes, or "pages" in Scalar). An _In the Margins_ page should be identified with the suffix `_ITM`. Wherever possible, this should be added to the intended Scalar slug. For instance, for the Scalar page `http://scalar.usc.edu/works/lexos/similarity-query`, the corresponding _In the Margins_ draft file would be called `similarity-query_ITM.md`.

### Types of _In the Margins_ Pages
The working notes file should form the framework for an _In the Margins_ page to be placed in the Scalar path called "The Lexos Workflow". This path will contain documentation of each tool with an emphasis on describing its features and how the tool should be used.

Certain portions of the working notes file may provide material for other pages dealing with more in-depth issues. These may be concerned with de-black boxing algorithms, exploring the implications of choosing certain options, and so on. These are pages that will go in the Scalar path called "Topics". _In the Margins_ pages can include intended links between pages on the two paths.

Some _In the Margins_ pages may be static media files such as images, which other are embedded in other _In the Margins_ pages.

There is no need to distinguish between different types of _In the Margins_ pages in the file name. If it is not clear which path the page should be placed on, a notation can be made at the top of the file.

**Important:** When authoring material for _In the Margins_ pages, be sure to observe the language conventions documented in the [Language Guide](LanguageGuide.md).

## Transferring _In the Margins_ pages to Scalar
Authoring _In the Margins_ pages in Markdown makes the process easier and ensures consistency. However, the material should be transferred to Scalar in HTML format. Individual files can be converted to HTML quickly by pasting the Markdown into an online form at [http://pandoc.org/try/](http://pandoc.org/try/). If batch conversion is needed this can be scripted in [Pandoc](http://pandoc.org/).

HTML files can then be pasted into the Scalar web editor when a Scalar page is created. (Media files can be imported using Scalar's "Import Local Media" function.) _In the Margins_ pages can be batch imported to Scalar, but this requires creating a CSV with header fields from Scalar ontologies as defined in [Scalar's API Reference](http://scalar.usc.edu/works/guide/working-with-the-api?path=advanced-topics).

**Important:** Authoring in Markdown will help keep the HTML as clean and simple as possible, but the HTML may be modified by Scalar's web editor. It is important to double check all formatting once the page has been saved in Scalar.

## Organising Content in Scalar
Scalar content is non-linear, and each page or media object is a node (also called a "page") that can be linked to and have links to any other page. Nodes can also contain paths or be placed on paths, which contain sequences of links designed to direct a user to read pages in a particular order. The method of constructing links to pages and paths is described in the [Scalar documentation](http://scalar.usc.edu/works/guide/quickstarts); however, it might be a good idea to develop a more concise set of instructions here.