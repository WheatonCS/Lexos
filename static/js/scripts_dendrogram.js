$(function() {
	$('#getdendro').click( function() {
		var activeFiles = $('.filenames').length;
		if (activeFiles == 1) {
			$("#densubmiterrormessage1").show().fadeOut(1000, "easeInOutCubic");
			return false;
		}
		return true;
	});
});