$(function() {
	$('#getdendro').click( function() {
		var activeFiles = $('#num_active_files').val();
		if (activeFiles < 2) {
			$("#densubmiterrormessage1").show().fadeOut(2500, "swing");
			return false;
		}
		return true;
	});

	var pdfPage = document.getElementById("pdfPageNumber");
    var node = document.getElementById('pdfPageNumber');
	var pdfPage = Number(node.innerHTML);
	var pdfHeight = pdfPage * 1400;

	document.getElementById("pdf").height = pdfHeight; 
});