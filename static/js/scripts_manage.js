

/* #### INITIATE SCRIPTS ON $(DOCUMENT).READY() #### */
$(document).ready( function () {

/* #### INITIATE MAIN DATATABLE #### */
/* #### END OF TABLE INITIATION #### */	

/* #### DEFINE CONTEXT MENU #### */
/* #### END OF CONTEXT MENU #### */

/* #### CLICK EVENT HANDLING #### */
/* #### END OF CLICK EVENT HANDLING #### */

/* #### TOOLBAR BUTTON EVENT HANDLING #### */
/*	$("#selectall").click(function() {
		selectAll();
	});

	$("#disableall").click(function() {
		deselectAll();
	});

	$("#delete").click(function() {
		deleteSelectedRows();
	});*/
/* #### END OF TOOLBAR BUTTON EVENT HANDLING #### */	

});
/* #### END OF $(DOCUMENT).READY() SCRIPTS #### */

/* #### SUPPORTING FUNCTIONS #### */
/* #### toggleId() #### LEGACY FUNCTION: NO LONGER IN USE */
// Toggles the document state by Ajax, then toggles the UI selected state for the item.
function toggleId(id) {
	row_id = "#" + id;
	$.ajax({
		type: "POST",
		url: document.URL,
		data: id.toString(),
		contentType: 'charset=UTF-8',
		headers: { 'toggleFile': 'dummy' },
		beforeSend: function(){
     		$("#status").show();
   		},
		//success: function() {
		//},
		complete: function(){
     		$("#status").hide();
   		},
		error: function(jqXHR, textStatus, errorThrown){
			alert('Error: Your action could not be saved to the session file.')
			$("#"+id).removeClass("ui-selected");
			console.log("bad: " + textStatus + ": " + errorThrown);
		}
	});
}
/* #### END OF toggleId() #### */

/* #### editLabel() #### */
// Opens a JQuery UI dialog to edit a document label. On submit, the File Manager is updated by Ajax.
function editLabel($target, cellText, title, row_id) {
	var form = 'Document Label <input id="tmp" type="text" value="'+cellText+'">';
	var opts = {
		height:200,
		width:400,
		buttons: {
		"Save": function() {
			val = $("#tmp").val();
			// Send by ajax, update table, and close on success
			$.ajax({
				type: "POST",
				url: document.URL,
				data: row_id.toString(),
				contentType: 'charset=UTF-8',
				headers: { 'setLabel': unescape(encodeURIComponent(val.toString())) },
				success: function(response) {
					$target.text(val);
					$("#editLabel").dialog("close");
					$("#editLabel").remove();
					tr = $target.parent();
				},
				error: function(jqXHR, textStatus, errorThrown){
					alert('Error: Your action could not be saved to the session file.')
					// display error if one
					console.log("bad: " + textStatus + ": " + errorThrown);
				}
			});
		},
		"Cancel": function() {
			$(this).dialog("close");		
		}}
	};
	$('<div id="editLabel" title="Document Label for ' + title + '">' + form + '</div>').dialog(opts);
}
/* #### END OF editLabel() #### */

/* #### editClass() #### */
// Opens a JQuery UI dialog to edit a document class. On submit, the File Manager is updated by Ajax.
function editClass($target, cellText, title, row_id) {
	var form = 'Class Prefix <input id="tmp" type="text" value="'+cellText+'">';
	var opts = {
		height:200,
		width:400,
		buttons: {
		"Save": function() {
			val = $("#tmp").val();
			// Send by ajax, update table, and close on success
			$.ajax({
				type: "POST",
				url: document.URL,
				data: row_id.toString(),
				contentType: 'charset=UTF-8',
				headers: { 'setClass': unescape(encodeURIComponent(val.toString())) },
				success: function(response) {
					console.log("Success: "+response);
					$target.text(val);
					tr = $target.parent();
					$("#editClass").dialog("close");
					$("#editClass").remove();
				},
				error: function(jqXHR, textStatus, errorThrown){
					alert('Error: Your action could not be saved to the session file.')
					// display error if one
					console.log("bad: " + textStatus + ": " + errorThrown);
				}
			});
		},
		"Cancel": function() {
			$(this).dialog("close");		
		}}
	};
	$('<div id="editClass" title="Add Class Prefix to ' + title + '">' + form + '</div>').dialog(opts);
}
/* #### END OF editClass() #### */

/* #### applyClass() #### */
// Opens a JQuery UI dialog to edit a document class. On submit, all selected documents are updated in the File Manager by Ajax.
function applyClass($target, cellText) {
	var form = 'Class Prefix <input id="tmp" type="text" value="'+cellText+'">';
	var opts = {
		height:200,
		width:400,
		buttons: {
		"Save": function() {
			val = $("#tmp").val();
			// Send by ajax, update table, and close on success
			$.ajax({
				type: "POST",
				url: document.URL,
				data: val.toString(),
				contentType: 'charset=UTF-8',
				headers: { 'applyClassLabel': 'dummy' },
				success: function(response) {
					$('.class-label').each(function() {
						if ($(this).parent().hasClass("selected")) {
							$(this).html(val);
						}
					});
					tr = $target.parent();
					$("#editClass").dialog("close");
					$("#editClass").remove();
				},
				error: function(jqXHR, textStatus, errorThrown){
					alert('Error: Your action could not be saved to the session file.')
				$("#"+id).removeClass("ui-selected");
					console.log("bad: " + textStatus + ": " + errorThrown);
				}
			});
		},
		"Cancel": function() {
			$(this).dialog("close");		
		}}
	};
	$('<div id="editClass" title="Apply Class Prefix to All Selected Files">' + form + '</div>').dialog(opts);
}
/* #### END OF applyClass() #### */

/* #### showPreviewText() #### */
//* Opens a JQuery UI dialog containing the document preview text. Eventually, this should be replaced with the complete text in an editor.
function showPreviewText(row_id) {
	$.ajax({
		type: "POST",
		url: document.URL,
		data: row_id,
		contentType: 'charset=UTF-8',
		headers: { 'previewTest': 'dummy' },
		success: function(response) {
			response = JSON.parse(response);
			console.log(response);
			title = response["label"];
			text = response["previewText"];
			// Encode tags as HTML entities
			text = String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
			//* To Do: Convert tagged texts to strings
			$('<div id="preview" title="Preview of ' + title + '">' + text + '</div>').dialog({height:500,width:500});
		},
		error: function(jqXHR, textStatus, errorThrown){
			alert('Error: Lexos could not retrieve the file preview.');
			// display error if one
			console.log("bad: " + textStatus + ": " + errorThrown);
		}
	});
}
/* #### END OF showPreviewText() #### */

/* #### deleteRow() #### */
// Deletes a single document in the File Manager and UI.
function deleteRow(target, title, row_id) {
	// Center the caution prompt in the window.
	$('#delete-confirm-wrapper').center();
	$('#delete-explanation').html("Are you sure you want to delete "+title+"?");
	$('#delete-confirm-wrapper').addClass("showing");
	// If the user clicks the cancel button, close the dialog.
	$('#cancel-bttn').click(function() {
		$('#delete-confirm-wrapper').removeClass("showing");
	});

	// If the user clicks confirm, delete the selection.
	$('#confirm-delete-bttn').click(function() {
		$.ajax({
			type: "POST",
			url: document.URL,
			data: row_id,
			headers: { 'deleteRow': 'dummy' },
			success: function() {
				$('#delete-confirm-wrapper').removeClass("showing");
				target.parent().remove();
			},
			error: function(jqXHR, textStatus, errorThrown){
				alert('Error: Lexos could save your changes to the session file.')
				console.log(errorThrown);
			}
		});
	});
}

/* #### END OF deleteRow() #### */

/* #### deleteSelectedRows() #### */
// Deletes selected documents in the File Manager and UI.
function deleteSelectedRows() {
	// Center the caution prompt in the window.
	$('#delete-confirm-wrapper').center();
	$('#delete-confirm-wrapper').addClass("showing");
	// If the user clicks the cancel button, close the dialog.
	$('#cancel-bttn').click(function() {
		$('#delete-confirm-wrapper').removeClass("showing");
	});

	// If the user clicks confirm, delete the selected documents.
	$('#confirm-delete-bttn').click(function() {
		$.ajax({
			type: "POST",
			url: document.URL,
			data: "",
			headers: { 'deleteActive': 'dummy' },
			success: function() {
				$('#delete-confirm-wrapper').removeClass("showing");
				$("#demo tbody tr").each(function() {
					if ($(this).hasClass("selected")) {
						$(this).remove();
					}
				});
				console.log(enabled);
			},
			error: function(jqXHR, textStatus, errorThrown){
				alert('Error: Lexos could save your changes to the session file.')
				console.log(errorThrown);
			}
		});
	});

}

/* #### END OF deleteSelectedRows() #### */

/* Functions called in lexos.py */
//Javascript         -->    Ajax Call*
//------------------------------------------
//toggleFile         -->    toggleFile
//editLabel          -->    setLabel
//editClass          -->    setClass
//applyClass         -->    applyClassLabel
//showPreviewText    -->    previewTest
//selectAll          -->    selectAll
//deselectAll        -->    disableAll
//deleteRow          -->    deleteRow
//deleteSelectedRows -->    deleteActive

// * Calls are made through select2() in the 
// Development Section of lexos.py.
// ** Missing function.

// By default, select2() calls getPreviewsOfAll()*.
// Otherwise, the following functions are called:
// lexos.py        -->    ModelClasses.py
// -------------------------------------------
// previewTest     -->    getPreview
// toggleFile      -->    toggleFile
// setLabel        -->    Handled in lexos.py
// setLabel        -->    Handled in lexos.py and setName 
// setClass        -->    Handled in lexos.py and
//                          setClassLabel
// selectAll       -->    enableAll
// applyClassLabel -->    classifyActiveFiles
// deleteActive    -->    deleteActiveFiles
// deleteRow       -->    deleteOneFile*

// *In the development section.
// ** Development section has classifyFile, which is not used.