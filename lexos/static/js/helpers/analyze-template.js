/**
 * Initializes the legacy form inputs.
 * @param {string} response: The response from the "/get-active-documents"
 *      request.
 * @returns {boolean}: Whether there is at least one active document.
 */
function initialize_legacy_inputs(response){

    let documents = Object.entries(parse_json(response));
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


/**
 * Validates the inputs on the "Tokenize" and "Cull" sections.
 * @return {boolean}: Whether the inputs are valid.
 */
function validate_analyze_inputs(){

    // "Tokenize" - "Grams"
    let grams = $("#grams-input").val();
    if(!validate_number(grams, 1)){
        error("Invalid gram size.");
        return false;
    }

    // "Cull" - "Use the top X terms"
    let most_frequent_words = $("#most-frequent-words-input").val();
    if($("#most-frequent-words-checkbox").is(":checked") &&
        !validate_number(most_frequent_words, 1)){
        error("Invalid number of top terms.");
        return false;
    }

    // "Cull" - "Must be in X documents"
    let minimum_documents = $("#minimum-occurrences-input").val();
    if($("#minimum-occurrences-checkbox").is(":checked") &&
        !validate_number(minimum_documents, 1, active_document_count)){
        error("Invalid number of minimum occurrences.");
        return false;
    }

    return true;
}
