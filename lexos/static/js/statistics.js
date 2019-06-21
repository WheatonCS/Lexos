$(function(){

    // If the walkthrough button is clicked, start the walkthrough
    walkthrough_button_callback = walkthrough;

    // Display the loading overlays
    start_loading("#graph-container, #table, #corpus-statistics, "+
        "#standard-error-test, #interquartile-range-test");

    // Initialize the tooltips
    initialize_tooltips();

    // Initialize the legacy form inputs and create the statistics
    get_active_file_ids(initialize, "#graph-container, #table, "+
        "#corpus-statistics, #standard-error-test, #interquartile-range-test");
});


/**
 * Initializes the legacy form inputs and creates the statistics.
 * @param {string} response: The response from the "active-file-ids" request.
 */
let document_statistics_csv;
function initialize(response){

    // Initialize the legacy form inputs. If there are no active documents,
    // display "No Active Documents" text and return
    if(!initialize_legacy_inputs(response)){
        add_text_overlay("#graph-container, #table, #corpus-statistics, "+
            "#standard-error-test, #interquartile-range-test",
            "No Active Documents");
        return;
    }

    // Create the statistics
    create_statistics();

    // If the "Generate" button is pressed, recreate the statistics
    $("#generate-button").click(function(){

        // Validate the inputs
        if(!validate_analyze_inputs()) return;

        // Remove any existing Plotly graphs
        remove_graphs();

        // Remove any existing error messages
        remove_errors();

        // Display the loading overlays and disable the appropriate buttons
        start_loading("#graph-container, #table, #corpus-statistics, "+
            "#standard-error-test, #interquartile-range-test",
            "#generate-button, #download-button, #png-button, #svg-button");

        // Create the statistics
        create_statistics();
    });

    // If the "Download" button is pressed, download the document statistics
    // CSV
    $("#download-button").click(function(){
        download(document_statistics_csv, "document-statistics.csv");
    });

    // If the "PNG" or "SVG" buttons are pressed, download the graph
    initialize_graph_download_buttons();
}


/**
 * Creates the statistics.
 */
function create_statistics(){

    // Send a request to get the corpus statistics
    send_ajax_form_request("/statistics/corpus")

         // If the request was successful, create the corpus statistics
        .done(create_corpus_statistics)

        // If the request failed, display an error and "Loading Failed" text
        .fail(function(){
            error("Failed to retrieve the corpus statistics.");
            add_text_overlay("#corpus-statistics, #standard-error-test, "+
                "#interquartile-range-test", "Loading Failed");
            loading_complete_check(3);
        });

    // Send a request to get the document statistics
    send_ajax_form_request("/statistics/document-statistics")

        // Always check if the loading has completed
        .always(function(){ loading_complete_check(); })

        // If the request was successful, store the CSV data and create the
        // table
        .done(create_document_statistics_table)

        // If the request failed, display an error and "Loading Failed" text
        .fail(function(){
            error("Failed to retrieve the document statistics.");
            add_text_overlay("#table", "Loading Failed");
        });

    // Create the box plot graph and enable the "Generate" button if all
    // sections have finished loading
    create_graph("/statistics/box-plot", function(){ loading_complete_check(); });
}


/**
 * Create the "Document Statistics" table.
 * @param {string} response: The response from the
 */
function create_document_statistics_table(response){

        document_statistics_csv = response.csv;

        // Create the table
        let sort_column_input = $(`input[name="sort-column"]`);
        create_table("#table", JSON.parse(response.table), ["Name",
            "Single-Occurrence Terms", "Total Terms", "Vocabulary Density",
            "Distinct Terms"], "", function(selected_head_cell_id){
                sort_column_input.val(selected_head_cell_id);
            }, sort_column_input.val());

        // Remove the loading overlay, fade the table in, and enable the
        // "Download" button
        finish_loading("#table", ".lexos-table", "#download-button");
}


/**
 * Creates the statistics for the "Corpus Statistics", "Standard Error Test",
 *      and "Interquartile Range Test" sections.
 * @param {string} response: The response from the "/statistics/corpus"
 *      request.
 */
function create_corpus_statistics(response){

    response = parse_json(response);

    // Populate the corpus statistics section with data
    $(`
        <h3>Average: ${response.average}</h3><br>
        <h3>Standard Deviation: ${response["standard_deviation"]}</h3><br>
        <h3>Interquartile Range: ${response["interquartile_range"]}</h3>
    `).appendTo("#corpus-statistics");

    // Populate the "Standard Error Test" section with data
    create_anomalies("#standard-error-test",
        response["standard_error_small"],
        response["standard_error_large"]);

    // Populate the "Interquartile Range Test" section with data
    create_anomalies("#interquartile-range-test",
        response["interquartile_range_small"],
        response["interquartile_range_large"]);

    // Remove the loading overlays sections and fade the data in
    finish_loading("#corpus-statistics, #standard-error-test, "+
        "#interquartile-range-test", "#corpus-statistics, "+
        "#standard-error-test, #interquartile-range-test");

    // Enable the "Generate" button if all elements have finished loading
    loading_complete_check(3);
}


/**
 * Populates the "Standard Error Test" or "Interquartile Range Test" sections
 *      with their data.
 * @param {string} element_id: The id of the section element to populate
 *      ("standard-error" or "interquartile-range").
 * @param {string[]} small_anomalies: The small anomalies.
 * @param {string[]} large_anomalies: The large anomalies.
 */
function create_anomalies(element_id, small_anomalies, large_anomalies){

    // Create a string stating the anomalies
    let text;
    if(!small_anomalies.length && !large_anomalies.length) text = "No Anomalies";
    else {
        text = "Anomalies: ";
        for(const anomaly of small_anomalies) text += anomaly+" (small), ";
        for(const anomaly of large_anomalies) text += anomaly+" (large), ";
        text = text.slice(0, -2);
    }

    // Add the string to the appropriate element
    $(`<h3>${text}</h3>`).appendTo(element_id);
}


/**
 * Re-enables the "Generate" button if all elements have finished loading.
 * @param {number} number_loaded: The number of elements that were loaded by
 *      the calling function.
 */
let elements_loaded = 0;
function loading_complete_check(number_loaded = 1){

    // Increment "elements_loaded" by the number of elements loaded by the
    // calling function
    elements_loaded += number_loaded;

    // If all 5 elements have not finished loading, return
    if(elements_loaded < 5) return;

    // Otherwise, re-enable the "Generate" button and reset "elements_loaded"
    $("#generate-button").removeClass("disabled");
    elements_loaded = 0;
}


/**
 * Initializes the tooltips for the "Tokenize" and "Cull" sections.
 */
function initialize_tooltips(){

    // "Tokenize"
    create_tooltip("#tokenize-tooltip-button", `Divide the text into n-grams
        (by tokens or characters) of the desired length.`);

    // "Cull"
    initialize_cull_tooltips(false);
}


/**
 * Initiates a walkthrough of the page.
 */
function walkthrough(){

    let intro = introJs();
    intro.setOptions({
        steps: [
            {
                element: '#left-column',
                intro: 'These are the settings for statistics. Tokenize and Cull can be used to control how data is compared. ' +
                    'Generate is here if you wish to change these settings.',
                position: 'top',
            },
            {
                element: '#graph-section',
                intro: 'Here the document sizes are graphed. This graph can be downloaded as a static PNG or vector SVG.',
                position: 'top',
            },
            {
                element: '#right-column',
                intro: 'Here are the overall statistics for your documents, used by the tool to determine outliers.',
                position: 'top',
            },
            {
                element: '#documents-section',
                intro: 'This table displays information concerning term usage across your documents. This table can be downloaded as a CSV file.',
                position: 'top',
            },
            {
                element: '#help-button',
                intro: 'For a more advanced summary of the Statistics features, check out the Help section.',
                position: 'bottom'
            }
        ]
    })

    intro.start();
}
