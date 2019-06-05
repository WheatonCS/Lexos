$(function(){

    // Create the loading overlay for the "Consensus Tree" section
    start_loading("#consensus-tree-body");

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

    // Initialize the legacy form inputs. If there are no active documents,
    // display "No Active Documents" text and return
    if(!initialize_legacy_inputs(response)){
        add_text_overlay("#consensus-tree-body", "No Active Documents");
        return;
    }

    // Create the consensus tree
    create_consensus_tree();

    // When the "Generate" button is pressed, recreate the consensus tree
    $("#generate-button").click(function(){
        if(!validate_consensus_tree_inputs() ||
            !validate_analyze_inputs()) return;
        start_loading("#consensus-tree-body", "#generate-button");
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
            `).appendTo("#consensus-tree-body");

            // Remove the loading overlay, fade in the consensus tree,
            // and enable the "Generate" button
            finish_loading("#consensus-tree-body",
                "#consensus-tree", "#generate-button")
        });
}


/**
 * Validate the consensus tree options inputs.
 * @returns {boolean}: Whether the inputs are valid.
 */
function validate_consensus_tree_inputs(){

    // "Cutoff"
    if(!validate_number($("#cutoff-input").val(), 0, 1)){
        error("Invalid cutoff.");
        return false;
    }

    // "Iterations"
    if(!validate_number($("#iterations-input").val(), 1)){
        error("Invalid number of iterations.");
        return false;
    }

    return true;
}
