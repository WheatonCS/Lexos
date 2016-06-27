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

	$("#getkmeans").click(function() {
		// Display the processing icon
		$("#status-analyze").css({"visibility":"visible", "z-index": "400000"});

		// Get variable values from the DOM
		var activeFiles = $('#num_active_files').val();
		var nclusters = $("#nclusters").val();
		var max_iter  = $("#max_iter").val();
		var n_init 	  = $("#n_init").val();
		var tol 	  = $("#tolerance").val();

		// Error messages
		var err1 = "<p>K-means requires at least 2 active documents.</p>";
		var err2 = "<p>The number of clusters (K value) must not be larger than the number of active files!</p>";
		var err3 = "<p>Invalid input. Make sure the input is an integer.</p>";
		var err4 = "<p>Invalid input. The relative tolerance must be a decimal.</p>";

		// Less than 2 active documents
		if (activeFiles < 2) {
			$("#error-modal .modal-body").html(err1);
			$("#error-modal").modal();

		}
		// K is larger than the number of active documents
		else if (nclusters > totalFileNumber) {
			$("#error-modal .modal-body").html(err2);
			$("#error-modal").modal();
		}
		// Trap invalid inputs: e.g. input is a float instead of an int (for FireFox)
		else if ((Math.abs(Math.round(nclusters)) != nclusters) || (Math.abs(Math.round(max_iter)) != max_iter)){
			$("#error-modal .modal-body").html(err3);
			$("#error-modal").modal();
		}
		else if ((Math.abs(Math.round(n_init)) != n_init) && n_init != ''){
			$("#error-modal .modal-body").html(err3);
			$("#error-modal").modal();
		}
		else if (Math.abs(Math.round(tol)) == tol && tol != ''){
			$("#error-modal .modal-body").html(err4);
			$("#error-modal").modal();
		}
		else {
			$("form").submit();
		}
		$("#error-modal").on('hidden.bs.modal', function () {
			$("#status-analyze").fadeOut()
		})
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
						.attr("class",listOfFilesInThisCluster[nextFile].replace(/\./g, ''))
					 .appendTo("#basicTable tbody");
					$('<td style="text-align:center;"/>').text(i).appendTo(row);
					$('<td style="text-align:left;"/>')
					.text(listOfFilesInThisCluster[nextFile])
					.appendTo(row);
					j += 1;
				}//end for nextFile
			}//end for each row
			
		} //end if
	}//end createTable()

	// The if clause prevents functions from running on initial page load
	if (dataset.length > 0) {
		ChunkSetDict = createDictionary();
		createTable(ChunkSetDict);
	}

    $("svg circle").tooltip({
        'container': 'body',
        'placement': 'right'
    });

	// Handle table mouseovers for Voronoi points
	$("#basicTable tbody tr")
		.mouseenter(function() {
			$(this).css("opacity", "0.6");
			id = $(this).attr("class");
			point = ".P"+id;
			text = ".T"+id;
			$(point).appendTo("#voronoi");
			$(text).appendTo("#voronoi");
			$(point).css("fill", "yellow");
			$(point).tooltip('show');  
 
	  	})
		.mouseleave(function() {
			$(this).css("opacity", "1.0");
			id = $(this).attr("class");
			point = ".P"+id;
			$(point).css("fill", "red");  
			$(point).tooltip('hide'); 
	  	});
});