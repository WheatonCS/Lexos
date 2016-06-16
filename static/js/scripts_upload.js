

$(function() {
	

  	$('[data-toggle="tooltip"]').tooltip();

	$("#uploadbrowse").click(function() {
		$("#fileselect").click();
		//$.get( "/detectActiveDocsbyAjax", function(response) {
      //console.log("Number of Active Documents: "+parseInt(response));
    //});

	});

	//------------------- FILEDRAG -----------------------------

	var allowedFileTypes = ['txt', 'xml', 'html', 'sgml', 'lexos'];
	

	function $id(id) {
		return document.getElementById(id);
	}

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
var numberOfFileDone=parseInt($('.fa-folder-open-o')[0].id);



	// file selection
	function FileSelectHandler(e) {

		// cancel event and hover styling
		FileDragHover(e);

		// fetch FileList object
		var files = e.target.files || e.dataTransfer.files;

		var totalFiles = files.length;

		// Make process bar back to 0
		$("#progress-bar").html("").css({"width": "0px"});
	

		$("#progress-bar").show();
		// process all File objects

		for (var i = 0, f; f = files[i]; i++) {
				var added=0;

			if (f.size< $id("MAX_FILE_SIZE").value){
				numberOfFileDone+=1;
				 added=1;
			}

			
			UploadAndParseFile(f);
			
			//loading progress bar
			if (f.type ==''){
				$("#progress").html("Loading Workspace");}
			else{
				var calculatedWidth=String(180*numberOfFileDone/totalFiles)+"px";
				$("#progress").html(numberOfFileDone+" of "+totalFiles).css("color", "#3498DB");
				$("#progress-bar").css({"width": calculatedWidth});		
				if (numberOfFileDone/totalFiles>0.5){
					$("#progress").css("color","#FFF");
				}
				if (added==1){
					$("#progress-bar").html("Complete!").css({"color":"#FFF", "text-align":"center", "width":"175px","height":"20px"} ).fadeOut(2000);
					$('.fa-folder-open-o')[0].dataset.originalTitle="You have "+ numberOfFileDone+ " active document(s)";
					$(".fa-folder-open-o").fadeIn(200);



				}
			}
		}
		
		$("#progress").html("Ready For Files To Upload").css("color","#074178").delay(3000).show();
	}

	// upload and display file contents
	function UploadAndParseFile(file) {

		var filename = file.name.replace(/ /g, "_");
		/*var x = $id("MAX_FILE_SIZE").value;
		alert("MAX_FILE_SIZE" + file.size);*/


		if (AllowedFileType(file.name) && file.size <= $id("MAX_FILE_SIZE").value) {

			
			if (file.size == 0){
				alert("Cannot process blank file -- " + file.name);

			}
			else {
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
						
						var xhr = new window.XMLHttpRequest();
						//Upload progress
						xhr.upload.addEventListener("progress", function(evt){
							if (evt.lengthComputable) {
								var percentComplete = evt.loaded / evt.total;
							//Do something with upload progress
								// console.log(percentComplete+'%');
							}
						}, false);

						return xhr;
					},
					success: function(res){
						var reader = new FileReader();
						reader.onload = function(e) {
							var template = $($('#file-preview-template').html());
							

							// template.find('.uploaded-file-preview').html(contents);

							template.find('.file-name').html(filename);
							var file_type='';
							if (file.type == ''){
								file_type = "Lexos Workspace";
								template.find('.file-information').find('.file-type').html(file_type);
							}
							else{
								template.find('.file-information').find('.file-type').html(file.type);
								var contents = e.target.result.replace(/</g, "&lt;")
													.replace(/>/g, "&gt;");

							}
							var file_size = file.size;
							if (file.size < 1024){
								template.find('.file-information').find('.file-size').html(file.size+"bytes");
							}
							else if (file.size < 1048576){
								file_size = (file.size/1024).toFixed(1);
								template.find('.file-information').find('.file-size').html(file_size+"KB");
							}
							else{
								file_size = (file.size/1024/1024).toFixed(1);
								template.find('.file-information').find('.file-size').html(file_size+"MB");
							}
						
							$('#manage-previews').prepend(template);
						}
						reader.readAsText(file);
					},
					complete: function(){
						$("#activeDocIcon").css("display","block");
					},
					error: function(jqXHR, textStatus, errorThrown){
						alert(textStatus + ": " + errorThrown);
					}
				});
			}
		}

		else if (!AllowedFileType(file.name)) {
			alert("Upload for " + filename + " failed.\n\nInvalid file type.");
		}
		else {


			alert("Upload for " + filename + " failed.\n\nFile bigger than " + MAX_FILE_SIZE_INT.value + " " + MAX_FILE_SIZE_UNITS.title + "B.");
		}
	}

	// initialize
	function Init() {

		var fileselect = $id("fileselect"),
			filedrag = $id("dragndrop"),
			submitbutton = $id("submitbutton");
		//console.log('babababababa');

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