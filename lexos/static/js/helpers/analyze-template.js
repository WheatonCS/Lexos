function initialize_legacy_inputs(response){

    let documents = Object.entries($.parseJSON(response));
    let document_names_element = $("#document-names-section");

    // If there are no active documents, return
    if(!documents.length) return false;

     // Otherwise, initialize legacy file name and ID inputs
    let value = "";
    for(const document of documents){

        // Add the file ID
        value += document[0]+' ';

        // Create the document name element
        $(`<input type="hidden" name="file_${document[0]}"
            value="${document[1]}">`).appendTo(document_names_element);
    }

    // Set the file IDs element
    $("#active-file-ids").val(value);
    return true;
}
