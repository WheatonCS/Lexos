/* Sets a timer to check for scroll events and moves the action buttons when the user 
   scrolls them off the top of the screen */
scrolled = false;
var myvar;
var shiftElement = window.setInterval(shiftElementIfNeeded, 300);
function shiftElementIfNeeded() {

	var scrollTop = $(window).scrollTop();
	var targetTop = 100;
	if (scrollTop > targetTop) {
	    buttons = $("#action-buttons").html();
	    newEl = $('<div id="action-buttons" style="text-align:right"></div>');
	    newEl.append(buttons);

		$("#action-buttons").remove();
		$("#preview-col").append(newEl);




	    if (scrollTop <= targetTop) {
		    $("#action-buttons").remove();
			$("#preview-col").prepend(newEl);
			clearInterval(shiftElement);
	    }
	}
}