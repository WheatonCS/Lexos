$(function() {

	$("#uploadbrowse").click(function() {
		$("#fileselect").click();
	});

	//------------------- FILEDRAG -----------------------------

	// getElementById
	function $id(id) {
		return document.getElementById(id);
	}

	// output information
	function Output(msg) {
		var m = $id("uploadpreviewdiv");
		m.innerHTML = msg + m.innerHTML;
	}

	// file drag hover
	function FileDragHover(e) {
		e.stopPropagation();
		e.preventDefault();
		e.target.className = (e.type == "dragover" ? "hover" : "");
	}

	// file selection
	function FileSelectHandler(e) {

		// cancel event and hover styling
		FileDragHover(e);

		// fetch FileList object
		var files = e.target.files || e.dataTransfer.files;

		// process all File objects
		for (var i = 0, f; f = files[i]; i++) {
			UploadAndParseFile(f);
		}
	}

	// upload and display file contents
	function UploadAndParseFile(file) {
		var filesUploaded = false;

		var filename = file.name.replace(/ /g, "_");
		
		var xhr = new XMLHttpRequest();
		if (xhr.upload && (file.type == "text/plain" || file.type == "text/html" || file.type == "text/xml" || file.type == "text/sgml") && file.size <= $id("MAX_FILE_SIZE").value) {
			// start upload
			xhr.open("POST", document.URL, false);
			xhr.setRequestHeader("X_FILENAME", filename);
			xhr.send(file);

			if (xhr.responseText == 'success') {
				filesUploaded = true;

				if (file.type.indexOf("text") == 0) {
					var reader = new FileReader();
					reader.onload = function(e) {
						// Detect whether the file has HTML or XML tags
						var pattern=new RegExp("<[^>]+>");
						var hasTags = pattern.test(e.target.result);
						// Update the checkTags and formmatingbox hidden inputs.
						// Show the strip tags form fields.
						if (hasTags == true) {
							$("#tags").val("on");
						}
						Output(
							"<div class=\"uploadedfilespreivewwrapper\"><strong>" +
							filename +
							":</strong><br><div class=\"uploadedfilespreivew\">" +
							e.target.result.replace(/</g, "&lt;")
										   .replace(/>/g, "&gt;")
										   .replace(/\n/g, "<br>") +
							"</div><br>File information: <strong>" +
							filename +
							"</strong> type: <strong>" +
							file.type +
							"</strong> size: <strong>" +
							file.size +
							"</strong> bytes</div>"
						);
					}
					reader.readAsText(file);
				}
			}
			else if (xhr.responseText == 'redundant_fail') {
				alert("Upload for " + filename + " failed.\nFile already exists on server.");
				return;
			}
			else {
				alert("Upload for " + filename + " failed.");
			}
		}
	}

	// initialize
	function Init() {

		var fileselect = $id("fileselect"),
			filedrag = $id("dragndrop"),
			submitbutton = $id("submitbutton");

		// file select
		fileselect.addEventListener("change", FileSelectHandler, false);

		// is XHR2 available?
		var xhr = new XMLHttpRequest();
		if (xhr.upload) {

			// file drop
			filedrag.addEventListener("dragover", FileDragHover, false);
			filedrag.addEventListener("dragleave", FileDragHover, false);
			filedrag.addEventListener("drop", FileSelectHandler, false);
		}
	}

	// call initialization file
	if (window.File && window.FileList && window.FileReader) {
		Init();
	}
});