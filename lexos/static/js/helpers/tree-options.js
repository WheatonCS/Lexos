/**
 * Registers options popup creation callbacks for the "Distance Metric" and
 * "Linkage Method" buttons.
 */
function initialize_tree_options(){

    // Register the "Distance Metric" button callback
    $("#distance-metric-button").click(function(){
        create_radio_options_popup("Distance Metric", "distance_metric",
            "#distance-metric-button", "#distance-metric-input", [
            ["euclidean", "Euclidean"],
            ["minkowski", "Minkowski"],
            ["cityblock", "Manhattan"],
            ["seuclidean", "Standard Euclidean"],
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
        create_radio_options_popup("Linkage Method", "linkage_method",
            "#linkage-method-button", "#linkage-method-input", [
            ["average", "Average"],
            ["single", "Single"],
            ["complete", "Complete"],
            ["weighted", "Weighted"]]);
    });
}
