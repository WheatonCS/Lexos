$(function() {
	var timeToToggle = 300;
	$("#labeledittingcsv").click( function() {
		$("#modifylabelscsv").slideToggle(timeToToggle);
	});

	$('#csvdownload, #csvgen').click(function() {
		var activeFiles = $('.filenames').length;
		if (activeFiles < 1) {
			$("#csvsubmiterrormessage1").show().fadeOut(2500, "swing");
			return false;
		}
		return true;
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

		// $('input[type=checkbox][name=greyword]').click(function(){
		// 	if ($('input[type=checkbox][name=greyword]').attr(':checked')) {
		// 		$("csvcontdiv").hide();
		// 	} else {
		// 		$("csvcontdiv").show();
		// 	}
		// });
	}

	updateGrey();

	$("#greyword").click(updateGrey);
	$("#culling").click(updateGrey);
	$("#MFW").click(updateGrey);


});
