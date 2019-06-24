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

    // Initialize the legacy form inputs and create the dendrogram
    get_active_file_ids(initialize, "#graph-container");

    // Initialize the tooltips
    initialize_analyze_tooltips();
    initialize_tooltips();

    // Initialize the walkthrough
    initialize_walkthrough(walkthrough);
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
            "This Tool Requires at Least Two Active Documents");
        return;
    }

    // Create the dendrogram
    create_graph("dendrogram/graph");

    // When the "Generate" button is pressed, recreate the dendrogram
    $("#generate-button").click(function(){

        // Validate the inputs
        if(!validate_analyze_inputs()) return;

        // Remove any existing Plotly graphs
        remove_graphs();

        // Remove any existing error messages
        remove_errors();

        // Display the loading overlay and disable the appropriate buttons
        start_loading("#graph-container",
            "#generate-button, #png-button, #svg-button");

        // Create the Plotly dendrogram graph
        create_graph("dendrogram/graph");
    });

    // If the "PNG" or "SVG" buttons are pressed, download the graph
    initialize_graph_download_buttons();
}


/**
 * Initializes the tooltips.
 */
function initialize_tooltips(){

    // "Distance Metric"
    create_tooltip("#distance-metric-tooltip-button", `The method for measuring
        the distance (difference) between documents.`);

    // "Linkage Method"
    create_tooltip("#linkage-method-tooltip-button", `The method used to
        determine when documents and/or other sub-clusters should be joined
        into new clusters.`);
}


/**
 * Initializes the walkthrough.
 */
function walkthrough(){

    let intro = introJs();
    intro.setOptions({steps: [
        {
            intro: `Welcome to Dendrogram!`,
            position: "top",
        },
        {
            element: "#dendrogram-options-section",
            intro: `These settings control how the Dendrogram is generated.
                Orientation changes which way the graph is displayed.`,
            position: "top",
        },
        {
            element: "#tokenize-section",
            intro: `Tokenize determines how terms are counted when generating
                data.`,
            position: "top",
        },
        {
            element: "#normalize-section",
            intro: `Normalize determines if and how term totals are weighted.`,
            position: "top",
        },
        {
            element: "#cull-section",
            intro: `Cull limits the number of terms used to generate data, and
                is optional.`,
            position: "top",
        },
        {
            element: "#dendrogram-buttons",
            intro: `Here you can generate a new Dendrogram. You can also
                choose to download the Dendrogram as a static PNG or a vector
                SVG.`,
            position: "top",
        },
        {
            intro: `This concludes the Dendrogram walkthrough!`,
            position: "top",
        }
    ]});

    intro.start();
}
