$(function() {
	
	$(".minifilepreviewsims").click(function() {
		$(this).siblings(".minifilepreviewsims").addClass('enabled');
		$(this).removeClass('enabled');
		$("#uploadname").val($(this).prop('id'));
	});


	$('#getsims').click( function() {
		return true;
	});

	$("form").submit(function() {
		if ($("#uploadname").val() == '') {
			$('#error-message').text("You must select a comparison file!");
			$('#error-message').show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
		else {
			return true;
		}
	});

	function createList() {

		mytable = $('<table></table>').attr({ id: "basicTable" });

		// title row
		var titleRow = $('<tr></tr>').appendTo(mytable);
		$('<td></td>').text("Rank").appendTo(titleRow);
		$('<td></td>').text("Filename").appendTo(titleRow);
		$('<td></td>').text("Cosine Similarity").appendTo(titleRow);

		// rankings
		var rows = (docsListScore.length-1);
		var cols = 3;
		var tr = [];
		for (var i = 0; i < rows; i++) {
			var row = $('<tr></tr>').appendTo(mytable);
			for (var j = 0; j < cols; j++) {

				if (j == 0) {
					$('<td></td>').text(i+1).appendTo(row); 
				} else if (j == 1) {
					$('<td></td>').text(docsListName[i]).appendTo(row); 
				} else {
					$('<td></td>').text(docsListScore[i]).appendTo(row);
				}
			}//for
		}//for

		mytable.appendTo("#simstable"); 



	}

	createList()

});
