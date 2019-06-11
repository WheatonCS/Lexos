/**
 * Creates a Plotly graph.
 * @param {string} url: The URL to send the request for the Plotly graph to.
 * @param {function} callback: The function to call when loading completes.
 *      By default, the function re-enables the "Generate" button.
 */
function create_graph(url, callback =
    function(){ enable("#generate-button"); }){

    // Send the request for the Plotly graph
    send_ajax_form_request(url)

        // Always call the callback
        .always(callback)

        // If the request was successful, initialize the graph
        .done(function(response){
            initialize_graph(response);
        })

        // If the request failed, display an error and "Loading Failed" text
        .fail(function(){
            error("Failed to retrieve the Plotly data.");
            add_text_overlay("#graph-container", "Loading Failed");
        });
}


/**
 * Initializes the Plotly graph.
 * @param {string} graph_html: The Plotly graph HTML to display.
 */
function initialize_graph(graph_html){

    // Add the Plotly graph HTML
    $(`<div id="graph" class="hidden"></div>`)
        .html(graph_html)
        .appendTo("#graph-container");

    // Update the graph size
    update_graph_size();
    $(window).resize(update_graph_size);

    // Remove the loading overlay and show the graph
    finish_loading("#graph-container", "#graph");
}

/**
 * Removes any existing plotly graphs.
 */
function remove_graphs(){
    for(const element of $(".js-plotly-plot")) Plotly.purge(element);
}


/**
 * Updates the size of the graph to fit its containing element.
 */
function update_graph_size(){

    // Get the containing element
    let graph_container_element = $("#graph-container");

    // Resize the graph to fit the graph container
    Plotly.relayout($(".js-plotly-plot")[0], {width: graph_container_element.width(),
        height: graph_container_element.height(), responsive: false},
        {autosize: false});
}
