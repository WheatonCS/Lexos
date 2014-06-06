$(function() {
	$("#uploadbrowse").click(function() {
		$("#fileselect").click();
	});

	//------------------- FILEDRAG -----------------------------

	var allowedFileTypes = ['txt', 'xml', 'html', 'sgml'];

	// getElementById
	function $id(id) {
		return document.getElementById(id);
	}

	// // output information
	// function Output(msg) {
	// 	var m = $id("manage-previews");
	// 	m.innerHTML = msg + m.innerHTML;
	// }

	function AllowedFileType(filename) {
		var splitName = filename.split(".");
		var fileType = splitName[splitName.length-1];
		if ($.inArray(fileType, allowedFileTypes) > -1) {
			return true;
		}
		else {
			return false;
		}
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
		var filename = file.name.replace(/ /g, "_");

		if (AllowedFileType(file.name) && file.size <= $id("MAX_FILE_SIZE").value) {
			
			// ajax call to upload files
			$.ajax({
				type: 'POST',
				url: document.URL,
				data: file,
				processData: false,
				async: false,
				contentType: file.type,
				headers: { 'X_FILENAME': encodeURIComponent(filename) },
				xhr: function() {
					console.log("Setting stuff");
					var xhr = new window.XMLHttpRequest();
					//Upload progress
					xhr.upload.addEventListener("progress", function(evt){
						if (evt.lengthComputable) {
							var percentComplete = evt.loaded / evt.total;
							//Do something with upload progress
							console.log(percentComplete);
						}
					}, false);

					return xhr;
				},
				success: function(res){
					var reader = new FileReader();
					reader.onload = function(e) {
						var template = $($('#file-preview-template').html());
						var contents = e.target.result.replace(/</g, "&lt;")
													.replace(/>/g, "&gt;");

						template.find('.uploaded-file-preview').html(contents);

						template.find('.file-label').html(filename);
						template.find('.file-information').find('.file-type').html(file.type);
						template.find('.file-information').find('.file-size').html(file.size);

						$('#manage-previews').prepend(template);
					}
					reader.readAsText(file);
				},
				error: function(jqXHR, textStatus, errorThrown){
					alert(textStatus + ": " + errorThrown);
				}
			});
		}

		else if (!AllowedFileType(file.name)) {
			alert("Upload for " + filename + " failed.\n\nInvalid file type.");
		}
		else {
			alert("Upload for " + filename + " failed.");
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

	// call initialization function
	if (window.File && window.FileList && window.FileReader) {
		Init();
	}
});