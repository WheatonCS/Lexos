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

	// highlights current analysis tool
	// $(".sublist li .current").toggleClass("selected");

	var selectedPageNavBar = $(".sublist li .current");

	selectedPageNavBar.parent().parent().addClass("selected");
});