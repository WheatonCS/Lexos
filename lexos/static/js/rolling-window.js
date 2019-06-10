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
function single_active_document_check(response){

    // Get the active documents
    let documents = Object.entries(parse_json(response));

    // If there are no active documents, display "No Active Documents" text
    // on the "Rolling Window" section
    let text;
    if(documents.length === 0) text= "No Active Documents";

    // If there is more than one active document, display "This Tool Requires
    // A Single Active Document" text on the "Rolling Window" section
    else if(documents.length > 1)
        text = "This Tool Requires A Single Active Document";

    // Otherwise, set the legacy form input for the file to analyze to the
    // active document, display "No Graph" text on the "Rolling Window"
    // section, and enable the generate button
    else {
        text = "No Graph";
        $("#file-to-analyze").val(documents[0][0]);
        enable("#generate-button, #download-button");
    }

    // Display the text in the graph container
    add_text_overlay("#graph-container", text);

    // If the "Generate" button is clicked, create the rolling window graph
    $("#generate-button").click(create_rolling_window);

    // If the "Download" button is clicked, for legacy compatibility, click
    // the "download-input" button which sends a download request
    $("#download-button").click(function(){ $("#download-input").click(); });
}

/**
 * Creates the rolling window.
 */
function create_rolling_window(){

    // Validate the inputs
    if(!validate_inputs()) return;

    // Remove any existing errors
    remove_errors();

    // Display the loading overlay and disable the "Generate" and "Download"
    // buttons
    start_loading("#graph-container", "#generate-button, #download-button");

    // Create the rolling window graph
    create_graph("/rolling-window/get-graph",
        function(){ enable("#generate-button, #download-button"); });
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
