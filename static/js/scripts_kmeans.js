$(function() {
	
	
	$('#getkmeans').click( function() {
		return true;
	});

	function createTable() {

		if ($("#kmeansresultscheck").text() == 'True') {
			$("#kmeansresults").removeClass('hidden');
			$("#kmeansresultscheck").text('');
		
			mytable = $('<table></table>').attr({ id: "basicTable" });
			var rows = tablerows;
			var cols = 2;
			var tr = [];
			for (var i = 0; i < rows; i++) {
				var row = $('<tr></tr>').appendTo(mytable);
				for (var j = 0; j < cols; j++) {
					$('<td></td>').text("text1").appendTo(row); 
					}//for
			}//for
			mytable.appendTo("#ktable");

		} //end if

	}//end createTable()

	createTable();



});
