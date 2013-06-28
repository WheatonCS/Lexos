$(function() {
	$("form").submit(function() {
		if (document.cookie == 'nofiles') {
			$("#submiterrormessage1").show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
	});

	$("#bttn-restart").click(function() {
		document.cookie = 'nofiles';
	});
});