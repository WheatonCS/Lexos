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
		var newHeight = $("#prepare-options").height()+70;
		$(".optionsandpreviewwrapper").height(newHeight);
	} else {
		var newHeight = $("#prepare-previews").height()+70;
		$(".optionsandpreviewwrapper").height(newHeight);
	}

	$("form").submit(function() {
		if (!havefiles()) {
			$("#submiterrormessage1").show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
	});

	var options = $('#prepare-options');
	var buttons = $('#prepare-submit');

	var buttonsFixed = true;
	var lastScrollTop = 0;

	if ((buttons.offset().top) <= ($(window).scrollTop()+options.height())) {
		buttons.css("top", ($(window).scrollTop()+options.height()).toString());
	}

	var topHeight = $('#navbardiv').height() + $('header').height();
	var atBottom = false;

	// throttle scroll event
	$(window).scroll(function(){
		if (timer) {
			clearTimeout(timer);
		}
		timer = setTimeout(function(){
			// fix buttons to bottom
			var scrollBottom = $(window).scrollTop() + $(window).height() + $('footer').height();

			if (scrollBottom >= $(document).height()){
				atBottom = true;
			} else {
				atBottom = false;
			}

			var optionsBottom = (options.height()+options.offset().top);

			// if at bottom of the page, remove fixed class for buttons
			if ((buttons.offset().top >= ($('footer').offset().top-buttons.height())) && buttonsFixed) {
				buttons.removeClass("fixed");
				buttonsFixed = false;
			};

			// if bottom of window at bottom of buttons, add fixed class
			if ((scrollBottom-50 < ($('footer').offset().top)) && !buttonsFixed) {
				buttons.addClass("fixed");
				buttonsFixed = true;
			};

			if ($(window).scrollTop() > topHeight && 
				options.outerHeight() < ($(document).height()-
										(buttons.outerHeight()+$('footer').outerHeight()+$('legend').outerHeight())) ){
				
				options.removeClass("fixbottom");
				options.addClass("fixed");
			}

			// if nav bar and title come back into view
			if ($(window).scrollTop() <= topHeight) {
				options.removeClass("fixbottom");
				options.removeClass("fixed");
			}

			if (($(document).height()-(buttons.height()*2+$('footer').height())) <= (options.offset().top+options.height())) {
				options.removeClass("fixed");
				options.addClass("fixbottom");
			}

		}, 10);
	});
});