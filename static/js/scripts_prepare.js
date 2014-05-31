$(function() {
	var timer;

	var buttonsFixed = false;

	var options = $('#prepare-options');
	var buttons = $('#prepare-submit');


	$(window).scroll(function(){
		// Timer stuff
		if (timer) {
			clearTimeout(timer);
		}
		// Timer to throttle the scroll event so it doesn't happen too often
		timer = setTimeout(function(){
			var scrollBottom = $(window).scrollTop() + $(window).height();
			var scrollTop = $(window).scrollTop();

			var optionsBottom = (options.height()+options.offset().top);

			// if bottom of scroll window at the footer, allow buttons to rejoin page as it goes by
			if (buttonsFixed && (scrollBottom >= ($('footer').offset().top))) {
				// console.log("Scroll bottom hit footer! On the way down");
				buttons.removeClass("fixed");
				buttonsFixed = false;
			}

			// if bottom of scroll window at the footer, fix button to the screen
			if (!buttonsFixed && (scrollBottom < ($('footer').offset().top))) {
				// console.log("Scroll bottom hit footer! On the way up");
				buttons.addClass("fixed");
				buttonsFixed = true;
			}
		}, 10);
	});

	$(window).scroll(); // Call a dummy scroll event after everything is loaded.
});