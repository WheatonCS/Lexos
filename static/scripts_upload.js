$(function() {
	$("#uploadbrowse").click(function() {
		$("#fileselect").click();
	});

	function toggleFileUse() {

	}

	$(".filepreview").click(function() {
		var inputToToggle = $(this).children('.filestatus');
		// alert(inputToToggle.prop('disabled'));
		inputToToggle.prop('disabled', !inputToToggle.prop('disabled'));
		$(this).toggleClass('enabled');
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
		
		var xhr = new XMLHttpRequest();
		if (xhr.upload && (file.type == "text/plain" || file.type == "text/html" || file.type == "text/xml" || file.type == "text/sgml") && file.size <= $id("MAX_FILE_SIZE").value) {
			var uploadURL = $id("upload").action
			// start upload
			xhr.open("POST", uploadURL, false);
			xhr.setRequestHeader("X_FILENAME", file.name);
			xhr.send(file);

			if (xhr.responseText != 'failed') {
				filesUploaded = true;

				var templateClone = $($(".template").clone())
				templateClone
					.prop('class', 'filepreview enabled')
					.prop('id', file.name)
					.find('.filestatus').prop('name', file.name).end()
					.find('h6').html(file.name).end()
					.find('.textblock').html(xhr.responseText
						.replace(/>/g, '&gt;')
						.replace(/</g, '&lt;')
						.replace(/\n/g, '<br>')
						).end();
				templateClone.find('.filestatus').appendTo('form')
				templateClone.appendTo("#uploadpreviewdiv");

				$(".filepreview").click(function() {
					var inputToToggle = $(this).children('.filestatus');
					inputToToggle.prop('disabled', !inputToToggle.prop('disabled'));
					$(this).toggleClass('enabled');
				});
			}
		}

		if (!filesUploaded) {
			alert("Upload for " + file.name + " failed.");
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

function havefile() {
	xhr = new XMLHttpRequest();

	// Ajax gives the XMLHttpRequest
	ajaxRequestURL = document.getElementById("upload").action

	xhr.open("POST", ajaxRequestURL, false);
	xhr.setRequestHeader('testifuploaded', '');
	xhr.send();

	if (xhr.responseText == 'False') {
		alert("No files have yet been uploaded.");
		return false;
	}
}