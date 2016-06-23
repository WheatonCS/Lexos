$(document).ready( function(){
	//  Dynamically change the height of the embedded PDF
	//$("#pdf").height(pdfPageNumber * 1400);
	$(".dendroImage").height(pdfPageNumber*120+"vh");

	// Show the silhouette score results based on the PDF height
	if ($("#pdf").height() == 0) {
		$("#silhouetteResults").hide();
		$("#dendrodownload").hide();
		$("#dendroPNGdownload").hide();
		$("#dendroSVGdownload").hide();
		$("#dendroNewickdownload").hide();
		$("#download").hide();
	}
	else {
		$("#silhouetteResults").show();	
		$("#dendrodownload").show();
		$("#dendroPNGdownload").show();
		$("#dendroSVGdownload").show();
		$("#dendroNewickdownload").show();
		$("#download").show();
	}

	// Events after 'Get Dendrogram' is clicked, handle exceptions
	$('#getdendro, #dendrodownload, #dendroSVGdownload, #dendroPNGdownload, #dendroNewickdownload, #download').on("click", function() {

		var activeFiles = $('#num_active_files').val();
		if (activeFiles < 2) {
			$("#densubmiterrormessage1").show().fadeOut(3000, "easeInOutCubic");
			return false;
		}
		else {
			var pruning =  $('#pruning').val();
			if ((Math.abs(Math.round(pruning)) != pruning) || pruning == 1) {
				$('#densubmiterrormessage3').show().fadeOut(3000, "easeInOutCubic");
				return false;
			}
				
			var thresholdValue = $('#threshold').val();
			var cOption = $('#criterion').val();
			if (cOption == 'inconsistent') {
				if ((thresholdValue >= 0 && thresholdValue <= inconsistentMax)|| (thresholdValue == '')) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(3000, "easeInOutCubic");
					return false;
				}	
			}
			else if (cOption == 'maxclust') {
				if ((thresholdValue >= 2 && thresholdValue <= maxclustMax)|| (thresholdValue == '')) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(3000, "easeInOutCubic");
					return false;
				}	
			}
			else if (cOption == 'distance') {
				if ((thresholdValue >= distanceMin && thresholdValue <= distanceMax)|| (thresholdValue == '')) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(3000, "easeInOutCubic");
					return false;
				}	
			}
			else if (cOption == 'monocrit') {
				if ((thresholdValue >= monocritMin && thresholdValue <= monocritMax )|| (thresholdValue == '')) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(3000, "easeInOutCubic");
					return false;
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