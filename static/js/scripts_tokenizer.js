$(function() {
	$('#csvgen').click(function() {
		$("#loading-div").css({"visibility": "visible", "z-index": "400000"});
	});
	
	// Handle exceptions when buttons are clicked
	$('#csvdownload, #csvgen').click(function() {
		var activeFiles = $('#num_active_files').val();
		console.log(activeFiles);
		if (activeFiles < 1) {
			$('#error-message').text("You must have active documents to proceed!");
			$("#error-message").show().fadeOut(3000,"easeInOutCubic");
			return false;
		}
		return true;
	});

	function updateCSVcontentOption() {
		if ( $("#greyword").is(':checked') || $("#culling").is(":checked") || $("#MFW").is(":checked") ) {
			$("#csvcontdiv").show();
		}
		else {
			$("#csvcontdiv").hide();
		}
	}

	updateCSVcontentOption();

	$("#greyword").click(updateCSVcontentOption);
	$("#culling").click(updateCSVcontentOption);
	$("#MFW").click(updateCSVcontentOption);

});
