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
