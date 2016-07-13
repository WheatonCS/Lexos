# Lexos-Bootstrap Developer's Guide
Updated: July 1 2016

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
* [Tips for Back-End Programming] (#back-end-tips)

## Introduction
Lexos 3.0 builds on Lexos-Bootstrap, itself a fork of Lexos 2.5 with much of the front-end functionality handled by the Bootstrap javascript framework. The original motivation for Lexos-Bootstrap was simply to borrow the Bootstrap navbar component to handle flyout menus for the Lexos cluster analysis tools. But it quickly became clear that other features of Bootstrap, particularly its grid layout system, would be useful for development, so Lexos-Bootstrap became the model for Lexos 3.0.

The conversion to the Bootstrap framework is far from complete, but it is largely functional. The main layout has been converted to the Bootstrap grid, but many internal elements still need to be converted to Bootstrap for cleaner code (requiring fewer css classes). Some css and javascript has been left as is if did not conflict with any of the new code.

The following notes should be helpful in completing the conversion and further development using Bootstrap.

## General Principles
Lexos 3.0 actually combines three innovations to Lexos. In addition to the Bootstrap css and javascript, Lexos 3.0 employs an updated version of the DataTables javascript in tools with tables (e.g. Manage, Tokenize, etc.). In addition to an improved API, this version of DataTables is Bootstrap-compliant, making it visually seamless with the rest of the styling. The Manage screen provides the best example of its functionality. The Manage screen also makes extensive use of Ajax requests to send data for processing by the server. This allows the screen to be updated without a page refresh. This is visually more appealing, but it also speeds loading times. Since Bootstrap does have a heavy footprint, it is actually important to use Ajax so that it does not have to be loaded multiple times. Converting earlier form submit behaviours in Lexos will take time, so the plan is to do so gradually.

## DataTables
DataTables is loaded from CDN, and it now integrates all its plugins with a single http request. DataTables is loaded in the template files where it is needed with the following code:

```javascript
<!-- Latest compiled and minified DataTables CSS -->
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/u/bs/jszip-2.5.0,pdfmake-0.1.18,dt-1.10.12,b-1.2.1,b-html5-1.2.1,b-print-1.2.1,fc-3.2.2,fh-3.1.2,se-1.2.0/datatables.min.css"/>

<!-- Latest compiled and minified DataTables JS --> 
<script type="text/javascript" src="https://cdn.datatables.net/u/bs/jszip-2.5.0,pdfmake-0.1.18,dt-1.10.12,b-1.2.1,b-html5-1.2.1,b-print-1.2.1,fc-3.2.2,fh-3.1.2,se-1.2.0/datatables.min.js"></script>

<script type="text/javascript" charset="utf8" src="{{ url_for('static', filename='DataTables-1.10.7/natural.js') }}?ver={{version}}"></script>
```

The template files should then have a normal html table like this:

```html
<table id="example" class="table table-striped table-condensed table-hover table-bordered">
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
* In some cases, there is also a call to `https://nightly.datatables.net/fixedcolumns/js/dataTables.fixedColumns.min.js`, which fixes an overlap issue where fixed columns are used. It may not be necessary for the latest version of DataTables.

DataTables essentially transforms a normal html table (which must have a `thead` element) in the template file. The table is styled according to normal [Bootstrap guidelines](http://getbootstrap.com/css/#tables). A good example can be found in `manage.html`. Search for `id="demo` (probably that id should be changed to something more informative).

The DataTable is then initialised in the `scripts_` file, e.g. `scripts_manage.js`. In this file, the first 100 or so lines are dedicated to initialising the table with various options and handling events. Further down, there are examples of how to use Ajax requests to update the table based on values returned from the server (for instance, filtering).

DataTables has a very extensive and well-document API with lots of options. The best way to understand them is to read the options initialised in `manage.html` and then read the [manual](https://www.datatables.net/manual/index) and [examples](https://www.datatables.net/examples/index). The [forums](https://www.datatables.net/forums/) are incredibly helpful, but be careful. Many questions refer to older versions of DataTables.

There are three current issues:
1. `DataTables-1.10.7/natural.js` should be phased out as described above.
2. In Tokenize, DataTables works well with all functions working by Ajax. The one exception is the function to rotate the table. According to the developer, "the idea of columns being vertical rather than horizontal in quite deeply baked into the current DataTables code". It may be necessary to fall back on a page reload to handle this function. So far, we are experimenting with destroying and rebuilding the table with an Ajax request.

## Ajax Requests
Here is a quick guide to making Ajax requests. Assume that you want to create a function that does something on the server and returns something to be handled in the page JavaScript. Create a function in the screen template or (better) `scripts_XX.js` file like this:

```javascript
function myFunction(args) {
    // If args is a list of values, convert it to a json string
    data = JSON.stringify(args);

    // Submit the Ajax request
    $.ajax({
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

Note: Download buttons are a special case. Often they need to send the form values through the POST array so that they can be used in a back-end function call. In this case, it may be easiest to trigger the download with a submit button like this:

```html
<input type="submit" class="bttn bttn-exit bttndownload" id="csvdownload" name="get-csv" value="Download CSV"/>
```

On the back end, this will not trigger a page reload as long as the back-end function does not return a `render_template()` function. In some cases, the current page route may have other behaviours triggered by the POST method, whether from an Ajax request or from a normal HTTP request. In this case, the download behaviour can be safely set apart using an `if/else` statement like the following:

```python
if request.method == "POST":
    if 'get-csv' in request.form:
        # The user clicks the download button.
        session_manager.cacheAnalysisOption()
        session_manager.cacheCSVOptions()
        savePath, fileExtension = utility.generateCSV(fileManager)
        managers.utility.saveFileManager(fileManager)

        return send_file(savePath, attachment_filename="frequency_matrix" + fileExtension, as_attachment=True)

    else:
        # Some data is returned by Ajax or a template is rendered.
```

## Javascript
Wherever possible, I have used native Bootstrap functions or third-part plugins made to be compatible with Bootstrap. All jQuery UI functions have been replaced, and jQuery UI is no longer loaded by default in `base.html`. However, it is still used for functions in Word Cloud and Multicloud, and it is therefore loaded only in these pages. This is achieved in `base.html` using a Jinja `if` statement as follows:

```html
<!-- Load jQuery UI only for selected pages -->
{% if active_page == 'wordcloud' or active_page == 'multicloud' %}
<link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
{% endif %}
```

If necessary, more active pages can be tested to determine if jQueryUI should be loaded. It has been discovered recently that jQuery UI hijacks Bootstrap tooltips, so this call must be placed before the Bootstrap function call in `base.html`.

Some legacy javascript has been left in template and script files. Each file should be examined to see what can be removed.

## Styling
Bootstrap provides pre-defined colour classes, as well as the `btn` class to convert links into buttons. These pre-defined classes are similar to, but not precisely the same as the Lexos colour scheme. We have used them for convenience but overridden them with Lexos styling rather unsystematically. This will obviously have to be made more systematic. I have sometimes left legacy class designations in the code where it did not interfere with functionality. We will need to go through the code and remove them.

In `style.css` we have often left legacy styles as a reference. We will need to clean this up. Some plugins also have their own stylesheets, and it may be worth it to consolidate them with `style.css` so that there are fewer http requests on page load.

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

One problem with Bootstrap tooltips and popovers is that they can only be made to appear above, below, to the left, or to the right of the trigger element, rather than diagonally above, and so on. Another problem is that the tooltip cannot be made to track the mouse position. Both these functions were available in in Lexos 2.5, which uses the qTip2 library. This has been mostly replaced in Bootstrap-Lexos, but qTip2 is still used in BubbleViz, so it is loaded in `viz.html`.

### Tooltips in Graphs
Substantial progress has been made in creating attractive tooltips that function properly, despite the fact attaching them to SVG elements is not straightforward. In BubbleViz, qTip2 is still used. There is a slight bug in the implementation which causes the tooltips to float around the screen after the mouse has left the trigger element, but the current implementation does a fairly good job of reducing the appearance of this bug to a minimum..

## Bootstrap Modals and Error Messages
The JQuery UI dialogs used in Lexos 2.5 have been mostly replaced with Bootstrap modals in Lexos-Bootstrap. Many examples can be seen in the right-click context menu in Manage. If possible, all error message should be implemented in Bootstrap modals. An example can be seen by selecting the "Rock Paper Scissors Lizard Spock" option in Manage.

The "cog" icon at the top right demonstrates a the use of a modal icon for another purpose such as enabling further settings or displaying _In the Margins_ content.

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

**Important:** If the ITM content is a YouTube video, use `data-type="video-dialog"`. Videos are not fetched directly from YouTube. The video must have a Scalar page, and `@data-slug` must contain the Scalar slug.

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
Bootstrap has native progress bars, but the tool currently uses the Lexos 2.5 progress bar.    

### Manage
Manage should be fairly complete. A previously unobserved behaviour is to select/de-select a single cell, rather than a row, on control/command-click. Selecting the cell requires a second click. The same behaviour seems to be present on the DataTables site: [https://datatables.net/extensions/select/examples/initialisation/simple.html](https://datatables.net/extensions/select/examples/initialisation/simple.html). It may be a bug in the latest version of DataTables. Again, testing is required.

### Scrub and Cut
These tools should be fully converted to Bootstrap layout and fully functional by Ajax. The placement of the action buttons is provisional&mdash;where to put them on the page is something of a design issue. 

### Tokenize
This tool has been laid out in Bootstrap, but its functionality has not been fully implemented through Ajax. There are complications because of the way DataTables are initialised.

### Word Cloud, Multicloud, and BubbleViz
Conversion to Bootstrap was fairly straightforward for these tools, and they may only need minor aesthetic improvements to the layout. Eventually, submission of options in Multicloud and BubbleViz should also be switched to Ajax requests.

Important changes are as follows:
+ In Word Cloud, the old word count table has been converted from TidyTable to DataTables.
+ The Multicloud toggle has been implemented using a plugin called [Bootstrap Switch](http://www.bootstrap-switch.org/). It is arguably less attractive than the one used in Lexos 2.5, but it is easy to integrate with Bootstrap and to re-deploy elsewhere, if needed.
+ BubbleViz had plenty of screen real estate, so the old check box to reveal options to filter the data did not seem necessary. It has been removed and all the options have been made visible.

### Rolling Windows
This tool has been entirely converted to Bootstrap. In the process, the options have been re-organised into a more logical flow with new labelling. A new navigational element has been introduced to jump directly to the graph when the form is submitted. Back to top arrows have been added to scroll the screen back up. Eventually, form submission should be switched to Ajax requests.

### Statistics
This tool has been entirely converted to Bootstrap, and the new version of DataTables has been implemented.

### Hierarchical Clustering
This tool has been converted to Bootstrap. The PDF dendrogram in the iframe has been replaced with an image. At the moment, this has required removing the labelling options, but we should eventually reintroduce them. In addition, scaling has been used to improve the appearance of dendrograms in the Lexos layout. Lexos can now export to Newick format so that Lexos cluster analyses can be used with other visualisation tools.

### K-Means Clustering
This tool has been converted to Bootstrap. Extensive changes have been made to the labelling of points in the graphs, and mouseover tooltips have been introduced. There is perhaps a bug in the Voronoi graph which causes points to gravitate to the top left.

### Similarity Query
This tool has been converted to Bootstrap, and the old TidyTable has been converted to DataTables.

### Topword
This tool has been almost entirely re-written. It has been placed in a light Bootstrap grid layout. It may still need more tooltips and explanatory text.


Introduction to the Back End
Lexos is built in Python 2.7 using the Flask web framework. Flask sets up a local server and handles processing tasks, including the rendering of html templates and the sending and receiving of http requests to and from the client. When Lexos is first run, Flask establishes a session cookie to handle information about the user's workspace. This cookie holds values that can be accessed from both the front end and the back end by means of the `session` variable. Lexos uses the `session` cookie for the following purposes:

* To cache user's options and other information.
* To send default information to the front end. Lexos defaults can be found in `constant.py`.

The `session` variable functions like a Python dictionary. Hence `session["option"]` will access the value of the specified option in the session.

The session can be renewed by calling `session_function.init()`.

When a user enters information through front-end form field, this is sent to the back end through the `request` variable. Information in the `request` variable can be accessed in a variety of ways:

* `request.method`: returns methods of the request, typically `POST` or `GET`
* `request.form`: returns a Dict containing the name each form field mapped to its value
* `request.form.getlist`: return a Dict containing the name each form field mapped to multiple values (if there is more than one)
* `request.file`: returns a Dict containing the id of each file in an html file input submission
* `request.json`: returns a json object typically containing the same information as `request.form`. It is generally sent from an Ajax request

In Lexos 2, most Lexos tools required the user to submit the form, which sent the form data to `lexos.py` and then triggered a page refresh with the back-end response. In Lexos 3, some features have been transfered to Ajax functions, which send data to `lexos.py` and return a response to the front end without the need for a page refresh.


### <a name='string-manipulation'></a>String Manipulation
Play with the `join` and `split` functions before you deal with strings. Small changes in the use of these functions can make a significant difference in runtime efficiency.

## <a name='back-end-programming'></a>Tips for Back-End Programming
For example use:
```python
str = ''.join[list]
```
Instead of:
```python
str = ''
for element in list:
    str += element
```

### <a name='csv-files'></a>Comma-Separated Value (CSV) and Tab-Separated Value (TSV) Files
To create a comma-separated-value (csv) file:
```python
rows = [','.join[row] for row in matrix] # Use '\t' for tabs
csv = '\n'.join[rows]
```

Note that DataTables can produce CSV and TSV files entirely on the client side, but this should only be done when the entire table is hel in the DOM (i.e. without server-side processing).

### <a name='manipulating-lists'></a>Manipulating Lists
Consider using the `filter` `map` function, the `*` operator, and in-line `for` loops when dealing with lists.

  For example use:
```python
list = map(lambda element: element[:50], list)
```
  Instead of:
```python
for i in range(len(list)):
  list[i] = list[i][:50]
```

When you initialize the list, use `*` rather than a `for` loop:

This is not used that often

For example use:
```python
empty_list = [0] * Len_list
```
Instead of:
```python
emptyMatrix = []
for _ in LenMatrix:
  emptyMatrix.append(0)
```

### `try`, `except` rather than `if`, `else`

For example use:
```python
try:
  dict[i] += 1
except KeyError:
  dict[i] = 1
```
Instead of:
```python
if i in dict:
  dict[i] += 1
else:
  dict[i] = 1
```

Use:
```python
try:
  os.makedir(path)
except:
  pass
```
Instead of:
```python
if os.path.isdir(path)
  pass
else:
  os.makedir(path)
```

When using `except` to do complicated jobs, as a general rule, you should specify the error type (`KeyError`, `ValueError`, etc.) explicitly.

### <a name='handling-matrices'></a>Use of Numpy arrays or dicts for matrices

Use `np.array` or `dict` instead of Python lists. Our current code cold use some greater adoption of this technique. More information can be found in [this tutorial](http://wiki.scipy.org/Tentative_NumPy_Tutorial).

Use:
```python
for element in npArray.flat():
  print element
```
Instead of:
```python
for row in pythonList:
  for element in row:
      print element
  ```

### <a name='temporary-functions'></a>Use `lambda` to create a temporary functions

Use:
```python
sortedList = sorted(ListofTuples, key=lambda tup: tup[n])
```
Instead of:
```python
def sortby(somelist, n):
  nlist = [(x[n], x) for x in somelist]
  nlist.sort()
  return [val for (key, val) in nlist]
sortedList = sortby(ListofTuples, n)
```

### <a name='performance-optimization'></a>Performance optimization
Read [this](https://wiki.python.org/moin/PythonSpeed/PerformanceTips) for tips on how to optimize performance.