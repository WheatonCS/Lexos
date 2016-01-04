// jScroll http://www.wduffy.co.uk/jScroll/
(function($){$.fn.jScroll=function(e){var f=$.extend({},$.fn.jScroll.defaults,e);return this.each(function(){var a=$(this);var b=$(window);var c=new location(a);b.scroll(function(){a.stop().animate(c.getMargin(b),f.speed)})});function location(d){this.min=d.offset().top;this.originalMargin=parseInt(d.css("margin-top"),10)||0;this.getMargin=function(a){var b=d.parent().height()-d.outerHeight();var c=this.originalMargin;if(a.scrollTop()>=this.min)c=c+f.top+a.scrollTop()-this.min;if(c>b)c=b;return({"marginTop":c+'px'})}}};$.fn.jScroll.defaults={speed:"slow",top:10}})(jQuery);

$(function() {
     $(".scroll").jScroll({speed : "fast", top: 100});

// Old code
/*	// Change position of submit div while scrolling the window
	var timer;
	var buttonsFixed = false;
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
*/
});