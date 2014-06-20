$(function() {
	$('#getdendro').click( function() {
		var activeFiles = $('#num_active_files').val();
		if (activeFiles < 2) {
			$("#densubmiterrormessage1").show().fadeOut(2500, "swing");
			return false;
		}
		else {
			var thresholdValue = $('#threshold').val();
			var cOption = $('#criterion').val();
			if (cOption == 'inconsistent') {
				// var fileNumberByTen = float(document.getElementById('fileNumberByTen').innerHTML)
				if (thresholdValue >= 0 && thresholdValue < 0.5) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(2500, "swing");
					return false;
				}	
			}
			else 
				if (cOption == 'maxclust') {
				$("#maxclustThreshold").show();
				var fileNumber = Number(document.getElementById('fileNumber').innerHTML);
				if (thresholdValue >= 2 && thresholdValue <= fileNumber) {
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
	
});