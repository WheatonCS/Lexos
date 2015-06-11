$(document).ready( function(){
	if (matrixExist === 0){
		// Disable dtm toggle when matrix
		$(".toggle-dtm").unbind("click")
						.css("background-color", "gray");
	}	
});

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
