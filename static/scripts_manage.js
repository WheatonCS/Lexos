$(function() {
	$(".navbaroption").click(function() {
		$(this).next("input").click();
	});

	$(".filepreview").click(function() {
		// var inputToToggle = $(this).children('.filestatus');
		// // alert(inputToToggle.prop('disabled'));
		// inputToToggle.prop('disabled', !inputToToggle.prop('disabled'));
		// $(this).toggleClass('enabled');
		xhr = new XMLHttpRequest();
		ajaxRequestURL = document.getElementById("manage").action;
		xhr.open("POST", ajaxRequestURL, false);
		xhr.send($(this).prop('id'));
		
		$(this).toggleClass('enabled');
	});
});

function haveactivefiles() {
	xhr = new XMLHttpRequest();

	// Ajax gives the XMLHttpRequest
	ajaxRequestURL = document.getElementById("upload").action;

	xhr.open("POST", ajaxRequestURL, false);
	xhr.setRequestHeader('testforactive', '');
	xhr.send();

	if (xhr.responseText == 'False') {
		alert("You have no files enabled.");
		return false;
	}
}