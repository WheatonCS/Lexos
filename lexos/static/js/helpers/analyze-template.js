/**
 *  Initialize the "Tokenize", "Normalize", and "Cull" tooltips.
 */
function initialize_analyze_tooltips(){

    // "Tokenize"
    create_tooltip("#tokenize-tooltip-button", `Divide the text into n-grams
        (by tokens or characters) of the desired length.`);

    // "Normalize"
    create_tooltip("#normalize-tooltip-button", `Set how terms are counted.
        Terms can be counted by raw (absolute) counts, by proportional
        frequencies (to account for document length), or by TF-IDF weighted
        counts.`);

    // "TF-IDF"
    create_tooltip("#tf-idf-tooltip-button", `Normalize the data for different
        document lengths using <a href="https://en.wikipedia.org/wiki/Tf%E2%80%93idf"
        target="_blank">Term Frequency-Inverse Document Frequency</a>.
        Selecting TF-IDF allows you to choose the distance metric according to
        which each document vector is normalized. Lexos uses base e (natural
        log) as the default.`);

    initialize_cull_tooltips();
}


/**
 * Initializes the tooltips for the "Cull" section
 * @param {boolean} on_right_edge: Whether the "Cull" section is on the right
 *      edge.
 */
function initialize_cull_tooltips(on_right_edge = true){

    // "Cull"
    create_tooltip("#cull-tooltip-button", `Place statistical bounds on the
        terms in the document-term matrix.`, on_right_edge);

    // "Use the top X Words"
    create_tooltip("#most-frequent-words-tooltip-button", `Use only the most
        frequently occurring terms in the document-term matrix.`, on_right_edge)

    // "Must be in X documents"
    create_tooltip("#minimum-occurrences-tooltip-button", `Set the minimum
        number of documents in which terms must occur to be included in the
        document-term matrix.`, on_right_edge);
}


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
