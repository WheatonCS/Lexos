$.fn.center = function() {
	this.css("top", Math.max(0, ((($(window).height()) - $(this).outerHeight())/2) - 200) + "px");
	this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth())/2)) + "px");
	return this;
}

function havefiles() {
	return ($('#num_active_files').val() != "0");
}

$(function() {
	$("form").submit(function() {
		if (!havefiles()) {
			$('#error-message').text("You must have active files to proceed!");
			$('#error-message').show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
	});

	// Add "selected" class to parent of selected link
	$(".sublist li .selected").parents('.headernavitem').addClass("selected");

	// display/hide expandable divs here
	$(".has-expansion .icon-arrow-right").click(function() {
		$(this).toggleClass("showing");
		
		$(this).parent('legend').siblings('.expansion').slideToggle(500);
	});

	// Gray out all disabled inputs
	$.each($('input'), function() {
		if ($(this).prop('disabled')) {
			$(this).parent('label').addClass('disabled');
		}
	});

	// Redirect all clicks on "Upload Buttons" to their file upload input
	$('.upload-bttn').click(function() {
		$(this).siblings('input[type=file]').click();
	});
});