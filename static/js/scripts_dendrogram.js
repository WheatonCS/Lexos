$(function() {

	var timeToToggle = 300;
	$("#labeleditting").click( function() {
		$("#modifylabels").slideToggle(timeToToggle);
	});

	$('#getdendro').click( function() {
		var activeFiles = $('.filenames').length;
		if (activeFiles < 2) {
			$("#densubmiterrormessage1").show().fadeOut(2500, "swing");
			return false;
		}
		return true;
	});
});