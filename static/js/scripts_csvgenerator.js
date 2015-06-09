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

	function updateGrey() {
		if ($('input[type=checkbox][name=greyword]').attr('checked')) {
			document.getElementById("csvcontdiv").style.visibility = "visible";
		}
		else {
			document.getElementById("csvcontdiv").style.visibility = "hidden";
		}
	}

	$('input[type=checkbox][name=greyword]').click(updateGrey);

	updateGrey();

});
