$(function(){

    // Create the loading overlay for the dendrogram graph
    start_loading("#consensus-tree-section-body");

    // Register option popup creation callbacks for the "Distance Metric" and
    // "Linkage Method" buttons
    initialize_tree_options();

    // Initialize legacy form inputs and create the consensus tree
    $.ajax({type: "GET", url: "/active-file-ids"}).done(initialize);
});


/**
 * Initializes legacy form inputs and creates the consensus tree.
 * @param {string} response: The response from the "active-file-ids" request.
 */
function initialize(response){

    // Initialize the legacy form inputs
    if(!initialize_legacy_inputs(response)) return;

    // Create the consensus tree
    create_consensus_tree();

    // When the "Generate" button is pressed, recreate the consensus tree
    $("#generate-button").click(function(){
        start_loading("#consensus-tree-section-body", "#generate-button");
        create_consensus_tree();
    });
}


/**
 * Creates the consensus tree.
 */
function create_consensus_tree(){
    send_ajax_form_request("consensus-tree/graph")
        .done(function(response){

            // Create the consensus tree
            $(`
                <div id="consensus-tree" class="hidden">
                    <img src="data:image/png;base64,${response}">
                </div>
            `).appendTo("#consensus-tree-section-body");

            // Remove the loading overlay, fade in the consensus tree,
            // and enable the "Generate" button
            finish_loading("#consensus-tree-section-body",
                "#consensus-tree", "#generate-button")
        });
}
