let csv;
$(function(){

    // Display the loading overlay for the "Comparison Document" and
    // "Similarity Query" sections
    start_loading("#comparison-document-section-body, #table");

    // Initialize the "Comparison Document", "Tokenize", "Cull", and
    // "Similarity Query" sections
    initialize_analyze_tooltips();
    initialize_tooltips();

    // Initialize the legacy form inputs and create the similarity table
    get_active_file_ids(initialize,
        "#comparison-document-section-body, #table");

    // If the "Download" button is pressed, download the CSV
    $("#download-button").click(function(){
        download(csv, "similarity-query.csv");
    });
});


/**
 * Initialize the legacy form inputs and create the similarity table.
 * @param {string} response: The response from the "/active-file-ids" request.
 */
function initialize(response){

    // If there are fewer than two active documents, display warning text
    // and return
    document_count = Object.entries(parse_json(response)).length;
    if(document_count <  2){
        add_text_overlay("#table", `This Tool Requires at Least Two Active
            Documents`);
        add_text_overlay("#comparison-document-section-body", '');
        return;
    }

    // Initialize the legacy form inputs
    if(!initialize_legacy_inputs(response)) return;

    // Otherwise, parse the response
    let documents = Object.entries(parse_json(response));

    // Enable the "Comparison Document" section's "Select" button
    let select_button_element = $("#select-button");
    select_button_element.removeClass("disabled");

    // Set the comparison document to the first document
    let first_document = documents[0];
    $("#comparison-document-input").val(first_document[0]);

    $(`<h3 id="comparison-document-text" class="hidden"></h3>`)
        .appendTo("#comparison-document-section-body")
        .text(first_document[1]);

    // Remove the loading overlay from the "Comparison Document" section and
    // fade in the comparison document name
    finish_loading("#comparison-document-section-body",
        "#comparison-document-text");

    // Register the popup creation callback for the "Comparison Document"
    // section's "Select" button
    select_button_element.click(function(){
        create_radio_options_popup("Comparison Document",
            "comparison-document", "#comparison-document-text",
            "#comparison-document-input", documents
        );
    });

    // Create the similarity table
    send_similarity_table_request();

    // If the "Generate" button is pressed, recreate the similarity table
    $("#generate-button").click(function(){
        if(!validate_analyze_inputs()) return;
        start_loading("#table", "#generate-button, #download-button");
        remove_errors();
        send_similarity_table_request();
    });
}


/**
 * Sends a request for the similarity query data and creates the similarity
 *      query table.
 */
function send_similarity_table_request(){

    // Send a request for the similarity query data
    send_ajax_form_request("similarity-query/results")

        // If the request was successful, store the CSV result and create the
        // similarity query table
        .done(function(response){
            csv = response.csv;
            create_similarity_table(response.table);
        })

        // If the request failed, display an error and "Loading Failed" text
        // and enable the "Generate" button
        .fail(function(){
            error("Failed to retrieve the similarity query data.");
            add_text_overlay("#table", "Loading Failed");
            enable("#generate-button");
        });
}


/**
 * Creates the similarity query table.
 * @param {string} response: The "table" part of the response from the
 *      "similarity-query/results" request.
 */
function create_similarity_table(response){

    // Create the tables
    create_table("#table", parse_json(response),
        ["Document", "Cosine Similarity"]);

    // Remove the loading overlay, fade in the table, and enable the
    // "Generate" and "Download" buttons
    finish_loading("#table", ".lexos-table",
        "#generate-button, #download-button");
}


/**
 * Initializes the tooltips for the "Similarity Query" and
 *      "Comparison Document" sections.
 */
function initialize_tooltips(){

    // "Similarity Query"
    create_tooltip("#similarity-query-tooltip-button", `The rankings are
        determined by the distance between documents. Small distances
        (near zero) represent documents that are similar, and distances close
        to one represent documents that are different.`, true);

    // "Comparison Document"
    create_tooltip("#comparison-document-tooltip-button", `Select one document
        to be the external comparison. All other documents will be used to
        make the model and will be ranked in order of most to least similar
        to the comparison document in your results.`);
}
