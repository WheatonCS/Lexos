$(function() {

	$("#normalize-options").hide();

	$("form").submit(function() {
	
		$("#status-prepare").css({"visibility":"visible", "z-index": "400000"});

		var activeFiles = $('#num_active_files').val();
		if (activeFiles < 2) {
			$("#kmeansubmiterrormessage1").show().fadeOut(3000, "easeInOutCubic");
			return false;
		}
		else{
		var nclusters = $("#nclusters").val();
		var max_iter  = $("#max_iter").val();
		var n_init 	  = $("#n_init").val();
		var tol 	  = $("#tolerance").val();

		if (nclusters > totalFileNumber) {
			$('#error-message').text("K must be less than the number of active files!");
			$('#error-message').show().fadeOut(3000, "easeInOutCubic");
			return false;
		}
		// trap invalid inputs: e.g. input is a float instead of an int (for FireFox)
		else if ((Math.abs(Math.round(nclusters)) != nclusters) || (Math.abs(Math.round(max_iter)) != max_iter)){
			$('#error-message').text("Invalid input! Make sure the input is an integer!");
			$('#error-message').show().fadeOut(3000, "easeInOutCubic");
			return false;
		}
		else if ((Math.abs(Math.round(n_init)) != n_init) && n_init != ''){
			$('#error-message').text("Invalid input! Make sure the input is an integer!");
			$('#error-message').show().fadeOut(3000, "easeInOutCubic");
			return false;
		}
		else if (Math.abs(Math.round(tol)) == tol && tol != ''){
			$('#error-message').text("Invalid input! The relative tolerance must be a decimal!");
			$('#error-message').show().fadeOut(3000, "easeInOutCubic");
			return false;
		}
		else {
			return true;
		}
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

			// Get the image link and create enlarge button
			var link = $("#kmeansimage").attr("src");
			$(".imageLink").attr("href", link);
			var btn = $('<input class="bttn bttn-action" value="Enlarge Graph">');
			btn.appendTo($(".imageLink"));
			
			// for each different cluster
			var maxCluster = ChunkSetDict.length;
			for (var i = 0; i < maxCluster; i++) {
				
				var listOfFilesInThisCluster = ChunkSetDict[i];

				// make rows
				for (nextFile=0; nextFile < listOfFilesInThisCluster.length; nextFile++) {
					var row = $('<tr/>')
					 .css("backgroundColor",colorChart[i])
					 .css("opacity", 1.0)
					 .appendTo("#basicTable");
					$('<td/>').text(i).appendTo(row);
					$('<td/>')
					.text(listOfFilesInThisCluster[nextFile])
					.appendTo(row);
				}//end for nextFile
			}//end for each row
		} //end if
	}//end createTable()

	ChunkSetDict = createDictionary();
	createTable(ChunkSetDict);
});