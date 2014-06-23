$(function() {
	$('#getdendro').click( function() {
		var activeFiles = $('#num_active_files').val();
		if (activeFiles < 2) {
			$("#densubmiterrormessage1").show().fadeOut(2500, "swing");
			return false;
		}
		else {
			var thresholdValue = $('#threshold').val();
			var thresholdMax = Number(document.getElementById('thresholdMax').innerHTML);
			var fileNumber = Number(document.getElementById('fileNumber').innerHTML);
			var cOption = $('#criterion').val();
			if (cOption == 'inconsistent') {
				if (thresholdValue >= 0 && thresholdValue <= thresholdMax) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(2500, "swing");
					return false;
				}	
			}
			else if (cOption == 'maxclust') {
				$("#maxclustThreshold").show();
				if ((thresholdValue >= 2 && thresholdValue <= fileNumber) || (fileNumber == 0)) {
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
});