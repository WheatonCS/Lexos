let documents;

$(function(){

    // Remove the "Normalize" section and set its input to "raw"
    $(`input[name="normalizeType"][value="raw"]`).prop("checked", true);

    // Display the loading overlay on the "Class Divisions" and "Top Words"
    // sections
    start_loading("#class-divisions-body, #top-words-body");

    // Initialize legacy form inputs and create the "Top Words" section
    $.ajax({type: "GET", url: "/active-file-ids"}).done(initialize);
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
