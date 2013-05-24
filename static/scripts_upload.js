function havefile() {
	xhr = new XMLHttpRequest();

	// Ajax gives the XMLHttpRequest
	ajaxRequestURL = document.getElementById("upload").action.split("/").slice(0,-1).join("/") + "/ajaxrequest";

	xhr.open("GET", ajaxRequestURL, false);
	xhr.send();

	if (xhr.responseText == 'False') {
		alert("No files uploaded yet");
		return false;
	}
}