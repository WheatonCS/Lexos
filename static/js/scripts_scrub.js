$(function() {
	var timeToToggle = 300;

	// display additional options on load
	$("#advanced-title .icon-arrow-right").addClass("showing");
	optionsDisplaying = true;

	function displayFileName(ev) {
		var files = ev.target.files || ev.dataTransfer.files;

		for (var i = 0, file; file = files[i]; i++) {
			var label = $("#"+ev.target.id).parent().find("#"+ev.target.id+"bttnlabel");
			label.html(file.name);
			label.css('color', '#00B226');
			$("#usecache"+ev.target.id).attr('disabled', 'disabled');
		}
	}

	function changePreviewHeight() {
		// var optionsHeight = $("#prepare-options").height();
		// var buttonsHeight = $("#prepare-submit").outerHeight();
		
		// $("#prepare-wrapper").stop().animate({
		// 	height: optionsHeight + buttonsHeight
		// }, timeToToggle);

		// $("#preview").stop().animate({
		// 	height: optionsHeight + buttonsHeight
		// }, timeToToggle);
	}

	// Register the change callback on the file uploads
	$("#swfileselect").change(displayFileName);
	$("#lemfileselect").change(displayFileName);
	$("#consfileselect").change(displayFileName);
	$("#scfileselect").change(displayFileName);

	$(".bttnfilelabels").click( function() {
		var filetype = $(this).attr('id').replace('bttnlabel', '');
		
		if ($("#usecache"+filetype).attr('disabled') != 'disabled') {
			$(this).css('color', '#FF0000');
			$(this).text($(this).text().replace('(using stored)', ''));
			$("#usecache"+filetype).attr('disabled', 'disabled');
		}
	});

	//-----------------------------------------------------
	$("#stopwords").click( function() {
		$("#stopwordinput").slideToggle(timeToToggle, function(){
			changePreviewHeight();
		});
	});
	$("#prettystopwordsupload").click( function() {
		$("#swfileselect").click();
	});
	//-----------------------------------------------------
	$("#lemmas").click( function() {
		$("#lemmainput").slideToggle(timeToToggle, function(){
			changePreviewHeight();
		});
	});
	$("#prettylemmasupload").click( function() {
		$("#lemfileselect").click();
	});
	//-----------------------------------------------------
	$("#consolidations").click( function() {
		$("#consolidationsinput").slideToggle(timeToToggle, function(){
			changePreviewHeight();
		});
	});
	$("#prettyconsolidationsupload").click( function() {
		$("#consfileselect").click();
	});
	//-----------------------------------------------------
	$("#specialchars").click( function() {
		$("#specialcharsinput").slideToggle(timeToToggle, function(){
			changePreviewHeight();
		});
	});
	$("#prettyspecialcharsupload").click( function() {
		$("#scfileselect").click();
	});

	// display/hide additional options here
	$("#advanced-title .icon-arrow-right").click(function(){
		if (optionsDisplaying) {
			$("#advanced-title .icon-arrow-right").removeClass("showing");
			optionsDisplaying = false;
		} else {
			$("#advanced-title .icon-arrow-right").addClass("showing");
			optionsDisplaying = true;
		}

		$(".advanced-options").slideToggle(500, function() {
			// $(window).trigger('scroll'); // Trigger a dummy event so any changes that need to happen on scrolling will (aka the buttons pop up)
			// Looks glitchy with the above line in, maybe leave out
		});
	});
});



$(function() {
	var timeToToggle = 100;
	$("#punctbox").click( function() {
		if ($(this).children('input').is(':checked')) {
			$("#aposhyph").fadeIn(timeToToggle);
		}
		else {
			$("#aposhyph").fadeOut(timeToToggle);
		}
	});
});