/* Sets a timer to check for scroll events and moves the action buttons when the user 
   scrolls them off the top of the screen */
scrolled = false;
var shiftElement = window.setInterval(shiftElementIfNeeded, 300);
function shiftElementIfNeeded() {
	scrolled = true;
	if (scrolled == true) {
		scrolled = false;
	    var scrollTop = $(window).scrollTop();
	    var targetTop = 100;
	    buttons = $("#action-buttons").html();
	    newEl = $('<div id="action-buttons" style="text-align:right"></div>');
	    newEl.append(buttons);
	    if (scrollTop > targetTop) {
		    $("#action-buttons").remove();
			$("#preview-col").append(newEl);
	    }
	    if (scrollTop <= targetTop) {
		    $("#action-buttons").remove();
			$("#preview-col").prepend(newEl);
	    }
	}
}