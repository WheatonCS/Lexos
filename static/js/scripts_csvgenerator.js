$(function() {

	// Handle exceptions when buttons are clicked
	$('#csvdownload, #csvgen').click(function() {
		var activeFiles = $('.filenames').length;
		if (activeFiles < 1) {
			$("#csvsubmiterrormessage1").show().fadeOut(3000, "easeInOutCubic");
			return false;
		}
		return true;
	});

	function updateGrey() {
		if ( $("#greyword").is(':checked') || $("#culling").is(":checked") || $("#MFW").is(":checked") ) {
			$("#csvcontdiv").show();
		}
		else {
			$("#csvcontdiv").hide();
		}
	}

	updateGrey();

	$("#greyword").click(updateGrey);
	$("#culling").click(updateGrey);
	$("#MFW").click(updateGrey);

});
