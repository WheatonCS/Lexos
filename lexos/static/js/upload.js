let total_files = 0;
let upload_count = 0;

/**
 * Checks if the file type is valid.
 * @return {boolean} bool - true if file type is valid.
 * @param {string} filename - The name of the file.
 */
function is_file_type_valid(filename){
    const allowed_file_types = ["txt", "xml", "html", "sgml", "lexos"];

    // Get the file file extension
    let fileType = filename.split('.')[filename.split('.').length - 1];

    // Return false if the file format is not in the list of allowed types
    return $.inArray(fileType, allowed_file_types) > -1;
}


/**
 * Uploads the given file.
 * @return {void}
 * @param {object} file - The file to upload.
 */
function upload_file(file){

    // Check if the file size is within limits
    if(file.size < $("#MAX_FILE_SIZE").value) return;

    // Replace the file name's spaces with underscores
    let file_name = file.name.replace(/ /g, '_');

    // Check if the file is of an invalid type
    if(!is_file_type_valid(file.name)){
        $("#error-modal-message").html(`The file `+
            `"${file_name}" is of an invalid type.`);
        $("#error-modal").modal();
        return;
    }

    // Check if the file is empty
    if(file.size === 0){
        $("#error-modal-message").html(`The file "${file_name}" is blank.`);
        $("#error-modal").modal();
        return;
    }

    // Upload the file
    send_ajax_request(file, file_name)
        .fail(function(jq_XHR, status, error)
            { alert(`${status}: ${error}`); })
        .done(function(){ upload_success_callback(file_name); });
}

/**
 * Called when a file has successfully uploaded.
 * @return {void}
 */
let uploaded_file_names = [];
function upload_success_callback(file_name)
{
    // Update the document count and status elements
    ++upload_count;

    let active_documents_element = $("#active-document-count");
    let active_documents = parseInt(active_documents_element.text())+1;
    active_documents_element.text(active_documents.toString());

    const status_element = $("#upload-status");
    status_element.text(`${upload_count} of ${total_files} uploaded`);

    // Update the uploaded documents list
    uploaded_file_names.push(file_name);

    let string = "";
    for(const file_name of uploaded_file_names) string += file_name+", ";
    string = string.substring(0, string.length-2);

    $("#upload-list").text(string);
}


/**
 * @return {ajax} The AJAX data.
 * @param {object} file - The file object.
 * @param {string} file_name - The name of the file.
 */
function send_ajax_request(file, file_name){
  return $.ajax({
    type: "POST",
    url: "upload/add-document",
    data: file,
    processData: false,
    async: false, /*Async results in errors*/
    contentType: file.type,
    headers: {"file-name": encodeURIComponent(file_name)}
  });
}


/**
 * Uploads the selected files.
 * @return {void}
 * @param {object} event - The event.
 */
function file_selection_handler(event){
    let files = event.target.files || event.originalEvent.dataTransfer.files;
    total_files = files.length;
    upload_count = 0;

    if(!files.length) return;
    $("#upload-status").text("0 of "+total_files);

    for(let file of files) upload_file(file);
}


/**
 * Intercepts the file drag and drop events.
 * @return {void}
 * @param {object} event - The event.
 */
function drag_and_drop_intercept(event){
  event.stopPropagation();
  event.preventDefault();
  event.target.className = (event.type === "dragover" ? "hover" : '');
}


/**
 * Initializes callbacks.
 * @return {void}
 */
$(function(){

    // Check for prerequisites
    if(!window.File || !window.FileList ||
        !window.FileReader || !new XMLHttpRequest()) return;

    // "Browse.." button input redirect
    $("#browse-button").click(function(){ $("#file-select-input").click(); });

    // File select input callback
    $("#file-select-input").change(file_selection_handler);

    // File drop section
    const drag_and_drop_section = $("#drag-and-drop-section");
    $("body").on("dragenter drop", drag_and_drop_intercept);
    drag_and_drop_section.on("dragover dragenter", drag_and_drop_intercept);
    drag_and_drop_section.on("drop", file_selection_handler);

    //File drop section highlighting
    let drag_counter = 0;
    drag_and_drop_section.on("dragenter", function(){
        ++drag_counter;
        $("#drag-and-drop-section").css({
            "color": "#FFFFFF", "background-color": "#FF6000"});
    });

    drag_and_drop_section.on("dragleave", function(){
        if(--drag_counter === 0) set_default_drop_section_colors();
    });

    drag_and_drop_section.on("drop", function(){
        drag_counter = 0;
        set_default_drop_section_colors();
    });
})


function set_default_drop_section_colors(){
    $("#drag-and-drop-section").css({
        "color": "#505050", "background-color": "#FFFFFF"});
}
