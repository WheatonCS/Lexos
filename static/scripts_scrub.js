$(function() {
	var timeToToggle = 500;
	$("#stopwords").click( function() {
		$("#box-stopwords").slideToggle(timeToToggle);
	});
	$("#lemmas").click( function () {
		$("#box-lemmas").slideToggle(timeToToggle);
	});
	$("#consolidations").click( function() {
		$("#box-consolidations").slideToggle(timeToToggle);
	});
	$("#specialchars").click( function() {
		$("#box-specialchars").slideToggle(timeToToggle);
	});
	$("#alloptuploadstoggle").click( function() {
		var numOpen = 0;
		if ($("#box-stopwords").is(":visible")) { numOpen++; }
		if ($("#box-lemmas").is(":visible")) { numOpen++; }
		if ($("#box-consolidations").is(":visible")) { numOpen++; }
		if ($("#box-specialchars").is(":visible")) { numOpen++; }

		if (numOpen < 3) {
			$("#box-stopwords").slideDown(timeToToggle);
			$("#box-lemmas").slideDown(timeToToggle);
			$("#box-consolidations").slideDown(timeToToggle);
			$("#box-specialchars").slideDown(timeToToggle);
		}
		else {
			$("#box-stopwords").slideUp(timeToToggle);
			$("#box-lemmas").slideUp(timeToToggle);
			$("#box-consolidations").slideUp(timeToToggle);
			$("#box-specialchars").slideUp(timeToToggle);
		}
	});
});

$(function() {
	var timeToToggle = 100;
	$("#punctbox").click( function() {
		$("#apos").fadeToggle(timeToToggle);
		$("#hyph").fadeToggle(timeToToggle);
	});
});

$(function() {
	$(document).tooltip({
		position:{
			relative: true,
			at: "center top-5", // location on the mouse
								// Negative horizontal is left, negative vertical is up 
			my: "center bottom",// location on the tooltip popup window
			collision: "fit"
		}

	});
});

function supports_html5_storage() {
	try {
		return 'localStorage' in window && window['localStorage'] !== null;
	} catch(e) {
		return false;
	}
}

function readshowstore_preview() {
	var XHRequest = new XMLHttpRequest();

	var filenames = document.getElementById('session_file_name').value;

}