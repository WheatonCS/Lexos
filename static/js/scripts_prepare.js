$(function() {
	var timer;

	// If the options or the previews are taller than the window, fix the submit div to start with
	if ($("#prepare-options").height() > $(window).height() || 
		$("#prepare-previews").height() > $(window).height()) {
		
		$("#prepare-submit").addClass("fixed");
	}


	// If the options are taller than the preview
	if ($("#prepare-options").height() >= $("#prepare-previews").height()) {	
		$("#prepare-wrapper").height($("#prepare-options").height()+60);
	}
	else { // The preview is taller than the options
		$("#prepare-wrapper").height($("#prepare-previews").height()+60);
	}

	var options = $('#prepare-options');
	var buttons = $('#prepare-submit');

	var buttonsFixed = true;
	var lastScrollTop = 0;

	// if ((buttons.offset().top) <= ($(window).scrollTop()+options.height())) {
	// 	buttons.css("top", ($(window).scrollTop()+options.height()).toString());
	// }

	var topHeight = $('#navbardiv').height() + $('header').height();
	var bottomHeight = $('footer').height();
	var atBottom = false;


	$(window).scroll(function(){
		// Timer stuff
		if (timer) {
			clearTimeout(timer);
		}
		// Timer to throttle the scroll event so it doesn't happen too often
		timer = setTimeout(function(){
			var scrollBottom = $(window).scrollTop() + $(window).height();
			var scrollTop = $(window).scrollTop();

			if (scrollBottom >= $(document).height()){
				atBottom = true;

				$("#prepare-options").addClass("fixed");

			} else {
				atBottom = false;
			}

			var optionsBottom = (options.height()+options.offset().top);

			// if bottom of scroll window at the footer, allow buttons to rejoin page as it goes by
			if ((scrollBottom >= ($('footer').offset().top)) && buttonsFixed) {
				// console.log("Scroll bottom hit footer! On the way down");
				buttons.removeClass("fixed");
				buttonsFixed = false;
			}

			// if bottom of scroll window at the footer, fix button to the screen
			if ((scrollBottom < ($('footer').offset().top)) && !buttonsFixed) {
				// console.log("Scroll bottom hit footer! On the way up");
				buttons.addClass("fixed");
				buttonsFixed = true;
			}

			// if top of scroll window is below the top elements (header, navbar, etc.), then fix the options to the screen
			if ($(window).scrollTop() > topHeight && 
				options.outerHeight() < ($(document).height() - buttons.outerHeight()) ){
				
				options.removeClass("anchorbottom");
				options.addClass("fixed");
			}

			// if nav bar and title come back into view, then unfix the options from the screen, anchor them to the normal spot
			if ($(window).scrollTop() <= topHeight) {
				options.removeClass("anchorbottom");
				options.removeClass("fixed");
			}

			// console.log(($(document).height()-(buttons.height()+$('footer').height())));
			// console.log(options.outerHeight());

			// if the footer is about to push the buttons up, then unfix the options from the screen, anchor them to the bottom
			if (scrollBottom - buttons.height() <= (options.offset().top + options.outerHeight())) {
				// console.log("FIXING TO BOTTOM");
				options.removeClass("fixed");
				options.addClass("anchorbottom");
			}

			// if ((options.outerHeight()))

		}, 10);
	});
});