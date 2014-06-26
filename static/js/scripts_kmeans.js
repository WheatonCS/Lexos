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
		else if ($("#nclusters").val() > totalFileNumber) {
			$('#error-message').text("K must be less than the number of active files!");
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

			// create the first row of the table
			var row = $('<tr></tr>').css("backgroundColor","white").appendTo(mytable);
			$('<th></th>').text("Cluster Number").appendTo(row);
			$('<th></th>').text("File Name").appendTo(row);

			// for each different cluster
			for (var i = 0; i < maxCluster; i++) {
				
				var listOfFilesInThisCluster = ChunkSetDict[i];

				// make rows
				for (nextFile=0; nextFile < listOfFilesInThisCluster.length; nextFile++) {
					// column for cluster #

					// colorChart[i % colorChart.length]: select next color modulo max_number_of_available_colors
					var row = $('<tr></tr>').css("backgroundColor",colorChart[i % colorChart.length]).appendTo(mytable);
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
