$(function() {

	var timeToToggle = 300;
	$("#labeleditting").click( function() {
		$("#modifylabels").slideToggle(timeToToggle);
	});

	$('#getdendro').click( function() {
		var activeFiles = $('.filenames').length;
		if (activeFiles == 1) {
			$("#densubmiterrormessage1").show().fadeOut(1000, "easeInOutCubic");
			return false;
		}
		return true;
	});
});