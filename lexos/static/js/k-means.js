$(function(){

     // Initialize legacy inputs and create the k-means graph
     $.ajax({type: "GET", url: "/active-file-ids"}).done(initialize);
});


/**
 * Initializes legacy inputs and creates the dendrogram.
 * @param {string} response: The response from the active-file-ids request.
 */
function initialize(response){

    // Initialize legacy inputs
    if(!initialize_legacy_inputs(response)) return;

    // Set the default clusters value
    let document_count = Object.entries(JSON.parse(response)).length;
    $("#clusters").val(Math.round(document_count/2));

    // Create the k-means graph
    create_k_means_graph();

    // Register the generate button callback
    $("#generate-button").click(function(){ create_k_means_graph(); });
}


function create_k_means_graph(response){

    // Add the loading overlay
    add_loading_overlay("#k-means");

    // Create the k-means graph
    send_ajax_form_request("k-means/graph").done(function(response){

        // Clear any existing contents in the k-means section
        let k_means_element = $("#k-means");
        k_means_element.empty();

        // Add the Plotly graph HTML to the k-means section
        k_means_element.html(response.plot);

        // Fade in the k-means section
        fade_in("#k-means");
    });

}
