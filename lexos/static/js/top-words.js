let documents;

$(function(){

    // Initialize analyze tooltips
    initialize_analyze_tooltips();

    // Remove the "Normalize" section and set its input to "raw"
    $(`input[name="normalizeType"][value="raw"]`).prop("checked", true);

    // Display the loading overlay on the "Class Divisions" and "Top Words"
    // sections
    start_loading("#class-divisions-body, #top-words-body");

    // Initialize legacy form inputs and create the "Top Words" section
    $.ajax({type: "GET", url: "/active-file-ids"}).done(initialize);

    create_tooltips();
});


/**
 * Initialize the legacy form inputs and create the class division and top
 *      words tables.
 * @param {string} response: The response from the "/active-file-ids" request.
 */
function initialize(response){

    documents = Object.values(parse_json(response));

    // Initialize the legacy form inputs. If there are no active documents,
    // display "No Active Documents" text and return
    if(!initialize_legacy_inputs(response)){
        add_text_overlay("#class-divisions-body, #top-words-body",
            "No Active Documents");
        return;
    }

    // Create the "Class Divisions" section
    $.ajax({type: "GET", url: "top-words/class-divisions"})
        .done(create_class_division_tables);

     // Create the "Top Words" section
    send_ajax_form_request("top-words/tables")
        .done(create_top_words_tables);

    // If the "Generate" button is pressed, recreate the "Top Words" section
    $("#generate-button").click(function(){
        if(!validate_analyze_inputs()) return;
        start_loading("#top-words-body", "#generate-button, #download-button");
        send_ajax_form_request("top-words/tables")
            .done(create_top_words_tables);
    });
}


function create_class_division_tables(response){

    // Create the class division table data
    let table_data = [];

    // For each class...
    for(const entry of Object.entries(parse_json(response))){

        // Push an object containing the class name and an empty array
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
    $(`<div id="class-divisions-grid" class="hidden"></div>`)
        .appendTo("#class-divisions-body");

    // Create the class divisions tables
    for(const table of table_data) create_table(table.name,
        "#class-divisions-grid", table.data);

    // Remove the loading overlay from the "Class Divisions" section and fade
    // in the tables
    finish_loading("#class-divisions-body", "#class-divisions-grid");
}


/**
 * Creates the top words tables.
 * @param {string} response: The response from the "top-words/table" request.
 */
function create_top_words_tables(response){

    // Create the table grid
    $(`<div id="top-words-grid" class="hidden"></div>`)
        .appendTo("#top-words-body");

    // Create the top words tables
    for(const table of response) create_table(
        table["title"], "#top-words-grid", table["result"]);

    // Remove the loading overlay from the "Top Words" section, fade in the
    // tables, and enable the "Generate" and "Download" buttons
    finish_loading("#top-words-body", "#top-words-grid",
        "#generate-button, #download-button");
}

function create_tooltips(){
    //Download Tooltip
    create_tooltip("#download-tooltip-button", 'Get Topwords only displays the top 30 results. Download if you wish to see the full result.');

    //Comparison Method
    create_tooltip("#comparison-method-tooltip-button", 'By default, topwords compares individual documents to the entire set of active documents. ' +
        'If you wish to compare individual documents to other classes, got to the Manage tool to edit class labels.');

    //Document to Corpus
    create_tooltip("#document-corpus-tooltip-button", 'Compare the proportion of each term in individual documents to their proportions in the whole collection.' +
        'Example: Find topwords for one chapter compared to the entire book.');

    //Document to Class
    create_tooltip("#document-class-tooltip-button", 'Compare the proportion of each term in a document within one class to their proportions in another class as ' +
        'a whole. Example: With two books (two classes), find topwords in any chapter (document) from one of the books compared to the entire other book (class).');

    //Class to Class
    create_tooltip("#class-class-tooltip-button", 'Compare the proportion of each term in one class to their proportions in another class. Example: ' +
        'Find topwords between two books (classes).');

    //Class Division
    create_tooltip("#class-division-tooltip-button", 'This indicates assigned classes and the documents contained in each class.');
}
