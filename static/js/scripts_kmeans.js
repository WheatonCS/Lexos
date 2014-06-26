$(function() {
	
	$(document).ready( function(){
		var clusterMenu = document.getElementsByClassName("sublist")[3];
		var clusterMenuLi = clusterMenu.getElementsByTagName("li")[1];
		var clusterMenuLiA = clusterMenuLi.getElementsByTagName("a")[0];
		clusterMenuLiA.setAttribute("class", "selected");

		var analyzeMenu = document.getElementsByClassName("headernavitem")[3];
		analyzeMenu.setAttribute("class", "headernavitem selected");
	});

	$("form").submit(function() {
		if ($("#nclusters").val() == '') {
			$('#error-message').text("You must provide a K value!");
			$('#error-message').show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
		else if ($("#max_iter").val() == '') {
			$('#error-message').text("You must provide the number of iterations!");
			$('#error-message').show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
		else {
			return true;
		}
	});


	function createTable() {

		if ($("#kmeansresultscheck").text() == 'True') {
			$("#kmeansresults").removeClass('hidden');
			$("#kmeansresultscheck").text('');
		
			mytable = $('<table></table>').attr({ id: "basicTable" });
			var rows = dataset.length;
			var cols = 2;
			var tr = [];

    		// Color chart
			var colorChart = [
				"red",
				"orange",
				"yellow",
				"green",
				"blue",
				"purple",
				"violet",
				"tomato",
				"silver",
				"pink"
			];

			for (var i = 0; i < rows+1; i++) {
				var row = $('<tr></tr>').appendTo(mytable);
				for (var j = 0; j < cols; j++) {
					if (i == 0 && j==0) {
						$('<th></th>').text("File Name").appendTo(row);
/*						document.body.style.backgroundColor = "red";
*/					}
					else if (i==0 && j==1) {
						$('<th></th>').text("Closest Center Index").appendTo(row);
					}
					else if (j == 0 && i != 0) {
						$('<td></td>').text(tablelabels[i-1]).appendTo(row);
						//$('<tr></tr>').backgroundColor = "red";
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
