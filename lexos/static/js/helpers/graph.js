let graph_id;

/**
 * Creates a Plotly graph.
 * @param {string} url: The URL to send the request for the Plotly HTML to.
 * @param {function} callback: The function to call when loading completes.
 *      By default, the function re-enables the "Generate" button.
 */
function create_graph(url, callback =
    function(){ enable("#generate-button"); }){

    // Send the request for the Plotly graph HTML
    send_ajax_form_request(url)

    // If the request was successful...
    .done(function(response){

        // Add the Plotly graph HTML
        let graph_element = $(`<div id="graph" class="hidden"></div>`)
            .html(response)
            .appendTo("#graph-container");

        // Get the Plotly graph ID
        graph_id = graph_element.find(".js-plotly-plot").attr("id");

        // Update the graph size
        update_graph_size();
        $(window).resize(update_graph_size);

        // Remove the loading overlay and show the graph
        finish_loading("#graph-container", "#graph");

        // Call the callback
        callback();
    })

    // If the request failed, display an error and "Loading Failed" text and
    // call the callback
    .fail(function(){
        error("Failed to retrieve the Plotly data.");
        add_text_overlay("#graph-container", "Loading Failed");
        callback();
    });
}

/**
 * Updates the size of the graph to fit its containing element.
 */
function update_graph_size(){

    // Get the containing element
    let graph_container_element = $("#graph-container");

    // Resize the graph to fit the graph container
    Plotly.relayout(graph_id, {width: graph_container_element.width(),
        height: graph_container_element.height()});
}
