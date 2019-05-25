/**
 * Creates a preview for each active document.
 *
 * @param {string} response: The response from the
 *     get-document-previews request.
 */
function initialize_document_previews(response){

    let previews = JSON.parse(response);

    // If there are no previews, display "No Previews" text
    if(!previews.length) display_no_previews_text();

    // Otherwise, create a preview for each active document
    for(const preview of previews) create_document_preview(preview[2], preview[3]);
}


/**
 * Creates a document preview with the given name and text.
 *
 * @param {string} preview_name: The name of the document.
 * @param {string} preview_text: The preview text.
 */
function create_document_preview(preview_name, preview_text){
    let preview = $(`
        <div class="preview">
            <h3 class="preview-name"></h3>
            <h3 class="preview-text"></h3>
        </div>
    `).appendTo("#previews");

    // HTML-escape
    preview.find(".preview-name").text(preview_name);
    preview.find(".preview-text").text(preview_text);
}

/**
 * Dispays "no previews" text.
 */
function display_no_previews_text(){
    $(`
        <div class="centerer">
            <h3>No Previews</h3>
        </div>
    `).appendTo("#previews");
}
