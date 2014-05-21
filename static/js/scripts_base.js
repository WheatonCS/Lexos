function havefiles() {
	return ($('#num_active_files').val() != "0");
}

$(function() {

	var timer;

	if ($("#prepare-options").height() > $(window).height() || 
		$("#prepare-previews").height() > $(window).height()) {
		
		$("#prepare-submit").addClass("fixed");
	}

	$("#prepare-submit").stop().animate({
		"background-color": "#fff",
		opacity: 0.94
	}, 10);

	if ($("#prepare-options").height() >= $("#prepare-previews").height()) {
		$(".optionsandpreviewwrapper").height($("#prepare-options").height()+60);
	} else {
		$(".optionsandpreviewwrapper").height($("#prepare-previews").height()+60);
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
				$("#prepare-options").addClass("fixed");
			} else {
				$("#prepare-options").removeClass("fixed");
			}

			if($(window).scrollTop() + $(window).height() < $(document).height()-90) {
				$("#prepare-submit").addClass("fixed");

				$("#prepare-submit").stop().animate({
					"background-color": "#fff",
					opacity: 0.94
				}, 100);
			} else {
				$("#prepare-submit").removeClass("fixed");

				$("#prepare-submit").stop().animate({
					"background-color": "none",
					opacity: 1
				}, 100);
			}
		}, 10);
	});
});