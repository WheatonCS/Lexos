$(function(){

    // Display the loading overlay on the "Dendrogram" section
    start_loading("#graph-container");

    // Register option popup creation callbacks for the "Distance Metric" and
    // "Linkage Method" buttons
    initialize_tree_options();

    // If the "Orientation" button is pressed, display a radio options popup
    $("#orientation-button").click(function(){
        create_radio_options_popup("Orientation", "orientation",
            "#orientation-button", "#orientation-input",
            [["left", "Left"],  ["bottom", "Bottom"]]);
    });

    // Initialize legacy form inputs and create the dendrogram
    $.ajax({type: "GET", url: "/active-file-ids"}).done(initialize);
});


/**
 * Initializes legacy form inputs and creates the dendrogram.
 * @param {string} response: The response from the "active-file-ids" request.
 */
function initialize(response){

    // Initialize legacy form inputs
    if(!initialize_legacy_inputs(response)) return;

    // If there are fewer than two active files, display warning text and
    // return
    if(Object.entries(JSON.parse(response)).length < 2){
        add_text_overlay("#graph-container",
            "This Tool Requires At Least Two Active Documents");
        return;
    }

    // Otherwise, create the dendrogram
    create_graph("dendrogram/graph");

    // When the "Generate" button is pressed, recreate the dendrogram
    $("#generate-button").click(function(){
        start_loading("#graph-container", "#generate-button");
        create_graph("dendrogram/graph");
    });
}
