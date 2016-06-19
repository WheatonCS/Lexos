$(function() {

	// Show the silhouette score results based whether the results are shown
	if ($("#kmeansresults").length) {
		$("#silhouetteResults").show();
	}
	else {
		$("#silhouetteResults").hide();	
	}

	// Hide unnecessary divs for DTM
	var newLabelsLocation = $("#normalize-options").parent();
	var newNormalizeLocation = $("#temp-label-div").parent();
	var tempNormalize = $("#normalize-options").html();
	var tempLabels = $("#temp-label-div").html();
	$("#normalize-options").remove();
	$("#temp-label-div").remove();
	newLabels = $('<fieldset class="analyze-advanced-options" id="temp-label-div"></fieldset>').append(tempLabels);
	newNormalize = $('<fieldset class="analyze-advanced-options" id="normalize-options"></fieldset>').append(tempNormalize);
	newLabelsLocation.append(newLabels);
	newNormalizeLocation.append(newNormalize);

	$("#normalize-options").hide();

	/* This event is handled in scripts_analyze.js, but for some reason it has to be 
	   repeated here to function. */
	$(".has-chevron").on("click", function() {
		$(this).find("span").toggleClass("down");
		$(this).next().collapse('toggle');
	});

	//$("#normalize-options").css({"visibility":"hidden"});

	$("form").submit(function() {
	
		$("#status-analyze").css({"visibility":"visible", "z-index": "400000"});

		var activeFiles = $('#num_active_files').val();
		if (activeFiles < 2) {
			$('#error-message').text("K-means requires at least 2 active documents to be created.");
			$('#error-message').show().fadeOut(3000, "easeInOutCubic");
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
			var j = 1;
			for (var i = 0; i < maxCluster; i++) {
				
				var listOfFilesInThisCluster = ChunkSetDict[i];

				// make rows
				for (nextFile=0; nextFile < listOfFilesInThisCluster.length; nextFile++) {
					var row = $('<tr id="text'+j+'-toggle"></tr>')
					 .css("backgroundColor",colorChart[i])
					 .css("opacity", 1.0)
					 .appendTo("#basicTable tbody");
					$('<td/>').text(i).appendTo(row);
					$('<td/>')
					.text(listOfFilesInThisCluster[nextFile])
					.appendTo(row);
					j += 1;
				}//end for nextFile
			}//end for each row
		} //end if
	}//end createTable()

	ChunkSetDict = createDictionary();
	createTable(ChunkSetDict);

    $("svg circle").tooltip({
        'container': 'body',
        'placement': 'right'
    });

	// Handle table mouseovers for Voronoi points
	$("#basicTable tbody tr")
		.mouseenter(function() {
			$(this).css("opacity", "0.6");
			id = $(this).attr("id").replace("text", "");
			id = id.replace("-toggle", "");
			point = "#point"+id;
			text = "#text"+id;
			$(point).css("fill", "yellow");
			$(point).parent().append(point);
			$(text).parent().append(text);  
			$(point).tooltip('show');  
 
	  	})
		.mouseleave(function() {
			$(this).css("opacity", "1.0");
			id = $(this).attr("id").replace("text", "");
			id = id.replace("-toggle", "");
			point = "#point"+id;
			$(point).css("fill", "red");  
			$(point).tooltip('hide'); 
	  	});
});