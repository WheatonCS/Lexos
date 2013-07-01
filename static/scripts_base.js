$(function() {
	alert(document.cookie);
	$("form").submit(function() {
		if ( !($(this).prop('name') == 'reset') ) {
			if (/nofiles/.test(document.cookie)) {
				$("#submiterrormessage1").show().fadeOut(1200, "easeInOutCubic");
				return false;
			}
		}
	});

	$("#bttn-restart").click(function() {
		document.cookie = 'nofiles';
	});
});