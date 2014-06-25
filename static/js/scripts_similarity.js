$(function() {
	
	$(".minifilepreviewsims").click(function() {
		$(this).siblings(".minifilepreviewsims").addClass('enabled');
		$(this).removeClass('enabled');
		$("#uploadname").val($(this).prop('id'));
	});


	$('#getsims').click( function() {
		console.log("CLICKED GET SIMS");
		return true;
	});

	function createList() {

		mytable = $('<table></table>').attr({ id: "basicTable" });

		var rows = docsList.length-1;
		var cols = 2;
		var tr = [];
		for (var i = 0; i < rows; i++) {
			var row = $('<tr></tr>').appendTo(mytable);
			for (var j = 0; j < cols; j++) {

				if (j == 0) {
					$('<td></td>').text(i+1).appendTo(row); 
				} else {
				$('<td></td>').text(docsList[i]).appendTo(row); 
				}
			}//for
		}//for

		mytable.appendTo("#simstable"); 

		console.log("done!");



	}

	createList()

});
