let checked_options = {
    "distance-metric": "euclidean",
    "linkage-method": "average",
    "orientation": "bottom"
};


$(function(){

    // Register the "Distance Metric" button callback
    $("#distance-metric-button").click(function(){
        create_options_popup("distance-metric", [
            ["euclidean", "Euclidean"],
            ["minkowski", "Minkowski"],
            ["cityblock", "Manhattan"],
            ["seuclidean", "Standardized Euclidean"],
            ["sqeuclidean", "Squared Euclidean"],
            ["cosine", "Cosine"],
            ["correlation", "Correlation"],
            ["hamming", "Hamming"],
            ["chebyshev", "Chebychev"],
            ["jaccard", "Jaccard"],
            ["canberra", "Canberra"],
            ["braycurtis", "Braycurtis"]]);
    });

    // Register the "Linkage Method" button callback
    $("#linkage-method-button").click(function(){
        create_options_popup("linkage-method", [
            ["average", "Average"],
            ["single", "Single"],
            ["complete", "Complete"],
            ["weighted", "Weighted"]]);
    });

    // Register the "Orientation" button callback
    $("#orientation-button").click(function(){
        create_options_popup("orientation",
            [["bottom", "Bottom"], ["left", "Left"]]);
    });

    // Initialize legacy inputs and create the dendrogram
    $.ajax({type: "GET", url: "/active-file-ids"}).done(initialize);
});


/**
 * Initializes legacy form inputs and creates the dendrogram.
 * @param {string} response: The response from the active-file-ids request.
 */
function initialize(response){

    // Initialize legacy inputs
    if(!initialize_legacy_inputs(response)) return;

    // Create the dendrogram
    create_dendrogram();

    // Register the "Generate" button callback
    $("#generate-button").click(function(){ create_dendrogram(); });
}


/**
 * Creates a popup containing radio button options.
 * @param {string} name: The name of the radio buttons.
 * @param {string[][]} options: The value and text of each radio button.
 */
function create_options_popup(name, options){

    // Create the popup
    create_popup();
    let popup_content = $("#popup-content");

    for(const option of options) {
        let element = $(`
            <div>
                <label class="circle-label">
                    <input type="radio" name="${name}" value="${option[0]}">
                    <span>${option[1]}</span>
                </label>
            </div>
        `).appendTo(popup_content);

        //console.log(checked_options[name], formatted_option);
        if(checked_options[name] === option[0]){
            element.find("input").prop("checked", true);
        }
    }

    $(`<h3 id="ok-button" class="selectable">OK</h3>`).appendTo(popup_content);

    // Create the "OK" button callback
    $("#ok-button").click(function(){
        let selected_element = $(`input[name="${name}"]:checked`);
        $(`#${name}-input`).val(selected_element.val());
        $(`#${name}-text`).text(selected_element.closest("div").find("span").html());
        checked_options[name] = selected_element.val();
        console.log(selected_element.val());
        close_popup();
    });
}


/**
 * Creates the dendrogram.
 */
function create_dendrogram(){

    // Add the loading overlay to the dendrogram element
    add_loading_overlay("#dendrogram");

    // Send the request for the Plotly dendrogram HTML
    send_ajax_form_request("dendrogram/graph").done(function(response){

        // Delete any existing contents in the dendogram element
        let dendrogram_element = $("#dendrogram");
        dendrogram_element.empty();

        // Add the Plotly HTML to the dendrogram element
        dendrogram_element.html(response);

        // Fade the dendrogram element in
         fade_in("#dendrogram");
    });
}
