$(function() {
	
	
	$('#getkmeans').click( function() {
		return true;
	});

	function createTable() {

		if ($("#kmeansresultscheck").text() == 'True') {
			$("#kmeansresults").removeClass('hidden');
			$("#kmeansresultscheck").text('');
		
			mytable = $('<table></table>').attr({ id: "basicTable" });
			var rows = dataset.length;
			var cols = 2;
			var tr = [];
			for (var i = 0; i < rows+1; i++) {
				var row = $('<tr></tr>').appendTo(mytable);
				for (var j = 0; j < cols; j++) {
					if (i == 0 && j==0) {
						$('<th></th>').text("File Name").appendTo(row);
						document.body.style.backgroundColor = "red";
					}
					else if (i==0 && j==1) {
						$('<th></th>').text("Closest Center Index").appendTo(row);
					}
					else if (j == 0 && i != 0) {
						$('<td></td>').text(tablelabels[i-1]).appendTo(row);
/*						if $('<td></td>').text(tablelabels[i-1]) == '0' {
							row.attr("backgroundColor", "red");
						}*/
					}
					else {
						$('<td></td>').text(dataset[i-1]).appendTo(row);
					}
					 
					}//for
			}//for
			mytable.appendTo("#ktable");

		} //end if

	}//end createTable()

	createTable();



});
