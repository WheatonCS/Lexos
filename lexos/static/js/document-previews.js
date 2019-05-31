/**
 * Creates a preview for each active document.
 *
 * @param {string} response: The response from the
 *     get-document-previews request.
 */
function initialize_document_previews(response){

    let previews = JSON.parse(response);

    // If there are no previews, display "No Previews" text
    if(!previews.length){
        add_text_overlay("#previews", "No Previews");
        return;
    }

    // Create a preview for each active document
    for(const preview of previews)
        create_document_preview(preview[2], preview[3]);
}


/**
 * Creates a document preview with the given name and text.
 *
 * @param {string} preview_name: The name of the document.
 * @param {string} preview_text: The preview text.
 */
function create_document_preview(preview_name, preview_text){

    // Create the document preview
    let preview = $(`
        <div class="preview hidden">
            <h3 class="preview-name"></h3>
            <h3 class="preview-text"></h3>
        </div>
    `).appendTo("#previews");

    // HTML-escape the text and add it to the document preview
    preview.find(".preview-name").text(preview_name);
    preview.find(".preview-text").text(preview_text);
}
