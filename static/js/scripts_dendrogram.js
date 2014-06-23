$(function() {
	$('#getdendro').click( function() {
		var activeFiles = $('#num_active_files').val();
		if (activeFiles < 2) {
			$("#densubmiterrormessage1").show().fadeOut(2500, "swing");
			return false;
		}
		else {
			var thresholdValue = $('#threshold').val();
			var inconsistentMax = Number(document.getElementById('inconsistentMax').innerHTML);
			var maxclustMax = Number(document.getElementById('maxclustMax').innerHTML);
			var distanceMax = Number(document.getElementById('distanceMax').innerHTML);
			var distanceMin = Number(document.getElementById('distanceMin').innerHTML);
			var monocritMax = Number(document.getElementById('monocritMax').innerHTML);
			var monocritMin = Number(document.getElementById('monocritMin').innerHTML);
			var cOption = $('#criterion').val();
			if (cOption == 'inconsistent') {
				if (thresholdValue >= 0 && thresholdValue <= inconsistentMax) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(2500, "swing");
					return false;
				}	
			}
			else if (cOption == 'maxclust') {
				if ((thresholdValue >= 2 && thresholdValue <= maxclustMax) || (maxclustMax == 0)) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(2500, "swing");
					return false;
				}	
			}
			else if (cOption == 'distance') {
				if (thresholdValue >= distanceMin && thresholdValue <= distanceMax || (maxclustMax == 0)) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(2500, "swing");
					return false;
				}	
			}
			else if (cOption == 'monocrit') {
				if (thresholdValue >= monocritMin && thresholdValue <= monocritMax || (maxclustMax == 0)) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(2500, "swing");
					return false;
				}	
			}
		}	

	});

	var node = document.getElementById('pdfPageNumber');
	var pdfPage = Number(node.innerHTML);
	var pdfHeight = pdfPage * 1491;

	document.getElementById("pdf").height = pdfHeight;

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

	$('#refreshThreshold').click( function() {
		var thresholdValue = $('#threshold').val();
		if (thresholdValue !== '') {
			document.getElementById('threshold').value = '';
		}
	});
});