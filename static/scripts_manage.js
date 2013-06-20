$(function() {
	$(".navbaroption").click(function() {
		$(this).next("input").click();
	});

	$(".filepreview").click(function() {
		var inputToToggle = $(this).children('.filestatus');
		// alert(inputToToggle.prop('disabled'));
		inputToToggle.prop('disabled', !inputToToggle.prop('disabled'));
		$(this).toggleClass('enabled');
	});
});