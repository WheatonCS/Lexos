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
		$("#prepare-wrapper").height($("#prepare-options").height()+60);
	} else {
		$("#prepare-wrapper").height($("#prepare-previews").height()+60);
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

	if ((buttons.offset.top) <= ($(window).scrollTop()+options.height())) {
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

				$("#prepare-options").addClass("fixed");

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
			if ((scrollBottom-45 < ($('footer').offset().top)) && !buttonsFixed) {
				buttons.addClass("fixed");
				buttonsFixed = true;
			};

			if ($(window).scrollTop() > topHeight && 
				options.outerHeight() < ($(document).height()-buttons.outerHeight()) ){
				
				options.removeClass("fixbottom");
				options.addClass("fixed");
			}

			// if nav bar and title come back into view
			if ($(window).scrollTop() <= topHeight) {
				options.removeClass("fixbottom");
				options.removeClass("fixed");
			}

			console.log(($(document).height()-(buttons.height()+$('footer').height())));
			console.log(options.outerHeight());
			if (($(document).height()-(buttons.height()+$('footer').height())) <= (options.offset().top + options.outerHeight())) {
				console.log("FIXING TO BOTTOM");
				options.removeClass("fixed");
				options.addClass("fixbottom");
			}

			// if ((options.outerHeight()))

		}, 10);
	});
});