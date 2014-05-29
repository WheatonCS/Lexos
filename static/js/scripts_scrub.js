$(function() {
	// display additional options on load
	$("#advanced-title .icon-arrow-right").addClass("showing");
	optionsDisplaying = true;

	$('.scrub-upload').change(function(ev) {
		filename = ev.target.files[0].name;

		$(this).siblings('.bttnfilelabels').html(filename);
	});

	$(".bttnfilelabels").click( function() {
		var filetype = $(this).attr('id').replace('bttnlabel', '');
		
		if ($("#usecache"+filetype).attr('disabled') != 'disabled') {
			$(this).css('color', '#FF0000');
			$(this).text($(this).text().replace('(using stored)', ''));
			$("#usecache"+filetype).attr('disabled', 'disabled');
		}
	});

	$("#punctbox").click( function() {
		var timeToToggle = 100;
		if ($(this).children('input').is(':checked')) {
			$("#aposhyph").fadeIn(timeToToggle);
		}
		else {
			$("#aposhyph").fadeOut(timeToToggle);
		}
	});
});