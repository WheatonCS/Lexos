let page_count = 1;
let page_number = 1;
let previous_page_number = -1;

$(function(){
    create_table();
    register_table_button_callbacks();
})

/**
 * Sends the request for the table data and creates the table.
 * @param {boolean} page_change: Whether the request is a page change.
 */
function create_table(page_change = true){

    // Reset the page number if the changed option was not the page number
    if(!page_change) page_number = 1;

    // Clamp the page number between 1 and the last page
    page_number = Math.max(1, Math.min(page_count, page_number));

    // Update the page number element
    $("#page-number").val(page_number);

    // Return if the page number has not changed and the changed option
    // was the page number
    if(page_change && (page_number === previous_page_number)) return;
    previous_page_number = page_number;

    // Display the loading overlay
    add_loading_overlay("#table-data");

    // Send the request for the table data
    $.ajax({
        type: "POST",
        url: "tokenize/get-table",
        processData: false,
        contentType: false,
        data: new FormData($("form")[0])
    }).done(get_table_callback);
}


/**
 * Creates the table.
 * @param {string} response: The response from the "tokenize/get-table" request.
 */
function get_table_callback(response){
    response = JSON.parse(response);

    // Set the page count
    page_count = parseInt(response.pages);
    $("#page-count").text(page_count);

    // If there are no rows, display "No Data" text
    if(response.data.length === 0){
        add_text_overlay("#table-data", "No Data");
        fade_in("#table-data");
        return;
    }

    // Otherwise, clear any existing content in the table data element
    let table_data_element = $("#table-data").empty();

    // Otherwise, create the table layout
    $(`
        <div id="table-data-grid">
            <div id="table-head"></div>
            <div id="table-body"></div>
        </div>
    `).appendTo(table_data_element);

    // Create the table head
    response.head[0] = "Terms";
    for(cell of response.head){
        let element = $(`<h3 class="tokenize-cell"></h3>`).appendTo("#table-head");
        element.text(cell);
    }

    // Create the table body
    let table_body_element = $("#table-body");
    for(row of response.data){
        let row_element = $(`<div class="tokenize-row"></div>`).appendTo(table_body_element);
        for(cell of row){
            let element = $(`<h3 class="tokenize-cell"></h3>`).appendTo(row_element);
            element.text(cell);
        }
    }

    // Fade in the table data
    fade_in("#table-data");
}


/**
 * Registers callbacks for each of the table buttons.
 */
function register_table_button_callbacks(){

    // Get the page number element
    let page_number_element = $("#page-number");

    // Rows per page
    $("input[type=radio][name=rows-per-page]").change(
        function(){ create_table(false); });

    // Search bar
    $("#search-input").on("input", function(){ create_table(false); });

    // Page number input
    $(page_number_element).on("input", function(){

        // Parse the page number
        let page_number_element = $("#page-number");
        page_number = parseInt(page_number_element.val());

        // Check that the input is valid
        if(isNaN(page_number)) page_number_element.val("");

        // Create the table
        create_table();
    });

    // Previous button
    $("#previous-button").click(function(){
        page_number = parseInt(page_number_element.val())-1;
        create_table();
    });

    // Next button
    $("#next-button").click(function(){
        page_number = parseInt(page_number_element.val())+1;
        create_table();
    });
}
