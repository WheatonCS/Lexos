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

    // Initialize the legacy form inputs. If there are no active documents,
    // display "No Active Documents" text and return
    if(!initialize_legacy_inputs(response)){
        add_text_overlay("#graph-container", "No Active Documents");
        return;
    }

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
