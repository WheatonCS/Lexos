let page_count = 1;
let page_number;
let previous_page_number = -1;
let reset_page_number = false;

$(function(){
    create_table();
    register_table_button_callbacks();
})

/**
 * Creates the table.
 */
function create_table(){

    // Reset the page number if necessary
    if(reset_page_number){
        page_number = 1;
        reset_page_number = false;
        $("#page-number").val(page_number);
    }

    // Set the previous page number
    previous_page_number = page_number;

    // Clear the table and hide the table data
    $("#table-head").empty();
    $("#table-body").empty();
    $("#table-data").css({"opacity": "0", "transition": "none"});

    // Send the request
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
 *
 * @param {string} response: The response from the "tokenize/get-table" request.
 */
function get_table_callback(response){
    response = JSON.parse(response);
    let table_body = $("#table-body");

    // Set the page count
    page_count = parseInt(response.pages);
    $("#page-count").text(page_count);

    // If there are no rows, display "no data" text
    if(response.data.length === 0){

        // Create the "no data" text
        $(`
            <div id="no-data-text-container" class="centerer">
                <h3 id="no-data-text">No Data</h3>
            </div>
        `).appendTo(table_body);

        // Fade in the table data
        $("#table-data").css({"transition": "opacity .2s", "opacity": "1"});

        return;
    }

    // Otherwise, create the table head
    response.head[0] = "Terms";
    for(cell of response.head){
        let element = $(`<h3 class="tokenize-cell"></h3>`).appendTo("#table-head");
        element.text(cell);
    }

    // Create the table body
    for(row of response.data){
        let row_element = $(`<div class="tokenize-row"></div>`).appendTo(table_body);

        for(cell of row){
            let element = $(`<h3 class="tokenize-cell"></h3>`).appendTo(row_element);
            element.text(cell);
        }
    }

    // Fade in the table data
    $("#table-data").css({"transition": "opacity .2s", "opacity": "1"});
}


/**
 * Registers callbacks for each of the table buttons.
 */
function register_table_button_callbacks(){

    // Get the page number element
    let page_number_element = $("#page-number");

    // Rows per page
    $("input[type=radio][name=rows-per-page]").change(
        function(){ create_table(true); });

    // Search bar
    $("#search-input").on("input", function(){ create_table(true); });

    // Page number input
    $(page_number_element).on("input", function(){
        if(parse_page_number()) create_table();
    });

    // Previous button
    $("#previous-button").click(function(){
        page_number_element.val(parseInt(page_number_element.val())-1);
        create_table();
    });

    // Next button
    $("#next-button").click(function(){
        page_number_element.val(parseInt(page_number_element.val())+1);
        create_table();
    });
}

/**
 * Parses the page number input.
 * @returns {boolean}: Whether the page number was changed to a new valid value.
 */
function parse_page_number(){

    // Parse the page number
    let page_number_element = $("#page-number");
    page_number = parseInt(page_number_element.val());

    // Check that the input is valid
    if(isNaN(page_number)){
        page_number_element.val("");
        return false;
    }

    // Clamp the page number
    page_number = Math.max(1, Math.min(page_count, page_number));

    // Synchronize the displayed value
    page_number_element.val(page_number);

    // Return whether the page number was updated
    return page_number !== previous_page_number;
}
