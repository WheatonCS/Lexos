let documents;
let csv;
$(function(){

    // Add the loading overlays
    start_loading("#class-divisions-body, #top-words-body");

    // Initialize the tooltips in the "Comparison Method", "Tokenize",
    // "Cull", "Class Divisions", and "Top Words" sections
    initialize_analyze_tooltips();
    initialize_tooltips();

    // Set the normalize option to raw counts
    $(`input[name="normalizeType"][value="raw"]`).prop("checked", true);

    // Initialize the legacy form inputs, create the class division tables,
    // and create the top words tables
    get_active_file_ids(initialize, "#class-divisions-body, #top-words-body");

    // If the "Download" button is pressed, download the CSV
    $("#download-button").click(function(){ download(csv, "top-words.csv"); });
});


/**
 * Initializes the legacy form inputs, creates the class division tables,
 *      and creates the top words tables.
 * @param {string} response: The response from the "active-file-ids" request.
 */
function initialize(response){

    documents = parse_json(response);

    // If there are fewer than two active documents, display warning text
    // and return
    document_count = Object.entries(parse_json(response)).length;
    if(document_count <  2){
        add_text_overlay("#class-divisions-body, #top-words-body", `This Tool
            Requires at Least Two Active Documents`);
        return;
    }

    // Otherwise, display "No Results" text on the "Top Words" section and
    // enable the "Generate" button
    add_text_overlay("#top-words-body", "No Results");
    enable("#generate-button");

    // Initialize the legacy form inputs
    initialize_legacy_inputs(response);

    // Send a request to get the class divisions
    $.ajax({type: "GET", url: "top-words/class-divisions"})

        // If the request was successful...
        .done(function(response){

            // Create the class division tables
            create_class_division_tables(response);

            // If the "Generate" button is pressed, create the "Top Words" section
            $("#generate-button").click(function(){
                start_loading("#top-words-body", "#generate-button, #download-button");
                remove_errors();
                send_top_words_request();
            });
        })

        // If the request failed, display an error and "Loading Failed" text
        .fail(function(){
            error("Failed to retrieve the class divisions.");
            add_text_overlay("#class-divisions-body, #top-words-body",
                "Loading Failed");
        });
}


/**
 * Creates the class division tables.
 * @param {string} response: The response from the
 *      "top-words/class-divisions" request.
 */
let single_class = false;
function create_class_division_tables(response){

    // Create the class division table data
    let table_data = [];

    // For each class...
    let classes = Object.entries(parse_json(response));
    single_class = classes.length <= 1;
    for(const entry of classes){

        // Push an object containing the class name and an empty data array
        let class_name = entry[0];
        table_data.push({name: class_name, data: []});

        // For each document ID in the class...
        for(const document_id of Object.entries(entry[1])){

            // If the ID is in the class, add it to the array
            if(document_id[1]) table_data[table_data.length-1].data
                .push([documents[parseInt(document_id[0])]]);
        }
    }

    // Create the class divisions grid
    $(`<div id="class-divisions-grid"></div>`)
        .appendTo("#class-divisions-body");

    // Create the class divisions tables
    for(const table of table_data) create_table(
        "#class-divisions-grid", table.data, '', table.name);

    // Remove the loading overlay from the "Class Divisions" section and fade
    // in the tables
    finish_loading("#class-divisions-body",
        "#class-divisions-grid .lexos-table");
}


/**
 * Sends a request for the top words data and creates the top words tables.
 */
function send_top_words_request(){

    // If the inputs are invalid, remove the loading overlay, enable the
    // buttons, and return
    if(!validate_inputs() || !validate_analyze_inputs()){
        top_words_loading_failure();
        return;
    }

    // Otherwise, send a request for the top words results
    send_ajax_form_request("top-words/results")

        // If the request was successful, create the top words tables and
        // store the CSV result
        .done(function(response){
            csv = response.csv;
            create_top_words_tables(response.tables);
        })

        // If the request failed, display an error, remove the loading overlay,
        // and enable the buttons
        .fail(function(){
            top_words_loading_failure();
            error("Failed to retrieve the top words data.");
        });
}


/**
 * Creates the top words tables.
 * @param {string} tables: The "tables" portion of the response from the
 *      "top-words/get-results" request.
 */
function create_top_words_tables(tables){

    // Create the table grid
    $(`<div id="top-words-grid"></div>`).appendTo("#top-words-body");

    // Create the top words tables
    for(const table of tables) create_table("#top-words-grid",
        table["result"], '', table["title"]);

    // Remove the loading overlay, fade in the tables, and enable the buttons
    finish_loading("#top-words-body", "#top-words-grid .lexos-table",
        "#generate-button, #download-button");
}


/**
 * Validates the inputs in the "Comparison Method" section.
 * @return {boolean}: Whether the inputs are valid.
 */
function validate_inputs(){
    let comparison_method = $(`input[name="testInput"]:checked`).val();

    if((comparison_method === "classToPara" ||
        comparison_method === "classToClass") && single_class){
        error("Invalid comparison method.");
        return false;
    }

    return true;
}


/**
 * Remove the loading overlay and enable the buttons on the "Top Words"
 *      section.
 */
function top_words_loading_failure(){

    // Remove the loading overlay and enable the "Generate" button
    finish_loading("#top-words-body", "", "#generate-button");

    // Display "Loading Failed" text
    add_text_overlay("#top-words-body", "Loading Failed");
}


/**
 * Initialize the tooltips for the "Comparison Method", "Class Divisions",
 * and "Top Words" sections.
 */
function initialize_tooltips(){

    // "Comparison Method"
    create_tooltip("#comparison-method-tooltip-button", `By default, topwords
    compares individual documents to the entire set of active documents. If
    you wish to compare individual documents to other classes, go to the
    Manage tool to edit class labels.`);

    // "Each document to the corpus"
    create_tooltip("#document-corpus-tooltip-button", `Compare the proportion
        of each term in individual documents to their proportions in the whole
        collection. Example: Find topwords for one chapter compared to the
        entire book.`);

    // "Each document to other classes"
    create_tooltip("#document-class-tooltip-button", `Compare the proportion
        of each term in a document within one class to their proportions in
        another class as a whole. Example: With two books (two classes),
        find topwords in any chapter (document) from one of the books
        compared to the entire other book (class).`);

    // "Each class to other classes"
    create_tooltip("#class-class-tooltip-button", `Compare the proportion of
        each term in one class to their proportions in another class.
        Example: Find topwords between two books (classes).`);

    // "Class Divisions"
    create_tooltip("#class-division-tooltip-button", `This indicates assigned
        classes and the documents contained in each class.`, true);

    // "Top Words"
    create_tooltip("#download-tooltip-button", `Get Topwords only displays the
        top 30 results. Download if you wish to see the full result.`, true);

}
