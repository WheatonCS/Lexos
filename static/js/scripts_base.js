function havefiles() {
	return ($('#num_active_files').val() != "0");
}

$(function() {

	var timer;

	if ($("#alloptions").height() > $(window).height() || 
		$("#preview").height() > $(window).height()) {
		
		$("#basesubmitdiv").addClass("fixed");
		$("#basesubmitdivbuttons").addClass("fixed");
	}

	$("#basesubmitdiv").stop().animate({
		"background-color": "#fff",
		opacity: 0.94
	}, 10);

	if ($("#alloptions").height() >= $("#preview").height()) {
		$(".optionsandpreviewwrapper").height($("#alloptions").height()+60);
	} else {
		$(".optionsandpreviewwrapper").height($("#preview").height()+60);
	}

	$("form").submit(function() {
		if (!havefiles()) {
			$("#submiterrormessage1").show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
	});

	// throttle scroll event
	$(window).scroll(function(){
		if (timer) {
			clearTimeout(timer);
		}
		timer = setTimeout(function(){
			// fix buttons to bottom
			var offset = $(".footer").height();

			if($(window).scrollTop() > 90) {
				$("#alloptions").addClass("fixed");
			} else {
				$("#alloptions").removeClass("fixed");
			}

			if($(window).scrollTop() + $(window).height() < $(document).height()-90) {
				$("#basesubmitdiv").addClass("fixed");
				$("#basesubmitdivbuttons").addClass("fixed");
				// $("#alloptions").addClass("fixed");


				$("#basesubmitdiv").stop().animate({
					"background-color": "#fff",
					opacity: 0.94
				}, 100);
			} else {
				$("#basesubmitdiv").removeClass("fixed");
				$("#basesubmitdivbuttons").removeClass("fixed");
				// $("#alloptions").removeClass("fixed");

				$("#basesubmitdiv").stop().animate({
					"background-color": "none",
					opacity: 1
				}, 100);
			}
		}, 10);
	});
});