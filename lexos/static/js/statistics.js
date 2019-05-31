$(function(){

    // Send a request to get the active files and their IDs
    $.ajax({type: "GET", url: "/active-file-ids"})

    // If the request is successful, initialize the page
        .done(initialize);
});

/**
 * Initializes the statistics page.
 * @param {string} response: The response from the "/active-file-ids" request.
 */
function initialize(response){

    // Initialize legacy inputs
    if(!initialize_legacy_inputs(response)) return;

    // Add a loading overlay to the various elements that are loading data
    start_loading("#table, #corpus-statistics, "+
        "#standard-error-test, #interquartile-range-test");

    // Send a request to get the corpus statistics
    send_ajax_form_request("/statistics/corpus")

         // If the request is successful, create the corpus statistics
        .done(create_corpus_statistics);

    // Send a request to get the document statistics
    send_ajax_form_request("/statistics/documents")

        // If the request is successful, create the document statistics
        .done(create_document_statistics);

    // Create the box plot graph for the "Document Sizes" section
    create_graph("/statistics/box-plot");
}


function create_corpus_statistics(response){

    // Parse the JSON response, replacing any "NaN" values with "N/A"
    response = JSON.parse(response.replace(/\bNaN\b/g, "\"N/A\""));

    // Set the corpus statistics section data
    $(`
        <h3>Average: ${response.average}</h3><br>
        <h3>Standard Deviation: ${response.standard_deviation}</h3><br>
        <h3>Interquartile Range: ${response.interquartile_range}</h3>
    `).appendTo("#corpus-statistics");

    // Set the standard error test data
    set_anomalies("standard-error", response.standard_error_small,
        response.standard_error_large);

    // Set the interquartile range test data
    set_anomalies("interquartile-range", response.interquartile_range_small,
        response.interquartile_range_large);

    // Remove the loading overlays and fade the elements in
    finish_loading("#corpus-statistics, #standard-error-test, "+
        "#interquartile-range-test", "#corpus-statistics, "+
        "#standard-error-test, #interquartile-range-test");
}


function set_anomalies(name, small, large){

    // Create a string stating the anomalies
    let text;
    if(!small.length && !large.length) text = "No Anomalies";
    else {
        text = "Anomalies: ";
        for(const anomaly of small) text += anomaly+" (small), ";
        for(const anomaly of large) text += anomaly+" (large), ";
        text = text.slice(0, -2);
    }

    // Add the string to the appropriate element and fade it in
    $(`<h3>${text}</h3>`).appendTo(`#${name}-test`);
}


function create_document_statistics(response){

    // Append the head and table body
    $(`
        <div id="table-head" class="hidden">
            <h3 class="table-head-cell">Name</h3>
            <h3 class="table-head-cell">Total Terms</h3>
            <h3 class="table-head-cell">Distinct Terms</h3>
            <h3 class="table-head-cell">Average Terms</h3>
            <h3 class="table-head-cell">Single-Occurrence Terms</h3>
        </div>
        <div id="table-body" class="hidden"></div>
    `).appendTo("#table");

    // Append the rows
    let rows = Object.entries(JSON.parse(response));
    for(row of rows){
        let data = Object.values(row[1]);

        $(`
            <div class="table-row">
                <h3 class="table-cell">${data[0]}</h3>
                <h3 class="table-cell">${data[1]}</h3>
                <h3 class="table-cell">${data[2]}</h3>
                <h3 class="table-cell">${data[3]}</h3>
                <h3 class="table-cell">${data[4]}</h3>
            </div>
        `).appendTo("#table-body");
    }

    // Fade the table in
    finish_loading("#table", "#table-head, #table-body");
}

