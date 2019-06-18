$(function(){

    // Redirect "Browse..." button clicks to the file selection input element
    // which will open an OS file selection window
    $("#browse-button").click(function(){ $("#file-select-input").click(); });

    // When the user finishes selecting files using the OS file selection
    // window, upload the selected files
    $("#file-select-input").change(upload_files);

    // Upload files dropped on the drag and drop section
    const drag_and_drop_section = $("#drag-and-drop-section");
    drag_and_drop_section.on("drop", upload_files);

    // Prevent the default drag and drop action of opening the file in the
    // browser
    $("body").on("dragover dragenter drop", drag_and_drop_intercept);
    drag_and_drop_section.on("dragover dragenter", drag_and_drop_intercept);

    // If the "Scrape" button is pressed...
    $("#scrape-button").click(scrape);

    // Highlight the drag and drop section when files are dragged over it
    initialize_drag_and_drop_section_highlighting();
})


/**
 * Performs scraping on the given URLs.
 */
function scrape(){

    // Disable the "Scrape" button
    disable("#scrape-button");

    // Remove any existing errors
    remove_errors();

    // Send the scrape request
    send_ajax_request("/upload/scrape", $("#scrape-input").val())

    // Always enable the "Scrape" button
    .always(function(){ enable("#scrape-button"); })

    // If the request was successful, display the uploaded files in the
    // "Upload List" section.
    .done(function(response){
        for(const file_name of response) create_upload_preview(file_name);
    })

    // If the request failed, display an error.
    .fail(function(){
        error("Scraping failed.");
    });
}


/**
 * Uploads the files selected via the OS file selection window or drag and
 *      drop.
 * @param {event} event: The event that triggered the callback.
 */
let files = [];
function upload_files(event){

    // Remove any existing error messages
    remove_errors();

    // For each selected file...
    for(let file of Object.values(event.target.files ||
        event.originalEvent.dataTransfer.files)){

        // Validate the file
        if(!validate_file(file)) continue;

        // Replace the file name's spaces with underscores
        file.name = file.name.replace(/ /g, '_');

        // Create the upload preview and add the progress element to the file
        // element
        file["upload_preview_element"] = create_upload_preview(file.name);

        // Add the file to the upload list
        files.unshift(file);
    }

    // Upload each file
    send_file_upload_requests();
}


/**
 * Validates the given file.
 * @param file: The file to validate.
 * @returns {boolean}: Whether the file is valid.
 */
function validate_file(file){

    // If the file exceeds the 256 MB size limit, display an error message
    // and return false
    if(file.size > 256000000){
        error("One or more files exceeded the 256 MB size limit.");
        return false;
    }

    // If the file is empty, display an error message and return false
    if(file.size <= 0){
        error("One or more uploaded files were empty.");
        return false;
    }

    // If the file is not of a supported type, display an error message and
    // return false
    if(!file_type_supported(file.name)){
        error("One or more files were of an unsupported file type.");
        return false;
    }

    return true;
}


/**
 * Uploads the given file.
 */
function send_file_upload_requests(){

    // Get the next file
    let file = files.pop();
    if(!file) return;

    // Send a request to upload the file
    $.ajax({
        xhr: initialize_upload_progress_callback(file),
        type: "POST",
        url: "upload/add-document",
        data: file,
        processData: false,
        contentType: file.type,
        headers: {"file-name": encodeURIComponent(file.name)}
      })

        // If the request is successful, call the "upload_success_callback()"
        // function and upload the next file in the list
        .done(function(){ send_file_upload_requests(); })

        // If the request failed, display an error
        .fail(function(){
            error("One or more files encountered errors during upload.");
        });
}


/**
 * Initializes the XHR file upload progress callback.
 * @param file: The file whose upload preview will be updated.
 * @returns {function(): Window.XMLHttpRequest}: The XHR object.
 */
function initialize_upload_progress_callback(file){

    return function(){

        // Create the XHR object
        let xhr = $.ajaxSettings.xhr();

        // When upload progress has been made...
        xhr.upload.onprogress = function(event){

            // Update the file's upload preview with the file's upload
            // progress
            let progress = event.loaded/event.total;
            let progress_bar_element =
                file.upload_preview_element.find(".progress-bar")
                .css("width", `${progress*100}%`);

            // If the upload has completed, increase the upload preview's
            // opacity
            if(progress >= 1){
                progress_bar_element.css("opacity", "0");
                file.upload_preview_element.find(".upload-preview-content")
                    .removeClass("disabled");
            }
        };

        return xhr;
    };
}


/**
 * Checks if the file type is supported.
 * @param {string} filename: The name of the file to check.
 * @return {boolean} bool: Whether the file type is supported.
 */
function file_type_supported(filename){
    const supported_file_types = ["txt", "xml", "html", "sgml", "lexos"];

    // Get the file's extension
    let fileType = filename.split('.')[filename.split('.').length - 1];

    // Return whether the file type is supported
    return $.inArray(fileType, supported_file_types) > -1;
}


/**
 * Create an upload preview element.
 */
function create_upload_preview(file_name){

    // Remove the "No Uploads" text if it exists
    $("#no-uploads-text").remove();

    // Update the "Active Document Count" element
    let active_documents_element = $("#active-document-count");
    let active_documents = parseInt(active_documents_element.text())+1;
    active_documents_element.text(active_documents.toString());

    // Create the upload preview element
    let upload_preview_element = $(`
        <div id="preview-${active_documents}" class="hidden upload-preview">
            <h3 class="disabled upload-preview-content"></h3>
            <div class="progress-bar"></div>
        </div>
    `).appendTo("#upload-previews-grid");

    // Add the HTML-escaped file name to the upload preview element
    upload_preview_element.find(".upload-preview-content")
        .text(file_name);

    // Fade in the preview element
    fade_in(`#preview-${active_documents}`,".5s");

    // Return the upload preview element
    return upload_preview_element;
}


/**
 * Intercepts file drag and drop events, preventing the default action of
 * opening the dropped file in the browser.
 * @param {object} event: The event that triggered the callback.
 */
function drag_and_drop_intercept(event){
  event.stopPropagation();
  event.preventDefault();
}


/**
 * Makes the drag and drop section highlighted when files are dragged over it.
 */
function initialize_drag_and_drop_section_highlighting(){

    let drag_counter = 0;
    const drag_and_drop_section = $("#drag-and-drop-section");

    drag_and_drop_section.on("dragenter", function(){
        ++drag_counter;
        drag_and_drop_section.addClass("highlighted");
    });

    drag_and_drop_section.on("dragleave", function(){
        if(--drag_counter === 0)
            drag_and_drop_section.removeClass("highlighted");
    });

    drag_and_drop_section.on("drop", function(){
        drag_counter = 0;
        drag_and_drop_section.removeClass("highlighted");
    });
}
