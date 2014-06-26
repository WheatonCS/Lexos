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
		
			mytable = $('<table></table>').attr({ id: "basicTable" });
			var rows = ChunkSetDict.length;
			var cols = 2;
			//var tr = [];

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

			var row = $('<tr></tr>').appendTo(mytable);
			$('<th></th>').text("Cluster Number").appendTo(row);
			$('<th></th>').text("File Name").appendTo(row);

			//for (var i = 0; i < rows+1; i++) {
			for (var i = 0; i < rows; i++) {
				var row = $('<tr></tr>').appendTo(mytable);
				// row.addClass("kmeansColorChart");
				// rows of fileName and cluster#
				var listOfFilesInThisCluster = ChunkSetDict[i];

				// make rows
				for (nextFile=0; nextFile < listOfFilesInThisCluster.length; nextFile++) {
					// column for cluster #
					var row = $('<tr></tr>').appendTo(mytable);
					$('<td></td>').text(i).appendTo(row);
					$('<td></td>').text(listOfFilesInThisCluster[nextFile]).appendTo(row);
				}//end for nextFile


			}//end for each row
/*
			// change colors
			var x = document.getElementById("ktable").getElementsByTagName("tr");
    		//x[0].innerHTML = "i want to change my cell color";
    		console.log(x[0]);
    		x[0].style.backgroundColor = "yellow";*/

			mytable.appendTo("#ktable");

		} //end if

	}//end createTable()

	ChunkSetDict = createDictionary();
	createTable(ChunkSetDict);



});
