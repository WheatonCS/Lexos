let page_count = 1;
let page_number = 1;
let previous_page_number = -1;

$(function(){

    // Create the tokenizer table
    send_table_data_request();

    // Create callbacks for the buttons and inputs on the table
    create_table_button_callbacks();
})

/**
 * Sends a request for the table data and creates the table.
 * @param {boolean} page_change: Whether the request is a page change.
 */
function send_table_data_request(page_change = true){

    // Reset the page number to 1 if the "Rows Per Page" or "Search" option
    // was changed
    if(!page_change) page_number = 1;

    // Clamp the page number between 1 and the last page
    page_number = Math.max(1, Math.min(page_count, page_number));

    // Update the page number input element
    $("#page-number").val(page_number);

    // Return if a page change was attempted but the page number remained the
    // same due to clamping or input of the same number
    if(page_change && (page_number === previous_page_number)) return;
    previous_page_number = page_number;

    // Otherwise, display the loading overlay on the table
    start_loading("#table-data");

    // Send a request for the table data
    $.ajax({
        type: "POST",
        url: "tokenize/get-table",
        processData: false,
        contentType: false,
        data: new FormData($("form")[0])
    })

    // If the request was successful, recreate the table
    .done(create_table);
}


/**
 * Creates the table.
 * @param {string} response: The response from the "tokenize/get-table" request.
 */
function create_table(response){

    // Parse the response
    response = JSON.parse(response);

    // Set the page count
    page_count = parseInt(response.pages);
    $("#page-count").text(page_count);

    // If there is no data, display "No Data" text and return
    if(response.data.length === 0){
        add_text_overlay("#table-data", "No Data");
        return;
    }

    // Otherwise, create the table layout
    $(`
        <div id="table-data-grid" class="hidden">
            <div id="table-head"></div>
            <div id="table-body"></div>
        </div>
    `).appendTo("#table-data");

    // Create the table head
    response.head[0] = "Terms";
    for(cell of response.head){
        let element = $(`<h3 class="table-cell"></h3>`).appendTo("#table-head");
        element.text(cell);
    }

    // Create the table body
    let table_body_element = $("#table-body");
    for(row of response.data){

        // Create a row
        let row_element = $(`<div class="table-row"></div>`).appendTo(table_body_element);

        // Populate the row with cells
        for(cell of row){
            let element = $(`<h3 class="table-cell"></h3>`).appendTo(row_element);
            element.text(cell);
        }
    }

    // Remove the loading overlay and show the table data
    finish_loading("#table-data", "#table-data-grid");
}


/**
 * Creates callbacks for the buttons and inputs on the table
 */
function create_table_button_callbacks(){

    // Get the page number element
    let page_number_element = $("#page-number");

    // Recreate the table if the "Rows Per Page" option is changed
    $("input[type=radio][name=rows-per-page]").change(function(){
        send_table_data_request(false);
    });

    // Recreate the table if the "Search" input is changed
    $("#search-input").on("input", function(){
        send_table_data_request(false);
    });

    // If the page number input is changed, parse the input and recreate the
    // table if applicable
    $(page_number_element).on("input", function(){

        // Parse the page number
        let page_number_element = $("#page-number");
        page_number = parseInt(page_number_element.val());

        // If there are no numbers in the input, clear the input and return
        if(isNaN(page_number)){
            page_number_element.val("");
            return;
        }

        // Otherwise, create the table
        send_table_data_request();
    });

    // If the "Previous" button is clicked, decrement the page number and
    // recreate the table if applicable
    $("#previous-button").click(function(){
        page_number = parseInt(page_number_element.val())-1;
        send_table_data_request();
    });

    // If the "Next" button is clicked, increment the page number and recreate
    // the table if applicable
    $("#next-button").click(function(){
        page_number = parseInt(page_number_element.val())+1;
        send_table_data_request();
    });
}
