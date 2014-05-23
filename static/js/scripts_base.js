function havefiles() {
	return ($('#num_active_files').val() != "0");
}

$(function() {
	$("form").submit(function() {
		if (!havefiles()) {
			$("#submiterrormessage1").show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
	});

	// highlights current analysis tool and nav bar item it belongs to
	$(".sublist li .current").toggleClass("selected");	

	if($(".sublist li .current").length > 0){
		// gets the nav bar item associated with the selected page
		$(".sublist li .current").parent().parent().parent().toggleClass("selected");
	}

	var timer;

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

			// console.log(($(document).height()-(buttons.height()+$('footer').height())));
			// console.log(options.outerHeight());
			if (($(document).height()-(buttons.height()+$('footer').height())) <= (options.offset().top + options.outerHeight())) {
				// console.log("FIXING TO BOTTOM");
				options.removeClass("fixed");
				options.addClass("fixbottom");
			}

		}, 10);
	});	
});