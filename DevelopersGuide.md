# Lexos-Bootstrap Developer's Guide

## Table of Contents
* [Introduction](#introduction)
* [General Principles](#general-principles)
* [DataTables](#datatables)
* [Ajax Requests](#ajax-requests)
* [Javascript](#javascript)
* [Styling](#styling)
* [Flyout Menus](#flyout-menus)
* [Tooltips and Popovers](#tooltips-and-popovers)
* [Bootstrap Modals and Error Messages](#bootstrap-modals-and-error-messages)
* [_In the Margins_](#in-the-margins)
* [Notes on Individual Screens](#notes-on-individual-screens)

## Introduction
Lexos-Bootstrap is a fork of the Lexos 2.5 with much of the front-end functionality handled by the Bootstrap javascript framework. The original motivation was simply to borrow the Bootstrap navbar component to handle flyout menus for the Lexos cluster analysis tools. But it quickly became clear that other features of Bootstrap, particularly its grid layout system, would be useful for development. So I attempted to convert the entire Lexos application to Bootstrap.

Lexos-Bootstrap is far from complete, but it is largely functional. The main layout has been converted to the Bootstrap grid, but many internal elements still need to be converted to Bootstrap for cleaner code (requiring fewer css classes). Some css and javascript has been left as is if did not conflict with any of the new code. With the exception of the new Manage page, I made almost no changes to the back end Python.

The following notes should be helpful in completing the conversion and further development using Lexos-Bootstrap.

## General Principles
Lexos-Bootstrap actually combines three innovations to Lexos. In addition to the Bootstrap css and javascript, Lexos-Bootstrap employs an updated version of the DataTables javascript in tools with tables (e.g. Manage, Tokenize, etc.). In addition to an improved API, this version of DataTables is Bootstrap-compliant, making it visually seamless with the rest of the styling. The Manage screen provides the best example of its functionality. The Manage screen also makes extensive use of Ajax requests to send data for processing by the server. This allows the screen to be updated without a page refresh. This is visually more appealing, but it also speeds loading times. Since Bootstrap does have a heavy footprint, it is actually important to use Ajax so that it does not have to be loaded multiple times. One of our first tasks will be to replace the current form submit code to Ajax requests.

## DataTables
DataTables is loaded from CDN, and it now integrates all its plugins with a single http request. DataTables is loaded in the template files where it is needed with the following code:

```javascript
<!-- Latest compiled and minified DataTables CSS -->
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/t/bs/jszip-2.5.0,pdfmake-0.1.18,dt-1.10.11,b-1.1.2,b-html5-1.1.2,b-print-1.1.2,fh-3.1.1,sc-1.4.1,se-1.1.2/datatables.min.css"/>

<!-- Latest compiled and minified DataTables JS --> 
<script type="text/javascript" src="https://cdn.datatables.net/t/bs/jszip-2.5.0,pdfmake-0.1.18,dt-1.10.11,b-1.1.2,b-html5-1.1.2,b-print-1.1.2,fh-3.1.1,sc-1.4.1,se-1.1.2/datatables.min.js"></script>

<script type="text/javascript" charset="utf8" src="{{ url_for('static', filename='DataTables-1.10.7/natural.js') }}?ver={{version}}"></script>
```

The template files should then have a normal html table like this:

```html
<table id="example" class="table table-striped table-bordered">
    <thead>
        <tr>
            <th>Column1</th>
            <th>Column2</th>            
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Cell 1</td>
            <td>Cell 2</td>
        </tr>
        <tr>
            <td>Cell 3</td>
            <td>Cell 4</td>
        </tr>
    </tbody>
</table>
```

To initialise the table, place the following code in the `scripts_` Javascript file:

```javscript
// Basic table initialisation
$(document).ready(function() {
    $('#example').DataTable();
});

// Initialisation with options
$(document).ready(function() {
    $('#example').DataTable({
        paging: true,
        searching: true
    });
});
```

### Notes:
* This code calls DataTables and all its plugins from CDN with a single http request. For the release version, we need to download the entire thing and make it available in a local folder in case the user needs it. From time to time, we may need to regenerate the urls to take into account updates to DataTables. The version number for the main script and each plugin is given in the url string. A new url can be generated from the DataTables [download builder](https://www.datatables.net/download/index).
* The separate call to `DataTables-1.10.7/natural.js` should be unnecessary in DataTables-1.10.11, but I have not figured out how to implement it. So this should be investigated and the extra script call phased out.

DataTables essentially transforms a normal html table (which must have a `thead` element) in the template file. The table is styled according to normal [Bootstrap guidelines](http://getbootstrap.com/css/#tables). A good example can be found in `manage.html`. Search for `id="demo` (probably that id should be changed to something more informative).

The DataTable is then initialised in the `scripts_` file, e.g. `scripts_manage.js`. In this file, the first 100 or so lines are dedicated to initialising the table with various options and handling events. Further down, there are examples of how to use Ajax requests to update the table based on values returned from the server (for instance, filtering).

DataTables has a very extensive and well-document API with lots of options. The best way to understand them is to read the options initialised in `manage.html` and then read the [manual](https://www.datatables.net/manual/index) and [examples](https://www.datatables.net/examples/index). The [forums](https://www.datatables.net/forums/) are incredibly helpful, but be careful. Many questions refer to older versions of DataTables.

There are three current issues:
1. `DataTables-1.10.7/natural.js` should be phased out as described above.
2. In Tokenize, DataTables works well with all functions working by Ajax. The one exception is the function to rotate the table. According to the developer, "the idea of columns being vertical rather than horizontal in quite deeply baked into the current DataTables code". It may be necessary to fall back on a page reload to handle this function.
3. In Statistics, something in `scripts_statistics.js` appears to conflict with the layout. So, for the moment, Statistics still uses the older version of DataTables.

## Ajax Requests
Here is a quick guide to making Ajax requests. Assume that you want to create a function that does something on the server and returns something to be handled in the page JavaScript. Create a function in the screen template or (better) `scripts_XX.js` file like this:

```javascript
function myFunction(args) {
    // If args is a list of values, convert it to a json string
    data = JSON.stringify(args);

    // Submit the Ajax request
    $.Ajax({
        type: "POST",
        url: "/myFunction",
        data: data,
        contentType: 'application/json;charset=UTF-8',
        cache: false,
        success: function(response) {
            // Do something ...
            console.log(response);
        },
        error: function(jqXHR, textStatus, errorThrown){
            $("#error-modal .modal-body").html("Lexos could not perform the requested function.");
            $("#error-modal").modal();
            console.log("bad: " + textStatus + ": " + errorThrown);
        }
    });
}
```
You can change the error message to say something more specific about the function.

In `lexos.py` add a route with the same name as the Javascript function (or whatever you pass in Ajax `url` value). The following example assumes you passed a list of file IDs as the `data` value, calls a function to modify each one, saves the results, and then returns a "success" message by Ajax.

```python
@app.route("/myFunction", methods=["GET", "POST"])
def myFunctionFunction():
    fileManager = managers.utility.loadFileManager()
    for fileID in request.json:
        fileManager.doSomethingToAFile(fileID)
    managers.utility.saveFileManager(fileManager)
    return 'success'
```

Screens already converted to Ajax in Lexos-Bootstrap:
+ Upload
+ Manage
+ Scrub
+ Cut

## Javascript
Wherever possible, I have used native Bootstrap functions or third-part plugins made to be compatible with Bootstrap. All jQuery UI functions have been replaced, and jQuery UI is no longer loaded in `base.html`. However, the jQuery UI `selectable()` method is still employed in Multicloud to handle tile dragging, so the jQuery UI javascript and accompanying css is loaded in the Multicloud template.

Some legacy javascript has been left in template and script files. Each file should be examined to see what can be removed.

## Styling
Bootstrap provides pre-defined colour classes, as well as the `btn` class to convert links into buttons. These pre-defined classes are similar to, but not precisely the same as the Lexos colour scheme. I have used them for convenience but overridden them with Lexos styling rather unsystematically. This will obviously have to be made more systematic. I have sometimes left legacy class designations in the code where it did not interfere with functionality. We will need to go through the code and remove them.

In `style.css` I have often left legacy styles as a reference. We will need to clean this up. Some plugins also have their own stylesheets, and it may be worth it to consolidate them with `style.css` so that there are fewer http requests on page load.

## Flyout Menus
The navbar flyout menus for clustering are submenus of a Bootstrap dropdown. This functionality is disabled in Bootstrap 3, so a plugin called SmartMenus has been used to re-enable it. There is no special markup needed for SmartMenus. Just follow the Bootstrap code for submenus in dropdowns, and add an extra submenu. The rest is automatic. That said, flyout menus should be used sparingly if at all.

## Tooltips and Popovers
In a few cases, Lexos appeared to be missing tooltips, so empty ones have been added with text calling attention to themselves.

Bootstrap has two very similar components to replace the native browser tooltip. Tooltips popup when the mouse hovers over the trigger element. Popover behaviours are more programmable, but Lexos-Bootstrap uses them in essentially the same way. The main difference is that popovers stay open until the cursor enters and then leaves the popover body. This makes them a better choice when the text contains links. However, multiple popovers in close proximity may replicate without disappearing if the user does not follow the mouseover-mouseout pattern.

Tooltips and popovers are initialised in `scripts_base.js`, so the easiest way to use them is to paste them in from one of the templates below.

#### Popover
```html
<i class="fa fa-question-circle lexos-tooltip-trigger" data-toggle="tooltip" data-html="true" data-placement="right" data-container="body" title="Some content" style=""></i>
```

#### Tooltip
```html
<i class="fa fa-question-circle lexos-popover-trigger" data-trigger="hover" data-html="true" data-toggle="popover" data-placement="right" data-container="body" data-content="Some content" style="" title=""></i>
```

`@style` may be used to adjust the size and placement of the trigger icon. The default is `margin-right:10px;font-size:14px;`. Tooltip text goes in `@title`; popover text goes in `@data-content`. In popovers, `@title` may be used to give the popover a header.

One problem with Bootstrap tooltips and popovers is that they can only be made to appear above, below, to the left, or to the right of the trigger element, rather than diagonally above, and so on. Another problem is that the tooltip cannot be made to track the mouse position. Both these functions were available in in Lexos 2.5, which uses the qTip2 library. This has been mostly replaced in Bootstrap-Lexos, but qTip2 is still initialised in `base.html` and is available in screens that use it, such as the word cloud functions.

### Tooltips in Graphs
Many of the word cloud-like visualisations allow you to view word counts when you mouse over words. Getting Bootstrap tooltips to appear over SVG elements is not straightforward, and I have not yet got it working. So in places, qTip2 is still used. If possible, it should be replaced since qTip2 has a bug which causes the tooltips to float around the screen after the mouse has left the trigger element (and to reduce code bloat). If possible, Bootstrap tooltips should be used. Another option is `d3.tip.js`.

## Bootstrap Modals and Error Messages
The JQuery UI dialogs used in Lexos 2.5 have been replaced with Bootstrap modals in Lexos-Bootstrap. Many examples can be seen in the right-click context menu in Manage. If possible, error message should be implemented in Bootstrap modals. An example can be seen by selecting the "Rock Paper Scissors Lizard Spock" option.

The "cog" icon at the top right demonstrates an _In the Margins_ page displayed in a Bootstrap modal.

## _In the Margins_
_In the Margins_ content is loaded by calling the Scalar API in `scripts_ITM.js`. The functions therein fetch the content from Scalar and format it for insertion in Lexos. Eventually, we will want to write functions to insert content in div elements or tooltips. Currently, ITM content can be loaded in the side panel on the left or in a Bootstrap modal. The latter is currently demonstrated by the cog icon next to the Reset button and the **Watch the Video** button in Rolling Windows.

### The Side Panel
The side panel (which is automatically closed on page load) gets its content from the following line in `base.html`:

```html
<div id="ITMPanel-itm-content" data-slug="{{ itm }}" data-type="panel" data-status="closed" style="max-height:99%;overflow-y:auto;">
```

`@data-slug` is the name of the Scalar slug to be fetched. It must be passed to the template from `lexos.py` using a variable like `@itm="best-practices"` (the current default). `@data-type="panel"` specifies the side panel as the target of the content.

### Modals
A Bootstrap modal may be targeted for ITM content by using the generic `ITM-modal` div. The cog icon demonstrates how to create button that triggers the modal:

```html
<a class="btn" id="bttn-cog" data-toggle="modal" data-target="#ITM-modal" data-slug="best-practices" data-type="dialog" href="#">
```

**Important:** If the ITM content is a YouTube video, use `data-type="dialog"`. Videos are not fetched directly from YouTube. The video must have a Scalar page, and `@data-slug` must contain the Scalar slug.

### Collapsible Panels
Collapsible panels for advanced options such as those in Scrub use Bootstrap's Collapse plugin. They have the following code template (here demonstrated using the stopwords option):

```html
<legend id="stopwords" class="has-chevron">Legend Text 
    <span class="fa fa-chevron-right rotate {{ 'showing' if sw_showing }}" data-target="#stopwordPanel" aria-expanded="false" aria-controls="stopwordPanel"></span>
</legend>
<div class="collapse" id="stopwordPanel">
    <div>Panel Content</div>
</div>
```

In the `base_analyze.html` template, Culling Options and Assign Temporary Labels use these collapsible panels. Some screens which leverage this template need to move Assign Temporary Lables to the top row and hide Culling Options. Code for doing this may be found at the top of `scripts_statistics.js` under the comment "Hide unnecessary divs for DTM".

## Notes on Individual Screens

### Upload
Bootstrap has native progress bars, but I was unable to use them to duplicate the current functionality. So the non-Bootstrap Lexos progress bar has been retained.    

### Manage
Manage should be fairly complete. A previously unobserved behaviour is to select/de-select a single cell, rather than a row, on control/command-click. Selecting the cell requires a second click. The same behaviour seems to be present on the DataTables site: [https://datatables.net/extensions/select/examples/initialisation/simple.html](https://datatables.net/extensions/select/examples/initialisation/simple.html). It may be a bug in the latest version of DataTables. Again, testing is required.

### Scrub and Cut
These tools should be fully converted to Bootstrap layout and fully functional by Ajax. There is a bug in the script that button bar above or below the document preview div, depending on the scroll position: a second copy of the button bar gets replicated inside the div. The placement of these buttons is provisional in any even&mdash;where to put them on the page is something of a design issue&mdash;but the bug should be fixed if the buttons are to be kept in this location. 

### Tokenize
This tool has been laid out in Bootstrap, but its functionality has not been implemented through Ajax. I have the code to do so in another repo, and I will implement it after Lexos-Bootstrap is adopted as the master repo.

### Word Cloud, Multicloud, and BubbleViz
Conversion to Bootstrap was fairly straightforward for these tools, and they may only need minor aesthetic improvements to the layout. The major challenge will be implementation of tooltips on SVG elements. However, submission of options in Multicloud and BubbleViz should also be switched to Ajax requests.

Important changes are as follows:
+ The Multicloud toggle has been implemented using a plugin called [Bootstrap Switch](http://www.bootstrap-switch.org/). It is arguably less attractive than the old one, but it is easy to integrate with Bootstrap and to re-deploy elsewhere, if needed.
+ BubbleViz had plenty of screen real estate, so the old check box to reveal options to filter the data did not seem necessary. I removed it and made all options visible.

### Rolling Windows
This tool has been entirely converted to Bootstrap. In the process, the options have been re-organised into (what I think) is a more logical flow. I have done some re-labelling in the process. Submission of options needs to be switched to Ajax requests.

### Statistics
This tool has been converted to Bootstrap, except for the use of DataTables. Something in `scripts_statistics.js` conflicts with the latest version of DataTables and messes up the layout. This will have to be investigated. It should be something fairly minor.

### Hierarchical Clustering
Converted to Bootstrap. The PDF dendrogram in the iframe should be replaced with an image, but this involves complications not related to the Bootstrap conversion. I have code to do it, which I'll integrate after Lexos-Bootstrap is adopted as the new master branch.

### K-Means Clustering
Converted to Bootstrap, but the chevrons on collapsible panels don't rotate. I'm not sure why.

### Similarity Query
This tool has been converted to Bootstrap, except for the generated table. Currently, the tool uses TidyTable. This needs to be switched to DataTables to take advantage of Bootstrap styling. Also, the Get and Download buttons needs to switch to Ajax requests rather than form submission.

### Topword
The various tables generated by this tool have been placed in a light Bootstrap grid layout. However, the main change is the (incomplete) addition of tooltips. Most still need explanatory text.
