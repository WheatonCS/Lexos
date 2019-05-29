$(function(){

    // Check that there is exactly one document active, initialize the legacy
    // form input if applicable, and display the appropriate text on the
    // "Rolling Window" section
    $.ajax({type: "GET", url: "/active-file-ids"})
        .done(single_active_document_check);

    // Create the "Generate" button callback
    $("#generate-button").click(create_rolling_window);

    // Create the "Download" button callback
    $("#download-button").click(function(){ $("#download-input").click(); });
});


/**
 * Checks that there is exactly one document active.
 * @param {string} response: The response from the "get-active-files" request.
 */
function single_active_document_check(response){

    // Get the active document IDs
    let documents = Object.entries($.parseJSON(response));

    // If there is not exactly one active document, display warning text and
    // disable the "Generate" and "Download" buttons
    let text;
    if(documents.length !== 1){
        text = "This Tool Requires a Single Active Document";
        $("#generate-button").addClass("disabled");
        $("#download-button").addClass("disabled");
    }

    // Otherwise, set the legacy form input for the file to analyze to the
    // active document and display "No Graph" text
    else {
        text = "No Graph";
        $("#file-to-analyze").val(documents[0][0]);
    }

    // Display the text
    add_text_overlay("#rolling-window", text);
}


/**
 * Creates the Plotly rolling window graph.
 */
function create_rolling_window(){

    // Add the loading overlay
    add_loading_overlay("#rolling-window");

    // Send the request for the rolling window Plotly graph HTML
    send_ajax_form_request("/rolling-window/get-graph")
    .done(function(response){

        // Remove any existing content in the rolling window element
        let rolling_window = $("#rolling-window");
        rolling_window.empty();

        // Add the Plotly graph HTML and fade the element in
        $("#rolling-window").html(response);
        fade_in(rolling_window);
    });
}

