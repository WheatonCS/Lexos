let page_count = 1;
let previous_page_number = -1;
let loading = false;
let queue = {queued: false, page_change: false};
let selected_column = 0;

$(function(){

    // Send the request for the active file IDs
    $.ajax({type: "GET", url: "/active-file-ids"})

        // If the request is successful, initialize the legacy inputs and create the table
        .done(initialize)

        // If the request failed, display an error
        .fail(function(){ error("Failed to retrieve"+
            "the active document IDs."); });
})


/**
 * Initializes the legacy inputs and creates the table.
 * @param {string} response: The response from the "/active-file-ids" request.
 */
function initialize(response){

    // Initialize the legacy inputs
    if(!initialize_legacy_inputs(response)){

        // If there are no active documents, display "No Active Documents"
        // text and return
        add_text_overlay("#table-data", "No Active Documents");
        return;
    }

    // Enable the "Generate" and "Download" buttons
    enable("#generate-button, #download-button");

    // Create the table
    send_table_data_request();

    // Create callbacks for the buttons and inputs on the table
    create_table_button_callbacks();
}


/**
 * Validates the page number, sends a request for the table data and creates
 * the table.
 * @param {boolean} page_change: Whether the action that triggered this table
 *      creation was a page change.
 * @param {boolean} queued_request: Whether this table creation was queued.
 */
function send_table_data_request(page_change = true, queued_request = false){

    // Perform the immediate validation checks
    immediate_validation(page_change);

    // If the table is already loading, queue a recreation and return
    if(loading){

        // If there is already a recreation queued, prefer resetting the page
        if(queue.queued) if(!page_change) queue.page_change = false;
        else queue.page_change = page_change;
        queue.queued = true;
        return;
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
    let page_number = page_number_element.val();
    if(isNaN(page_number) || page_change & (page_number ===
        previous_page_number) || !validate_analyze_inputs()){
        loading = false;
        execute_queued_table_recreation();
        return;
    }

    // Otherwise, update the previous page number
    previous_page_number = page_number;

    // Display the loading overlay on the table
    if(!queued_request) start_loading("#table-data");
    let start = (page_number-1)*$(`input[name="length"]:checked`).val();

    send_ajax_form_request("tokenize/get-table",
        { "sort-column": selected_column, start: start })

        // If the request was successful, recreate the table
        .done(create_table)

        // If the request failed, display an error
        .fail(function(){ error("Failed to retrieve the table data."); });
}


/**
 * Creates the table.
 * @param {string} response: The response from the "tokenize/get-table" request.
 */
function create_table(response){

    // If there is a queued table recreation, execute it and return
    loading = false;
    if(queue.queued){
        execute_queued_table_recreation();
        return;
    }

    // Otherwise, parse the response
    response = parse_json(response);

    // Set the page count
    page_count = parseInt(response["pages"]);
    $("#page-count").text(page_count);

    // If there is no data, display "No Data" text and return
    if(response["data"].length === 0){
        add_text_overlay("#table-body", "No Data");
        return;
    }

    // Create the table layout
    $(`
        <div id="table-data-grid" class="hidden">
            <div id="table-head"></div>
            <div id="table-body" class="hidden-scrollbar"></div>
        </div>
    `).appendTo("#table-data");

    // Create the table head
    response["head"].unshift("Terms");
    let id = 0;
    for(cell of response["head"]){

        // Create the cell element
        let cell_element = $(`<h3 id=${id} class="table-cell"></h3>`)
            .appendTo("#table-head");
        ++id;
        cell_element.text(cell);

        // If a column is clicked, select it and recreate the table if it
        // was not previously selected
        cell_element.click(function(){
            let id = $(this).attr("id");
            if(selected_column !== id){
                selected_column = id;
                send_table_data_request(false);
            }
        });
    }

    // Highlight the cell of the selected column
    $(`#table-head #${selected_column}`).addClass("selected-cell");

    // Populate the table body
    let table_body_element = $("#table-body");
    for(row of response["data"]){

        // Create a row
        let row_element = $(`<div class="table-row"></div>`)
            .appendTo(table_body_element);

        // Populate the row with cells
        for(cell of row){
            let element = $(`<h3 class="table-cell"></h3>`)
                .appendTo(row_element);
            element.text(cell);
        }
    }


    // Remove the loading overlay and fade in the table data
    finish_loading("#table-data", "#table-data-grid");
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
    $("#generate-button").click(function(){ send_table_data_request(false); });

    // If the "Download" button is pressed, download the table as a CSV
    $("#download-button").click(function(){
        $("#trigger-download").click();
    });

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
 */
function execute_queued_table_recreation(){

    // If a table recreation was queued, perform the reload
    if(queue.queued){
        queue.queued = false;
        send_table_data_request(queue.page_change, true);
        queue.page_change = false;
    }
}


/**
 * Performs page number validation checks that should occur whether or not the
 *  table will be recreated.
 * @param {boolean} page_change: Whether the action that triggered the table
 *      recreation was a page change.
 */
function immediate_validation(page_change){

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
