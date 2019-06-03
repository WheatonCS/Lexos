$(function(){

    // Display the loading overlay on the "K-Means" section
    start_loading("#graph-container");

     // Initialize the legacy inputs and create the k-means graph
     $.ajax({type: "GET", url: "/active-file-ids"}).done(initialize);
});


/**
 * Initializes legacy inputs and creates the k-means graph.
 * @param {string} response: The response from the "active-file-ids" request.
 */
function initialize(response){

    // Initialize legacy inputs
    if(!initialize_legacy_inputs(response)) return;

    // Set the default clusters value
    let document_count = Object.entries(JSON.parse(response)).length;
    $("#clusters").val(Math.floor(document_count/2)+1);

    // Create the k-means graph
    create_graph("k-means/graph");

    // If the "Generate" button is pressed, reload the k-means graph.
    $("#generate-button").click(function(){
        start_loading("#graph-container", "#generate-button");
        create_graph("k-means/graph");
    });
}
