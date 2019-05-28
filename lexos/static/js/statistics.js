$(function(){
    $.ajax({type: "GET", url: "/active-file-ids"}).done(initialize);
});


function initialize(response){

    // Initialize legacy inputs
    if(!initialize_legacy_inputs(response)) return;

    // Start the loading overlays
    batch_add_loading_overlay(["#box-plot", "#table", "#corpus-statistics",
            "#standard-error-test", "#interquartile-range-test"]);

    // Get the corpus statistics
    send_ajax_form_request("/statistics/corpus")
        .done(create_corpus_statistics);

    // Get the document statistics
    send_ajax_form_request("/statistics/documents")
        .done(create_document_statistics);

    // Get the box plot
    send_ajax_form_request("/statistics/box-plot").done(function(response){
       let box_plot_element = $("#box-plot");
       box_plot_element.html(response);
       fade_in("#box-plot");
    });
}


function create_corpus_statistics(response){
    response = JSON.parse(response.replace(/\bNaN\b/g, "\"N/A\""));

    // Empty the elements
    let corpus_statistics_element = $("#corpus-statistics").empty();
    $("#standard-error-test").empty();
    $("#interquartile-range-test").empty();
    console.log(response);

    // Set the corpus statistics section data
    $(`
        <h3>Average: ${response.average}</h3><br>
        <h3>Standard Deviation: ${response.standard_deviation}</h3><br>
        <h3>Interquartile Range: ${response.interquartile_range}</h3>
    `).appendTo(corpus_statistics_element);

    // Set the standard error test data
    set_anomalies("standard-error", response.standard_error_small,
        response.standard_error_large);

    // Set the interquartile range test data
    set_anomalies("interquartile-range", response.interquartile_range_small,
        response.interquartile_range_large);

    // Fade in the elements
    batch_fade_in(["#corpus-statistics", "#standard-error-test",
        "#interquartile-range-test"]);
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

    // Empty the table element
    let table_element = $("#table").empty();

    // Append the head and table body
    $(`
        <div id="table-head">
            <h3 class="table-head-cell">Name</h3>
            <h3 class="table-head-cell">Total Terms</h3>
            <h3 class="table-head-cell">Distinct Terms</h3>
            <h3 class="table-head-cell">Average Terms</h3>
            <h3 class="table-head-cell">Single-Occurrence Terms</h3>
        </div>
        <div id="table-body"></div>
    `).appendTo(table_element);

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
    fade_in("#table");
}

