<p><b>Manage</b> is the tool you use to perform various types of "housekeeping" on documents in your Lexos workspace. In addition to documents derived from files you have uploaded, <b>Manage</b> will also list documents created by other tools such as segments produced by the Cutter tool.</p>
<p>Use the <b>Manage</b> tool for the following purposes</p>
<ul>
<li>To activate and de-activate documents in your workspace. By default, most Lexos tools will only operate on your active documents.</li>
<li>To delete unwanted documents from your workspace.</li>
<li>To re-name or classify documents in your workspace.</li>
</ul>

<h4>The Manage Interface</h4>
<p>Documents in your workspace are listed in the form of a table. When the uploaded file from which each document is derived will be listed by filename in the <b>Original Source</b> column. The <b>Document Name</b> column lists the filename without the extension. If you use Lexos tools to create new documents based on your uploaded files, the original filename will be displayed in the <b>Original Source</b> column, and a new name will be generated for the <b>Document Name</b> column. Document names can be changed as described in <b>Using the Context Menu</b> below.</p>

<p>Be default, documents created by file upload or a Lexos tool do not have an associated class, so the <b>Class Label</b> column is empty. The <b>Excerpt</b> column shows the beginning and end of each document separated by an ellipsis (...). Columns can be sorted alphabetically clicking on the column header. The table highlights columns in blue to show which column is being used to sort the listed documents. If you have a large table, you can filter it down to a few rows containing keywords entered in the <b>Search</b> field. The text of the entire table is searched, so matches may be found in any column. You may use the <b>Display</b> dropdown menu to increase the number of rows displayed, or you can use the pagination links at the bottom right of the table to paginate through smaller sets of rows.</p>

<h4>Activating, De-Activating, and Deleting Documents</h4>
<p>By default, all documents are activated when they are uploaded. Rows containing active documents are highlighted in green. The following methods can be used to manage the active state of documents:</p>

<ul>
<li><b>Single Click</b>: This will de-activate all documents and toggle the state of the row clicked. If it is active, it will be de-activated. If it is not active, it will be activated.</li>
<li><b>Control or Command Click</b>: This will toggle the state of the row clicked without affecting the state of any other rows.</li>
<li><b>Shift Click</b>: This activate ranges of rows. Shift-clicking on a row will activate documents in all rows between the row clicked and the first active row above or below the row clicked.</li>
<li><b>Drag Click</b>: Clicking on a row with the mouse button held down will activate or de-activate all rows between the row clicked and the row the mouse cursor is over when the mouse button is released.</li>
<li><b>Right Click</b>: This will open the context menu. See <b>Using the Context Menu</b> below.
<li><b>The Select All and Deselect All Buttons</b>: These are useful because they activate and de-activate all the documents in your workspace, not just those displayed on the page.</li>
</ul>  

<p>Documents may also be activated and de-activated using the <b>Context Menu</b> as described below.</p>

<p>Certain tools such as <b>Word Cloud</b> allow you to select and de-select sub-sets of your active documents. These selections apply only within the given tool and do not affect whether the documents are active or not throughout the Lexos suite. If you need to change the state of a document so that it is or is not accessible to all tools, you should do this using <b>Manage</b>.</p>

<h4>Deleting Documents</h4>
<p>Deleting individual documents from the workspace is probably achieved most easily achieved using the <b>Context Menu</b> as described below. However, you can deselect all documents, activate only the document you wish to delete, and then click the <b>Delete Selected</b> button. This button is probably more useful when you have multiple active documents, as it will delete them all at once. Make sure that you have de-activated any documents you do not wish to delete.</p> 

<h4>Using the Context Menu</h4>
<p>Right-clicking on a table cell or row will open the context menu. It has the following options:</p>
<ul>
<li><b>Preview Document</b>: This will open a dialog containing the entire text of your document (without formatting or white spaces). Note that longer documents can take a while to load, so please be patient.</li>
<li><b>Edit Document Name</b>: This function allows you to create a new name for the document in the row you have clicked. To change the name, enter your new name in the dialog form field and click <b>Save</b>.</li>
<li><b>Edit Document Class</b>: This function allows you to create a class label for the document in the row you have clicked. Enter the label you wish to identify with the class in the dialog form field and click <b>Save</b>. See further the section on document classes below.</li>
<li><b>Delete Document</b>: This function will delete the individual document in the row you have clicked.</li>
<li><b>Select All Documents and Deselect All Documents</b>: These options have the same function as the <b>Select All</b> and <b>Deselect All</b> buttons.</li>
<li><b>Apply Class to Selected Documents</b>: If you have multiple active documents, this option will allow you to apply a class label to all of them at once. Enter the label you wish to identify with the class in the dialog form field and click <b>Save</b>. See further the section on document classes below.</li>
<li><b>Delete Selected Documents</b>:  If you have multiple active documents, this option will allow you to delete them all at once. It has the same function as the <b>Delete Selected</b> button.</li>
</ul>

<h4>Classifying Documents</h4>
<p>Document classes are groups of documents identified as belonging to the same category defined by some human-assigned criterion. For instance, a collection of novels might be separated into two classes based on whether they were published in Britain or the United States. Gender, genre, and date of authorship might also be used to classify documents. Lexos' class labels allow you to assign classes to documents and sort by class in the <b>Manage</b> tool. At present, document classes are under-utilized elsewhere in the Lexos suite, but they are an important part of the <b>Topwords</b> tool. In general, you should assign class labels in <b>Manage</b> before going to <b>Topwords</b>.</p>