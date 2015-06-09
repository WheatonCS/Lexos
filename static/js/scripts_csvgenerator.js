$(function() {
	var timeToToggle = 300;
	$("#labeledittingcsv").click( function() {
		$("#modifylabelscsv").slideToggle(timeToToggle);
	});

	function noErrorMsg() {
		var activeFiles = $('.filenames').length;
		if (activeFiles < 1) {
			$("#csvsubmiterrormessage1").show().fadeOut(2500, "swing");
			return false;
		}
		return true;
	}

	$('#csvdownload, #csvgen').click(function() {
		if (noErrorMsg()){
			return true;
		}
		else
			return false;
	});

	// if ($('#greyword').attr('checked')) {
	// 		$("#csvcontdiv").hide();
	// 	}
	// 	else {
	// 		$("#csvcontdiv").show();
	// }

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
