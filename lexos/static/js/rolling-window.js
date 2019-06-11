$(function(){

    // Display the loading overlay
    start_loading("#graph-container");

    // Initialize the tooltips
    initialize_tooltips();

    // If the "Calculation Type" is changed, set the appropriate "Search
    // Terms" input
    $(`input[name="counttype"]`).change(function(){

        if($(`input[name="counttype"]:checked`).val() === "average")
            $("#search-terms-input-denominator").css("display", "none");
        else $("#search-terms-input-denominator").css("display", "inline");
    });

    // Check that there is exactly one document active and display the
    // appropriate text on the "Rolling Window" section
    get_active_file_ids(single_active_document_check, "#graph-container");
});


/**
 * Checks that there is exactly one document active and sets the appropriate
 * text in the "Rolling Window" section.
 * @param {string} response: The response from the "get-active-files" request.
 */
let csv;
function single_active_document_check(response){

    // Get the active documents
    let documents = Object.entries(parse_json(response));

    // If there are no active documents, display "No Active Documents" text
    // on the "Rolling Window" section
    if(documents.length === 0)
        add_text_overlay("#graph-container", "No Active Documents");

    // If there is more than one active document, display "This Tool Requires
    // A Single Active Document" text on the "Rolling Window" section
    else if(documents.length > 1) add_text_overlay("#graph-container",
        "This Tool Requires a Single Active Document");

    // Otherwise, set the legacy form input for the file to analyze to the
    // active document, display "No Graph" text on the "Rolling Window"
    // section, and enable the generate button
    else {
        add_text_overlay("#graph-container", "No Graph");
        $("#file-to-analyze").val(documents[0][0]);
        enable("#generate-button");
    }

    // If the "Generate" button is clicked, create the rolling window graph
    $("#generate-button").click(create_rolling_window);

    // If the "Download" button is pressed, download the CSV
    $("#download-button").click(function(){
        download(csv, "rolling-window.csv");
    });
}


/**
 * Creates the rolling window.
 */
function create_rolling_window(){

    // Validate the inputs
    if(!validate_inputs()) return;

    // Remove any existing Plotly graphs
    remove_graphs();

    // Remove any existing error messages
    remove_errors();

    // Display the loading overlay and disable the "Generate" and "Download"
    // buttons
    start_loading("#graph-container", "#generate-button, #download-button");

    // Create the rolling window graph and get the CSV data
    send_rolling_window_result_request();
}


/**
 * Creates the rolling window graph and gets the CSV data.
 */
function send_rolling_window_result_request(){

    // Send a request for the k-means results
    send_ajax_form_request("/rolling-window/results")

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
            error("Failed to retrieve the rolling window data.");
            enable("#generate-button");
        });
}


/**
 * Validates the inputs.
 * @return {boolean}: Whether the inputs are valid.
 */
function validate_inputs(){

    // "Search terms"
    if($("#search-terms-input").val().length < 1){
        error("Please enter the search terms.");
        return false;
    }

    // "Window"
    if(!validate_number($("#window-size-input").val(), 1)){
        error("Invalid window size.");
        return false;
    }

    // "Milestone"
    if($("#milestone-checkbox").is("checked") &&
        $("#milestone-input").val().length < 1){
        error("Please either enter a milestone or "+
            "uncheck the milestone option.");
        return false;
    }

    return true;
}


/**
 * Initializes the tooltips.
 */
function initialize_tooltips(){

    // "Rolling Average"
    create_tooltip("#rolling-average-tooltip-button", `Measures the number of
        times the input appears in the window, divided by the overall size of
        the window.`);

    // "Rolling Ratio"
    create_tooltip("#rolling-ratio-tooltip-button", `Measures the value of the
        first input divided by the sum of the first and second inputs.`);

    // "Search Terms" input
    create_tooltip("#search-terms-input-tooltip-button", `Please divide inputs
        by commas. For rolling ratios, input the numerator and denominator.`);

    // "Strings"
    create_tooltip("#strings-tooltip-button", `A string can be of any length.
        When searching for multiple stings, separate each string by comma with
        no whitespace. Any entered whitespace will be included in the
        search.`);

    // "Regex"
    create_tooltip("#regex-tooltip-button", `Visit
        <a href="https://en.wikipedia.org/wiki/Regular_expression"
        target="_blank">this page</a> for more information on regular
        expressions.`);

    // "Window"
    create_tooltip("#window-size-tooltip-button", `The number of characters,
        tokens, or lines each window should contain. The maximum size is
        10000.`);

    // "Milestone"
    create_tooltip("#milestone-tooltip-button", `Search the file for all
        instances of a specified string and plot a vertical dividing line at
        those locations.`, true);
}