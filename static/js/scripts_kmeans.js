$(document).ready( function(){
	var clusterMenu = document.getElementsByClassName("sublist")[3];
	var clusterMenuLi = clusterMenu.getElementsByTagName("li")[1];
	var clusterMenuLiA = clusterMenuLi.getElementsByTagName("a")[0];
	clusterMenuLiA.setAttribute("class", "selected");

	var analyzeMenu = document.getElementsByClassName("headernavitem")[3];
	analyzeMenu.setAttribute("class", "headernavitem selected");
});


$(function() {
	$("form").submit(function() {
		var nclusters = $("#nclusters").val();
		var max_iter  = $("#max_iter").val();
		var n_init 	  = $("#n_init").val();
		var tol 	  = $("#tolerance").val();

		if (nclusters > totalFileNumber) {
			$('#error-message').text("K must be less than the number of active files!");
			$('#error-message').show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
		// trap invalid inputs: e.g. input is a float instead of an int (for FireFox)
		else if ((Math.abs(Math.round(nclusters)) != nclusters) || (Math.abs(Math.round(max_iter)) != max_iter)){
			$('#error-message').text("Invalid input! Make sure the input is an integer!");
			$('#error-message').show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
		else if ((Math.abs(Math.round(n_init)) != n_init) && n_init != ''){
			$('#error-message').text("Invalid input! Make sure the input is an integer!");
			$('#error-message').show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
		else if (Math.abs(Math.round(tol)) == tol && tol != ''){
			$('#error-message').text("Invalid input! The relative tolerance must be a decimal!");
			$('#error-message').show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
		else {
			return true;
		}
	});

	function createDictionary() {

		var ChunkSetDict = new Array();

		for(key=0; key < KValue; key++)  {
			ChunkSetDict[key] = [];
		}

		for(i=0; i < tablelabels.length; i++)  {
			ChunkSetDict[dataset[i]].push(tablelabels[i]);
		}

		return ChunkSetDict;

	};//end createDictionary


	function createTable(ChunkSetDict) {

		if ($("#kmeansresultscheck").text() == 'True') {
			$("#kmeansresults").removeClass('hidden');
			$("#kmeansresultscheck").text('');
		
			// start to build an HTML table
			mytable = $('<table></table>').attr({ id: "basicTable" });

			var maxCluster = ChunkSetDict.length;

    		// Color chart
			var colorChart = [
				"#00A6A6",
				"#188B00",
				"#006464",
				"#0090F7",
				"#00F887",
				"#008181",
				"#0067AF",
				"#00BA65",
				"#00548A",
				"#1FB400"
			];

			// create the first row of the table
			var row = $('<tr></tr>').css("backgroundColor","white").appendTo(mytable);
			$('<td></td>').text("Cluster Number").appendTo(row);
			$('<td></td>').text("File Name").appendTo(row);

			// for each different cluster
			for (var i = 0; i < maxCluster; i++) {
				
				var listOfFilesInThisCluster = ChunkSetDict[i];

				// make rows
				for (nextFile=0; nextFile < listOfFilesInThisCluster.length; nextFile++) {
					// column for cluster #

					// colorChart[i % colorChart.length]: select next color modulo max_number_of_available_colors
					var row = $('<tr></tr>').css("backgroundColor",colorChart[i % colorChart.length]).css("opacity", .9).appendTo(mytable);
					$('<td></td>').text(i).appendTo(row);
					$('<td></td>').text(listOfFilesInThisCluster[nextFile]).appendTo(row);
				}//end for nextFile


			}//end for each row

			mytable.appendTo("#ktable");

		} //end if

	}//end createTable()

	ChunkSetDict = createDictionary();
	createTable(ChunkSetDict);



});
