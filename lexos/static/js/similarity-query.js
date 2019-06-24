let table;
$(function(){

    // Display the loading overlay for the "Comparison Document" and
    // "Similarity Query" sections
    start_loading("#comparison-document-section-body, #table");

    // Initialize the legacy form inputs and create the similarity table
    get_active_file_ids(initialize,
        "#comparison-document-section-body, #table");

    // Initialize the table
    table = new Table("similarity", "similarity-query/results",
        "#table-section", "Similarity Query", validate_analyze_inputs,
        null, true, true, false, true, true);

    // If the "Download" button is pressed, download the CSV
    $("#download-button").click(function(){
        download(csv, "similarity-query.csv");
    });

    // Initialize the tooltips
    initialize_analyze_tooltips();
    initialize_tooltips();

    // Initialize the walkthrough
    initialize_walkthrough(walkthrough);
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
        add_text_overlay("#similarity-table-content", `This Tool Requires at
            Least Two Active Documents`);
        add_text_overlay("#comparison-document-section-body", '');
        return;
    }

    // Otherwise, initialize the legacy form inputs
    if(!initialize_legacy_inputs(response)) return;

    // Initialize the comparison document section
    initialize_comparison_document_section(
        Object.entries(parse_json(response)));

    // Create the similarity table
    table.create();
}


/**
 * Initializes the comparison document section.
 * @param {Object[]} documents: The documents to display as options.
 */
function initialize_comparison_document_section(documents){

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


/**
 * Initializes the walkthrough.
 */
function walkthrough(){

    let intro = introJs();
    intro.setOptions({steps: [
        {
            intro: `Welcome to Similarity Query!`,
            position: "top",
        },
        {
            element: "#comparison-document-section",
            intro: `By clicking "Select" you can choose which document is the
                baseline for comparison.`,
            position: "top",
        },
        {
            element: "#tokenize-section",
            intro: `Tokenize determines how terms are counted when generating
                data.`,
            position: "top",
        },
        {
            element: "#cull-section",
            intro: `Cull limits the number of terms used to generate data, and
                is optional.`,
            position: "top",
        },
        {
            element: "#sim-query-buttons",
            intro: `Here you can generate a new Similarity Query. You can also
                choose to download the current table as a CSV file.`,
            position: "top",
        },
        {
            intro: `This concludes the Similarity Query walkthrough!`,
            position: "top",
        }
    ]});

    intro.start();
}
