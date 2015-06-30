$.fn.center = function() {
	this.css("top", Math.max(0, ((($(window).height()) - $(this).outerHeight())/2) - 200) + "px");
	this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth())/2)) + "px");
	return this;
}

$(function() {

	// Load the Scalar API and cache it.
	$.ajax({
		url: "scalarapi.js",
		dataType: "script",
		cache: true
	});

	// Handle exceptions for submitting forms and display error messages on screen
	$("form").submit(function() {
		if ($('#num_active_files').val() == "0") {
			$('#error-message').text("You must have active documents to proceed!");
			$('#error-message').show().fadeOut(3000); // Use easeInOutCubic effect can cause program crash on analyzer pages

			$("#status-prepare").hide();
			// $('<div id="error-warning">You must have active files to proceed. Please select one or more files on the Select screen.</div>').dialog({
			// 	title: '<span class="ui-icon ui-icon-alert"></span> Error!'
			// });
			return false;
		} else
			return true;
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

	// Show the nested submenu of clustering when mouse hover over the corresponding navbar, otherwise hide the nested menu
	$("#clustering-menu, #clustering-submenu").mouseover(function(){
		$("#clustering-submenu").css({"opacity": 1, "visibility": "visible"});
	}).mouseleave(function(){
		$("#clustering-submenu").css({"opacity": 0, "visibility": "hidden"});
	});

	// Highlight the nested label of the navBar when nested pages are active
	if ($(".nestedElement").hasClass("selected")){
		$(".nestedLabel").addClass("selected");
	}

});