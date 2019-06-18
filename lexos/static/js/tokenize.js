let page_count = 1;
let previous_page_number = -1;
let loading = false;
let queue = {queued: false, page_change: false};
let selected_column = 0;

$(function(){

    // Initialize the "Tokenize", "Normalize", and "Cull" tooltips
    initialize_analyze_tooltips();

    //Initialize the "Orientation" tooltip
    create_tooltip("#orientation-tooltip-button", `This option will not be
        represented in the table below, but will be applied to the file sent
        when the "Download" button is clicked.`);

    // Initialize the legacy form inputs and create the token table
    get_active_file_ids(initialize, "#generate-button, #download-button");
})


/**
 * Initializes the "Download" button.
 */
function initialize_download_button(){

    // If the "Download" button is pressed...
    $("#download-button").click(function(){

        // Validate inputs, disable the "Generate" and "Download" buttons
        // and remove any existing error messages
        if(!validate_table(false)) return;
        disable("#download-button");

        // Send a request for the table data
        send_ajax_form_request("tokenize/csv",
            {"sort-column": selected_column, "start": 0})

            // Always enable the "Download" button, set the "loading" variable
            // to false, and execute any queued requests
            .always(function(){
                loading = false;
                enable("#download-button");
                if(queue.queued) execute_queued_table_recreation(true);
            })

            // If the request was successful, download the document statistics
            .done(function(response){ download(response, "tokenizer.csv"); })

            // If the request failed, display an error message
            .fail(function(){
                error("Failed to download the tokenizer data.");
            });
    });
}


/**
 * Initializes the legacy inputs and creates the token table.
 * @param {string} response: The response from the "active-file-ids" request.
 */
function initialize(response){

    // Initialize the legacy inputs
    if(!initialize_legacy_inputs(response)){

        // If there are no active documents, display "No Active Documents"
        // text and return
        add_text_overlay("#table", "No Active Documents");
        return;
    }

    // Enable the "Generate" and "Download" buttons
    enable("#generate-button, #download-button");

    // Create the token table
    send_table_data_request();

    // Create callbacks for the buttons and inputs on the token table
    create_table_button_callbacks();
}


/**
 * Validates the page number, sends a request for the token table data and
 *      creates the table.
 * @param {boolean} page_change: Whether the action that triggered this table
 *      creation was a page change.
 * @param {boolean} loading_overlay: Whether to display the loading overlay.
 */
let page_number;
function send_table_data_request(page_change = true, loading_overlay = true){

    // Perform table checks
    if(!validate_table(page_change)) return;

    // Display the loading overlay on the table
    if(loading_overlay) start_loading("#table", "#download-button");
    let start = (page_number-1)*$(`input[name="length"]:checked`).val();

    send_ajax_form_request("tokenize/table",
        { "sort-column": selected_column, "start": start })

        // If the request was successful, recreate the table
        .done(create_token_table)

        // If the request failed, display an error
        .fail(function(){
            error("Failed to retrieve the token table data.");
            add_text_overlay("#table", "Loading Failed");
        });
}


/**
 * Performs the necessary validation for table generation.
 * @param {boolean} page_change: Whether the page has changed.
 * @return {boolean}: Whether the table inputs are valid.
 */
function validate_table(page_change){

    // Perform the immediate validation checks
    immediate_table_validation(page_change);

    // If the table is already loading, queue a recreation and return
    if(loading){

        // If there is already a recreation queued, prefer resetting the page
        if(queue.queued){ if(!page_change) queue.page_change = false; }
        else queue.page_change = page_change;
        queue.queued = true;
        return false;
    }

    // Otherwise, set the "loading" variable to true
    loading = true;

    // Reset the page number to 1 if the "Rows Per Page" or "Search" option
    // was changed
    let page_number_element = $("#page-number");
    if(!page_change) page_number_element.val("1");

    // Return if the input page number is not parsable, if a page change was
    // attempted but the page number remained the same due to clamping or
    // input of the same number, or if the "Tokenize" or "Cull" sections have
    // an invalid input
    page_number = page_number_element.val();
    if(isNaN(page_number) || page_change & (page_number ===
        previous_page_number) || !validate_analyze_inputs()){
        loading = false;
        execute_queued_table_recreation();
        return false;
    }

    // Otherwise, update the previous page number and remove any existing
    // error messages
    previous_page_number = page_number;
    remove_errors();

    return true;
}


/**
 * Creates the table.
 * @param {string} response: The response from the "tokenize/get-table" request.
 */
function create_token_table(response){

    // If there is a queued table recreation, execute it and return
    loading = false;
    if(queue.queued){
        execute_queued_table_recreation();
        return;
    }

    // Otherwise, parse the response
    let parsed_response = parse_json(response);

    // Set the page count
    page_count = parseInt(parsed_response["pages"]);
    $("#page-count").text(page_count);

    // If there is no data, display "No Data" text and return
    if(parsed_response["data"].length === 0){
        add_text_overlay("#table", "No Data");
        return;
    }

    // Otherwise, create the table
    parsed_response["head"].unshift("Term")
    create_table("#table", parsed_response["data"],
        parsed_response["head"], '',
        function(selected_head_cell_id){
            selected_column = selected_head_cell_id;
            send_table_data_request(false);
        }, selected_column);

    // Remove the loading overlay and fade in the table data
    finish_loading("#table", ".lexos-table", "#download-button");
}


/**
 * Creates callbacks for the buttons and inputs on the table
 */
function create_table_button_callbacks(){

    // Get the page number element
    let page_number_element = $("#page-number");

    // If the "Search" input is changed, recreate the table
    $("#search-input").on("input", function(){
        send_table_data_request(false);
    });

    // If the "Rows Per Page" option is changed, recreate the table
    $(`input[type="radio"][name="length"],
        input[type="radio"][name="sort-ascending"]`)
        .change(function(){ send_table_data_request(false); });

    // If the "Generate" button is pressed, recreate the table
    $("#generate-button").click(function(){
        send_table_data_request(false);
    });

    // Initialize the "Download" button
    initialize_download_button();

    // If the page number input is changed, recreate the table
    $(page_number_element).on("input", function(){
        send_table_data_request();
    });

    // If the "Previous" button is clicked, decrement the page number and
    // recreate the table
    $("#previous-button").click(function(){
        page_number_element.val(parseInt(page_number_element.val())-1);
        send_table_data_request();
    });

    // If the "Next" button is clicked, increment the page number and recreate
    // the table
    $("#next-button").click(function(){
        page_number_element.val(parseInt(page_number_element.val())+1);
        send_table_data_request();
    });
}


/**
 * Executes the queued table recreation if it exists.
 * @param {boolean} loading_overlay: Whether to show the loading overlay.
 */
function execute_queued_table_recreation(loading_overlay = false){

    // If a table recreation was queued, perform the reload
    if(queue.queued){
        queue.queued = false;
        send_table_data_request(queue.page_change, loading_overlay);
        queue.page_change = false;
    }
}


/**
 * Performs page number validation checks that should occur whether or not the
 *  table will be recreated.
 * @param {boolean} page_change: Whether the action that triggered the table
 *      recreation was a page change.
 */
function immediate_table_validation(page_change){

    // Parse the page number from the input
    let page_number_element = $("#page-number");
    let page_number = parseInt(page_number_element.val());

    // If there was no parsable page number...
    if(isNaN(page_number)){

        // If the calling action was a page change, clear the page number
        // input and return false
        if(page_change) page_number_element.val("");

        // Otherwise, the calling action was not a page change, so set the
        // page number to 1
        else page_number_element.val("1");
    }

    // Otherwise, clamp the page number between 1 and the last page
    else {
        page_number = Math.max(1, Math.min(page_count, page_number));
        page_number_element.val(page_number);
    }
}
