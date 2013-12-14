function havefiles() {
	var xhr = new XMLHttpRequest();

	var testURL = document.URL.split('/').slice(0, -1).join('/') + '/filesactive';

	xhr.open("GET", testURL, false);
	xhr.setRequestHeader('testforactive', '');
	xhr.send();
	if (xhr.responseText == 'True') {
		return true;
	}
	else {
		return false;
	}
}

/* append the span for the error message */
$(function() {
	var errormessage1 = "Submission Failed! No active text.";
	$("#basesubmitdiv").append('<span class="submiterrors" id="submiterrormessage1">' + errormessage1 + '</span>');
});

$(function() {
	$("form").submit(function() {
		if (!havefiles()) {
			$("#submiterrormessage1").show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
	});
});