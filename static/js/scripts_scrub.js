$(function() {

	var timeToToggle = 300;

	// display additional options on load
	$(".expandbttn").addClass("advancedoptionsshowing");
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
		var optionsHeight = $("#alloptions").height();
		
		$(".optionsandpreviewwrapper").stop().animate({
			height: optionsHeight
		}, timeToToggle);

		$("#preview").stop().animate({
			height: optionsHeight
		}, timeToToggle);
	}

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
	// var timeToToggle = 300;
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
	$(".expandbttn").click(function(){
		if (optionsDisplaying){
			$(".expandbttn").removeClass("advancedoptionsshowing");
			optionsDisplaying = false;
		} else {
			$(".expandbttn").addClass("advancedoptionsshowing");
			optionsDisplaying = true;
		}

		$(".advancedoptions").animate({
			height: "toggle"
		}, 500);
	});
});



$(function() {
	var timeToToggle = 100;
	$("#punctbox").click( function() {
		if ($(this).children('input').is(':checked')) {
			$("#aposhyph").fadeOut(timeToToggle);
		}
		else {
			$("#aposhyph").fadeIn(timeToToggle);
		}
	});
});