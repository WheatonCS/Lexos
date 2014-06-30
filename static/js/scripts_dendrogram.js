$(document).ready( function(){
	var clusterMenu = document.getElementsByClassName("sublist")[3];
	var clusterMenuLi = clusterMenu.getElementsByTagName("li")[1];
	var clusterMenuLiA = clusterMenuLi.getElementsByTagName("a")[0];
	clusterMenuLiA.setAttribute("class", "selected");

	var analyzeMenu = document.getElementsByClassName("headernavitem")[3];
	analyzeMenu.setAttribute("class", "headernavitem selected");
});

$(function() {
	$('#refreshThreshold').click( function() {
		var activeFiles = $('#num_active_files').val();
		if (activeFiles <= 2) {
			$('#error-message').text("You must have enough active files to proceed!");
			$('#error-message').show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
		else {
			var thresholdValue = $('#threshold').val();
			if (thresholdValue !== '') {
				document.getElementById('threshold').value = '';
				return true;
			}
		}
	});

	$('#getdendro').click( function() {
		var activeFiles = $('#num_active_files').val();
		if (activeFiles < 2) {
			$("#densubmiterrormessage1").show().fadeOut(2500, "swing");
			return false;
		}
		else {
			var pruning =  $('#pruning').val();
			if ((Math.abs(Math.round(pruning)) != pruning) || pruning == 1) {
				$('#densubmiterrormessage3').show().fadeOut(2500, "easeInOutCubic");
				return false;
			}
				
			var thresholdValue = $('#threshold').val();
			var cOption = $('#criterion').val();
			if (cOption == 'inconsistent') {
				if ((thresholdValue >= 0 && thresholdValue <= inconsistentMax)|| (thresholdValue == '')) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(2500, "swing");
					return false;
				}	
			}
			else if (cOption == 'maxclust') {
				if ((thresholdValue >= 2 && thresholdValue <= maxclustMax)|| (thresholdValue == '')) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(2500, "swing");
					return false;
				}	
			}
			else if (cOption == 'distance') {
				if ((thresholdValue >= distanceMin && thresholdValue <= distanceMax)|| (thresholdValue == '')) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(2500, "swing");
					return false;
				}	
			}
			else if (cOption == 'monocrit') {
				if ((thresholdValue >= monocritMin && thresholdValue <= monocritMax )|| (thresholdValue == '')) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(2500, "swing");
					return false;
				}	
			}
		}	

	});

	$('#criterion option').each(function() {
		$("#tValue").show();
	});

	$('#threshold').each(function() {
		var default_value = this.value;
		$(this).focus(function(){
			if(this.value == default_value) {
				this.value = '';
			}
		});
	});

	var pdfPage = Number(document.getElementById("pdfPageNumber").innerHTML);
	var pdfHeight = pdfPage * 1491;

	document.getElementById("pdf").height = pdfHeight;
});