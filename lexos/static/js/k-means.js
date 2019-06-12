$(function(){

    // Display the loading overlay on the "K-Means" section
    start_loading("#graph-container");

    // Initialize the tooltips for the "Options", "Advanced", "Tokenize",
    // "Normalize", and "Cull" sections
    initialize_analyze_tooltips();
    initialize_tooltips();

    // Check that there are at least two active documents, initialize the
    // legacy inputs and the "Generate" and "Download" buttons, create the
    // k-means graph, and get the CSV data
    get_active_file_ids(initialize, "#graph-container");
});


/**
 * Checks that there are at least two active documents, initializes the legacy
 *      inputs and the "Generate" and "Download" buttons, creates the k-means
 *      graph, and gets the CSV data.
 * @param {string} response: The response from the "active-file-ids" request.
 */
let document_count;
let csv;
function initialize(response){

    // Initialize the legacy form inputs. If there are no active documents,
    // display "No Active Documents" text and return
    if(!initialize_legacy_inputs(response)){
        add_text_overlay("#graph-container", "No Active Documents");
        return;
    }

    // If there are fewer than two active documents, display warning text
    // and return
    document_count = Object.entries(parse_json(response)).length;
    if(document_count <  2){
        add_text_overlay("#graph-container",
            "This Tool Requires at Least Two Active Documents");
        return;
    }

    // Otherwise, set the default "Clusters" value
    $("#clusters-input").val(Math.floor(document_count/2)+1);

    // Create the k-means graph and get the CSV data
    send_k_means_result_request();

    // If the "Generate" button is pressed, recreate the k-means graph
    $("#generate-button").click(function(){

        // Validate the inputs
        if(!validate_k_means_inputs() || !validate_analyze_inputs()) return;

        // Remove any existing Plotly graphs
        remove_graphs();

        // Remove any existing error messages
        remove_errors();

        // Display the loading overlays and disable the "Generate" and
        // "Download" buttons
        start_loading("#graph-container",
            "#generate-button, #download-button");

        // Create the k-means graph and get the CSV data
        send_k_means_result_request();
    });

    // If the "Download" button is pressed, download the CSV
    $("#download-button").click(function(){ download(csv, "k-means.csv"); });
}


/**
 * Creates the k-means graph and gets the CSV data.
 */
function send_k_means_result_request(){

    // Send a request for the k-means results
    send_ajax_form_request("/k-means/results")

        // If the request was successful, initialize the graph, store the CSV
        // data, and enable the "Generate" and "Download" buttons
        .done(function(response){
            csv = response.csv;
            initialize_graph(response.graph);
            enable("#generate-button, #download-button");
        })

        // If the request failed, display an error and enable the "Generate"
        // button
        .fail(function(){
            error("Failed to retrieve the k-means data.");
            enable("#generate-button");
        });
}


/**
 * Validates the inputs in the "Options" and "Advanced" sections.
 * @return {boolean}: Whether the inputs are valid.
 */
function validate_k_means_inputs(){

    // "Clusters"
    if(!validate_number($("#clusters-input").val(), 1, document_count)){
        error("Invalid number of clusters.");
        return false;
    }

    // "Maximum Iterations"
    if(!validate_number($("#maximum-iterations-input").val(), 1)){
        error("Invalid number of maximum iterations.");
        return false;
    }

    // "Different Centroids"
    if(!validate_number($("#different-centroids-input").val(), 1)){
        error("Invalid number of different centroids.");
        return false;
    }

    // "Relative Tolerance"
    if(!validate_number($("#relative-tolerance-input").val(), 0)){
        error("Invalid relative tolerance.");
        return false;
    }

    return true;
}


/**
 * Initialize the tooltips.
 */
function initialize_tooltips(){

    // "Clusters"
    create_tooltip("#clusters-tooltip-button", `The number of clusters (or
        the number of centroids). The number of clusters should always be 
        fewer or equal to the number of active documents. By default, this
        value is set to half the number of active documents.`);

    // Visualization
    create_tooltip("#visualization-method-tooltip-button", `2D-Scatter plot
        and Voroni diagram will reduce the DTM to a two dimensional matrix,
        whereas 3D-Scatter plot will reduce the DTM to a three dimensional
        matrix. Compared to the scatter plots, Voronoi displays the centroids
        and draws polygons for each document cluster.`);

    // Initialization method
    create_tooltip("#initialization-method-tooltip-button", `"K-Means++
        selects initial cluster centers using a weighted probability
        distribution to speed up convergence. "Random" chooses k observations
        at random from the data to serve as the initial centroids.`);

    // "Different Centroids"
    create_tooltip("#different-centroids-tooltip-button", `The number of times
        (n) the k-means algorithm will be run with different centroid seeds.
        The final results will be the best output of those n consecutive
        runs.`);

    // "Relative Tolerance"
    create_tooltip("#relative-tolerance-tooltip-button", `Decimal, relative
        tolerance with respect to inertia to declare convergence.`);
}
