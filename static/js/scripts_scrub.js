$(function() {
	// display additional options on load
	var advancedOptions = $("#advanced-title");
	advancedOptions.find('.icon-arrow-right').addClass("showing");
	advancedOptions.siblings('.expansion').slideToggle(0);

/* Old code used for all upload buttons
	$('.scrub-upload').change(function(ev) {
		filename = ev.target.files[0].name;
	});
*/
	$('#swfileselect').change(function(ev) {
		filename = ev.target.files[0].name;
		if (filename.length > 35) {filename = filename.substring(0, 34) + "...";}
		$("#swfileselectbttnlabel").html(filename);
	});

	$('#lemfileselect').change(function(ev) {
		filename = ev.target.files[0].name;
		if (filename.length > 35) {filename = filename.substring(0, 34) + "...";}
		$("#lemfileselectbttnlabel").html(filename);
	});

	$('#consfileselect').change(function(ev) {
		filename = ev.target.files[0].name;
		if (filename.length > 35) {filename = filename.substring(0, 34) + "...";}
		$("#consfileselectbttnlabel").html(filename);
	});

	$('#scfileselect').change(function(ev) {
		filename = ev.target.files[0].name;
		if (filename.length > 35) {filename = filename.substring(0, 34) + "...";}
		$("#scfileselectbttnlabel").html(filename);
	});


	$(".bttnfilelabels").click( function() {
		var filetype = $(this).attr('id').replace('bttnlabel', '');
		usingCache = $('#usecache'+filetype).attr('disabled') != 'disabled';

		if ((usingCache) || ($(this).attr('id') != '')) {
			$(this).siblings('.scrub-upload').attr('value', '');
			$("#usecache"+filetype).attr('disabled', 'disabled');
			$(this).text('');
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