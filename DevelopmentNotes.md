# Development Notes
# Navbar
The navbar has been replaced with a Bootstrap navbar, which required a litle bit of Javascript tweaking to allow the banner to be displayed above it. Bootstrap 3 disallows the flyout submenus required for the Clustering menu items, so this functionality is reintroduced using the SmartMenus plugin. The plugin generates a console message of `SyntaxError: expected expression, got '.'`, but it appears to function correctly.

Bug: The navbar expands to full screen width when you scroll down, a behaviour that did not manifest in the original local test site. Something was not copied over correctly, so this needs to be investigated. 

# Upload
This page is partially converted to Bootstrap. Everything is laid out in the Bootstrap grid, but the old progress bar is still used. I had trouble achieving the same effect with the Bootstrap progress bar, but it could probably be done with some more work.

# Manage
This replaces the old Select page. Everything is laid out in the Bootstrap grid. Additionally, the table is set up using the newest version of DataTables (which now has Bootstrap styling) loaded from CDN. You can no longer drag select multiple rows, but the shift- and control-click behaviour is now much more consistent. The old right-click context menu has been replaced with a Bootstrap-based plugin with the same functionality.

The new version of DataTables has a built-in natural sorting function, which I haven't yet implemented. Intriguingly, it also has sorting functions for other languages, such as Chinese, French, and Turkish. These could be implemented as part of a localisation scheme.

Note: The search function works only on the client-side so that only the excerpts are searched. It _is_ possible to search on the server-side with an ajax request (I have this functioning in Tokenize), but I am unsure whether it would be faster to loop through all the files and return the file IDs of those which match the string or whether to construct a DTM and query against it. DataTables sends an Ajax request for every keystroke, so this could be an expensive, is useful function.

# Scrub
Provisionally laid out using the Bootstrap grid. Bootstrap tooltips added. Some work needs to be done on the file upload button placement. I am very dissatisfied with the current implementation of the Preview, Apply, and Download buttons, so I moved them to the top right and applied the Bootstrap affix function, which fixes their position when the screen is scrolled. There's a small bug, as it is pinned to the right side of the screen, rather than the container, so that must be fixed if new position is acceptable. These buttons now call ajax functions to avoid page re-loading. The previews are now displayed in a Bootstrap panel, which I think looks pretty snazzy. Right-clicking the document names might trigger the same preview function used in Manage to display the full preview, for added usefulness.

# Cut
This screen uses the same basic layout template as Scrub, so it reflects the new placement of the Preview, Apply, and Download buttons. Also, the functions these buttons call need to be changed to ajax calls to avoid page re-loading. The layout of the individual features has been fully converted to Bootstrap, but it could probably use some aesthetic tweaking.

# Tokenize/Count
To be transfered from local test. Everything is laid out in the Bootstrap grid, but conversion to the new DataTables is in progress. The new version will load the entire dataset to the client if it is small (currently set arbitrarily to 10,000 rows); otherwise, it will load only the first ten rows and then request additional data by ajax in response to user actions.

# Word Cloud
Unmodified.

# Multicloud
Unmodified.

# BubbleViz
Unmodified.

# Rolling Windows
Unmodified.

# Statistics
Unmodified.

# Hierarchical Clustering
Unmodified. Some work has been done to add Newick conversion and display graphs using matplotlib, but it needs to be transfered from my local version.

# K-Means Clustering
Unmodified.

# Similarity Query
Unmodified.

# Topword
Unmodified.

## Last Update
Dec 29, 2015