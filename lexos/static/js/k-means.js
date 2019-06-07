$(function(){

    // Initialize the "Tokenize", "Normalize", and "Cull" tooltips
    initialize_analyze_tooltips();

    // Display the loading overlay on the "K-Means" section
    start_loading("#graph-container");

     // Initialize the legacy inputs and create the k-means graph
     $.ajax({type: "GET", url: "/active-file-ids"}).done(initialize);

     create_tooltips();
});


/**
 * Initializes legacy inputs and creates the k-means graph.
 * @param {string} response: The response from the "active-file-ids" request.
 */
let document_count;
function initialize(response){

    // Initialize the legacy form inputs. If there are no active documents,
    // display "No Active Documents" text and return
    if(!initialize_legacy_inputs(response)){
        add_text_overlay("#graph-container", "No Active Documents");
        return;
    }

    // Set the default clusters value
    document_count = Object.entries(parse_json(response)).length;
    $("#clusters-input").val(Math.floor(document_count/2)+1);

    // Create the k-means graph
    create_graph("k-means/graph");

    // If the "Generate" button is pressed, reload the k-means graph.
    $("#generate-button").click(function(){
        if(!validate_k_means_inputs() || !validate_analyze_inputs()) return;
        start_loading("#graph-container", "#generate-button");
        create_graph("k-means/graph");
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

function create_tooltips(){
    //Clusters
    create_tooltip("#numclusters-tooltip-button", 'The number of clusters (or the number of centroids). ' +
        'The K-value should always be fewer or equal to the number of active documents. By default, this value is set to half the number of active documents.');

    //Visualization
    create_tooltip("#visualization-method-tooltip-button", '2D-Scatter plot and Voroni diagram will reduce the DTM to a two dimensional matrix, whereas ' +
        '3D-Scatter plot will reduce the DTM to a three dimensional matrix. Compared to the scatter plots, Voroni displays the centroids and draws polygons for each document cluster.');

    //Initialization Method
    create_tooltip("#initialization-method-tooltip-button", '\'kmeans++\' selects initial cluster centers using a weighted probability distribution to speed up convergence. The \'random\' option' +
        'chooses k observations at random from the data to serve as the initial centroids.');

    //Max Iterations
    create_tooltip("#max-iterations-tooltip-button", 'Maximum number of iterations for the k-means algorithm for a single run. The default is 300.');

    //Different Centroids
    create_tooltip("#diff-centroids-tooltip-button", 'The number of times (N) the k-means algorithm will be run with different centroid seeds. The final' +
        ' results will be the best output of those N consecutive runs. (The default is 10).');

    //Relative Tolerance
    create_tooltip("#relative-tolerance-tooltip-button", 'Decimal, relative tolerance with respect to inertia to declare convergence.');
}
