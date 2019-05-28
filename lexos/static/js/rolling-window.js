$(function(){

    // Initialize
    $.ajax({type: "GET", url: "/active-file-ids"})
        .done(valid_selection_check);

    // Create the generate button callback
    $("#generate-button").click(create_rolling_window);

    // Create the download button callback
    $("#download-button").click(function(){ $("#download-input").click(); });
});


/**
 * Checks that there is exactly one document active.
 * @param {String} response: The response from the get-active-files request.
 */
function valid_selection_check(response){

    // Get the active document IDs
    let documents = Object.entries($.parseJSON(response));

    // If there is not exactly one active document, display
    // "this tool requires a single active document" text and grey the
    // generate and download buttons out
    let text;
    if(documents.length !== 1){
        text = "This Tool Requires a Single Active Document";
        $("#generate-button").addClass("disabled");
        $("#download-button").addClass("disabled");
    }

    // Otherwise, set the active document element and display "no graph" text
    else {
        text = "No Graph";
        $("#file-to-analyze").val(documents[0][0]);
    }

    // Display the text
    $(`<div class="centerer"><h3>${text}</h3></div>`).appendTo("#rolling-window");
}


/**
 * Creates the rolling window data.
 */
function create_rolling_window(){

    // Remove the existing contents
    let rolling_window_element = $("#rolling-window");
    rolling_window_element.empty();
    rolling_window_element.css({"transition": "none", "opacity": "0"});

    // Send the get-graph request
    send_ajax_form_request("/rolling-window/get-graph")
    .done(function(response){
        $("#rolling-window").html(response);
        setTimeout(function(){ $("#rolling-window").css(
            {"transition": "opacity .2s", "opacity": "1"}); }, 100);
    });
}

