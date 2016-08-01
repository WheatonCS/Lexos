$(document).ready( function(){
	//  Dynamically change the height of the embedded image
	pdfPageNumber = 1;
	$(".dendroImage").height(pdfPageNumber*120+"vh");

	// Function to convert the form data into a JSON object
	function jsonifyForm() {
	    var form = {};
	    $.each($("form").serializeArray(), function (i, field) {
	        form[field.name] = field.value || "";
	    });
	    return form;
	}

	function doAjax(action) {
		var form = jsonifyForm();
		var extension = {};
		extension[action] = true;
		$.extend(form, extension);
	    $.ajax({
            "type": "POST",
            "url": "/cluster",
            "contentType": 'application/json; charset=utf-8',
            "dataType": "json",
            "data": JSON.stringify(form),
            //"beforeSend": function(form) {
            //    console.log("Before Send: "+JSON.stringify(form));
            //},
            "complete": function(response) {
            	$("#pdf").attr("src", "/dendrogramimage?"+response["responseJSON"]["ver"]);
            	$("#scoreSpan").html(response["responseJSON"]["score"]);
            	$("#criterionSpan").html(response["responseJSON"]["criterion"]);
            	$("#thresholdSpan").html(response["responseJSON"]["threshold"]);
            	$(".generated").removeClass("hidden");
            	//console.log("Response: "+JSON.stringify(response));
            	document.getElementById("graph-anchor").scrollIntoView({block: "start", behavior: "smooth"});
            	$("#status-analyze").css({"visibility":"hidden"});
            }
        }//end ajax
    )};

	// Events after 'Get Dendrogram' is clicked, handle exceptions
	$('#getdendro, #dendroPDFdownload, #dendroSVGdownload, #dendroPNGdownload, #dendroNewickdownload, #download').on("click", function() {
		var err1 = 'A dendrogram requires at least 2 active documents to be created.';
	    var err2 = "Invalid Threshold.";
	    var err3 = "Invalid number of leaves.";
		var activeFiles = $('#num_active_files').val();
		var action = $(this).attr("id");

		if (activeFiles < 2) {
			$("#status-analyze").css({"visibility":"hidden"});
	        $('#error-modal-message').html(err1);
	        $('#error-modal').modal(); 			
		}
		else {
			var pruning =  $('#pruning').val();
			if ((Math.abs(Math.round(pruning)) != pruning) || pruning == 1) {
				$("#status-analyze").css({"visibility":"hidden"});
		        $('#error-modal-message').html(err3);
		        $('#error-modal').modal(); 	
			}
				
			var thresholdValue = $('#threshold').val();
			var cOption = $('#criterion').val();
			if (cOption == 'inconsistent') {
				if ((thresholdValue >= 0 && thresholdValue <= inconsistentMax)|| (thresholdValue == '')) {
					if (action == "getdendro") {
						$("#status-analyze").css({"visibility":"visible", "z-index": "400000"});
						doAjax(action);
					}
				}
				else {
					$("#status-analyze").css({"visibility":"hidden"});
			        $('#error-modal-message').html(err2);
			        $('#error-modal').modal(); 	
				}	
			}
			else if (cOption == 'maxclust') {
				if ((thresholdValue >= 2 && thresholdValue <= maxclustMax)|| (thresholdValue == '')) {
					if (action == "getdendro") {
						$("#status-analyze").css({"visibility":"visible", "z-index": "400000"});
						doAjax(action);
					}
				}
				else {
					$("#status-analyze").css({"visibility":"hidden"});
			        $('#error-modal-message').html(err2);
			        $('#error-modal').modal();
					if (action == "getdendro") { doAjax(action); }
				}	
			}
			else if (cOption == 'distance') {
				if ((thresholdValue >= distanceMin && thresholdValue <= distanceMax)|| (thresholdValue == '')) {
					if (action == "getdendro") {
						$("#status-analyze").css({"visibility":"visible", "z-index": "400000"});
						doAjax(action);
					}
				}
				else {
					$("#status-analyze").css({"visibility":"hidden"});
			        $('#error-modal-message').html(err2);
			        $('#error-modal').modal(); 
				}	
			}
			else if (cOption == 'monocrit') {
				if ((thresholdValue >= monocritMin && thresholdValue <= monocritMax )|| (thresholdValue == '')) {
					if (action == "getdendro") {
						$("#status-analyze").css({"visibility":"visible", "z-index": "400000"});
						doAjax(action);
					}
				}
				else {
					$("#status-analyze").css({"visibility":"hidden"});
			        $('#error-modal-message').html(err2);
			        $('#error-modal').modal(); 
				}	
			}
		}
	});
	
	// Update threshold values
	$('#threshold').each(function() {
		var default_value = this.value;
		$(this).focus(function(){
			if(this.value == default_value) {
				this.value = '';
			}
		});
	});
	// Calculate the threshold values based on criterions
	var inconsistentrange = "0 ≤ t ≤ ";
	var maxclustRange = "2 ≤ t ≤ ";
	var range = " ≤ t ≤ ";

	var inconsistentMaxStr = inconsistentMax.toString(); 
	var maxclustMaxStr = maxclustMax.toString();
	var distanceMaxStr = distanceMax.toString();
	var monocritMaxStr = monocritMax.toString();

	var distanceMinStr = distanceMin.toString();
	var monocritMinStr = monocritMin.toString();

	var inconsistentOp = inconsistentrange.concat(inconsistentMaxStr);
	var maxclustOp = maxclustRange.concat(maxclustMaxStr);
	var distanceOp = distanceMinStr.concat(range,distanceMaxStr);
	var monocritOp = monocritMinStr.concat(range,monocritMaxStr);

	var placeholderText = {"Inconsistent":inconsistentOp, "Maxclust": maxclustOp, "Distance": distanceOp, "Monocrit":monocritOp};

	$("#criterion").on("change",function() {
		var selectedVal = $('#criterion').find(':selected').text();
		$("#threshold").attr("placeholder", placeholderText[selectedVal]);
	}).on("click",function() {
		var selectedVal = $('#criterion').find(':selected').text();
		$("#threshold").attr("placeholder", placeholderText[selectedVal]);
	});
});