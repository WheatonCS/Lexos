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

	function updateGrey() {
		if ($('input[type=checkbox][name=greyword]').attr('checked')) {
			document.getElementById("csvcontdiv").style.visibility = "visible";
		}
		else {
			document.getElementById("csvcontdiv").style.visibility = "hidden";
		}

		// $('input[type=checkbox][name=greyword]').click(function(){
		// 	if ($('input[type=checkbox][name=greyword]').attr(':checked')) {
		// 		$("csvcontdiv").hide();
		// 	} else {
		// 		$("csvcontdiv").show();
		// 	}
		// });
	}

	$('input[type=checkbox][name=greyword]').click(updateGrey);

	updateGrey();

});
