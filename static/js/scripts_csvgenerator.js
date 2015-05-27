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

	$('#csvdownload').click(function() {
		if (noErrorMsg()){
			return true;
		}
		else
			return false;
	});

	$('#csvgen').click(function() {
		if (noErrorMsg()){
			var matrixData = $('#csvgen').data();
			var jsonData = JSON.stringify(matrixData);

			matrixTitle = matrixData["title"]

			matrixArray = [];
			matrixArray.push(matrixData["matrix"]);

			$("#csvstatsTable").dialog({
				width: 375,
				height: 300
			});

			return true;
		}
		else
			return false;
	});
});
