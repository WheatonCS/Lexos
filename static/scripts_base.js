function haveactivefiles() {
	// Ajax gives the XMLHttpRequest
	var xhr = new XMLHttpRequest();

	xhr.open("POST", document.URL, false);
	xhr.setRequestHeader('testforactive', '');
	xhr.send();

	if (xhr.responseText == 'False') {
		alert("You have no files enabled.");
		return false;
	}
}

$("form").submit(function() {
	alert("boom1");
});