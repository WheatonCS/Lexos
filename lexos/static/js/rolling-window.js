$(function(){

    // Send a request to get the active files and their IDs
    $.ajax({type: "GET", url: "/active-file-ids"})

        // If the request is successful, check that there is exactly one
        // document active and display the appropriate text on the
        // "Rolling Window" section
        .done(single_active_document_check);

    // If the "Generate" button is clicked, create the rolling window graph
    $("#generate-button").click(function(){
        create_graph("/rolling-window/get-graph");
    });

    // If the "Download" button is clicked, for legacy compatibility, click
    // the "download-input" button which sends a download request
    $("#download-button").click(function(){ $("#download-input").click(); });
});


/**
 * Checks that there is exactly one document active and sets the appropriate
 * text in the "Rolling Window" section.
 * @param {string} response: The response from the "get-active-files" request.
 */
function single_active_document_check(response){

    // Get the active documents
    let documents = Object.entries($.parseJSON(response));

    // If there is not exactly one active document, display warning text and
    // disable the "Generate" and "Download" buttons in the "Rolling Window"
    // section
    let text;
    if(documents.length !== 1){
        text = "This Tool Requires A Single Active Document";
        $("#generate-button").addClass("disabled");
        $("#download-button").addClass("disabled");
    }

    // Otherwise, set the legacy form input for the file to analyze to the
    // active document and display "No Graph" text
    else {
        text = "No Graph";
        $("#file-to-analyze").val(documents[0][0]);
    }

    // Display the text in the graph container
    add_text_overlay("#graph-container", text);
}
