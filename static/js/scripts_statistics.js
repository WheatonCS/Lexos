/* #### INITIATE SCRIPTS ON $(DOCUMENT).READY() #### */
$(document).ready( function () {

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