/* #### INITIATE SCRIPTS ON $(DOCUMENT).READY() #### */
$(document).ready( function () {

	$("#normalize-options").css({"visibility":"hidden"});

	// Toggle file selection when 'Toggle All' is clicked
	$("#allCheckBoxSelector").click(function(){
		if (this.checked) {
			$(".minifilepreview:not(:checked)").trigger('click');
		} else {
			$(".minifilepreview:checked").trigger('click');
		}
	});

	var prev = -1; //initialize variable
	$("#statsFileSelect").selectable({
		filter: "label",  //Makes the label tags the elts that are selectable
		selecting: function(e , ui){
			var currnet = $(ui.selecting.tagName, e.target).index(ui.selecting);   //gets index of current taget label
			if (e.shiftKey && prev > -1) {      //if you were holding the shift key and there was a box previously clicked
				//take the slice of labels from index prev to index curr and give them the 'ui-selected' class
				$(ui.selecting.tagName,e.target).slice(Math.min(prev,currnet)+1, Math.max(prev,currnet)+1).addClass('ui-selected');
				prev = -1;  //reset prev index
			}else{
				prev = currnet;  //set prev to current if not shift click
			}
		},
		stop: function() {
			//when you stop selecting, all inputs with the class 'ui-selected' get clicked
			$(".ui-selected input", this).trigger("click");
		}
	});

/* #### INITIATE MAIN DATATABLE #### */
	//* Change the element name and test whether the table variable persists
    table = $('table.display').DataTable({
		"iDisplayLength": 25,
		"aLengthMenu": [[25, 50, 100, -1],
						[25, 50, 100, "All"]],
		"scrollY": "400px", // Table max-height
		"scrollCollapse": true, // Collapse shorter
		// Change DataTable default language
		"language": {
			"lengthMenu": "Display _MENU_ documents",
			"info": "Showing _START_ to _END_ of _TOTAL_ documents"
		},
		// Main column definitions
		//* May need to make the index sortable.
		//* Need to modify natural sorting to be case insensitive.
		"columnDefs": [
			{ sortable: true, targets: "_all" },
			{type: 'natural', targets: "_all"}
		],
		// Default Sorting
		order: [[ 0, 'asc' ]],
				dom: 'lT<"clear">frtip',
        tableTools: {
			"sSwfPath": "/static/DataTables-1.10.7/extensions/TableTools/swf/copy_csv_xls_pdf.swf",
            "sRowSelect": "os",
            "aButtons": [
				"print",
                {
                    "sExtends":    "collection",
                    "sButtonText": "Save",
                    "aButtons":    [ "csv", "xls", {
                    "sExtends": "pdf",
                    "sPdfOrientation": "landscape",
					"sTitle": "Lexos Export",
                    "sPdfMessage": "Brought to you by Lexos."
                } ]
                }
			]
        }
	});
});