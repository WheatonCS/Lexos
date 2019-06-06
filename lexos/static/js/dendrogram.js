$(function(){

    // Initialize the "Tokenize", "Normalize", and "Cull" tooltips
    initialize_analyze_tooltips();

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

    create_tooltips();
});


/**
 * Initializes legacy form inputs and creates the dendrogram.
 * @param {string} response: The response from the "active-file-ids" request.
 */
function initialize(response){

    // Initialize the legacy form inputs. If there are no active documents,
    // display "No Active Documents" text and return
    if(!initialize_legacy_inputs(response)){
        add_text_overlay("#graph-container", "No Active Documents");
        return;
    }

    // If there are fewer than two active files, display warning
    // text and return
    if(Object.entries(parse_json(response)).length < 2){
        add_text_overlay("#graph-container",
            "This Tool Requires At Least Two Active Documents");
        return;
    }

    // Create the dendrogram
    create_graph("dendrogram/graph");

    // When the "Generate" button is pressed, recreate the dendrogram
    $("#generate-button").click(function(){
        if(!validate_analyze_inputs()) return;
        start_loading("#graph-container", "#generate-button");
        create_graph("dendrogram/graph");
    });
}

function create_tooltips(){
    create_tooltip("#distance-metric-tooltip-button", 'Different methods for measuring the distance (differences) between documents.');

    create_tooltip("#linkage-method-tooltip-button", 'Linkage is the method used to determine when documents and/or other sub-clusters should be joined into new clusters.');
}
