let page_count = 1;
let reset_page_number = false;

$(function(){
    create_table();
    register_table_button_callbacks();
})


/**
 * Creates the table.
 */
function create_table(){

    // Clamp the page number
    let page_number_element = $("#page-number");
    let page_number = parseInt(page_number_element.val());
    page_number = Math.max(1, Math.min(page_count, page_number));

    // Reset the page number if necessary
    if(reset_page_number){
        page_number = 1;
        reset_page_number = false;
    }
    page_number_element.val(page_number);

    // Send the request
    $.ajax({
        type: "POST",
        url: "tokenizer/get-table",
        processData: false,
        contentType: false,
        data: new FormData($("form")[0])
    }).done(get_table_callback);
}


/**
 * Creates the table.
 *
 * @param {string} response: The response from the "tokenizer/get-table" request.
 */
function get_table_callback(response){
    response = JSON.parse(response);

    // Clear the table
    let table_head = $("#table-head").empty();
    let table_body = $("#table-body").empty();

    // Set the page count
    page_count = parseInt(response.pages);
    $("#page-count").text(page_count);

    // If there are no rows, display "no data" text
    if(response.data.length === 0){
        $(`
            <div id="no-data-text-container" class="centerer">
                <h3 id="no-data-text">No Data</h3>
            </div>
        `).appendTo(table_body);
        return;
    }

    // Otherwise, create the table head
    response.head[0] = "Terms";
    for(cell of response.head){
        let element = $(`<h3 class="tokenizer-cell"></h3>`).appendTo(table_head);
        element.text(cell);
    }

    // Create the table body
    for(row of response.data){
        let row_element = $(`<div class="tokenizer-row"></div>`).appendTo(table_body);

        for(cell of row){
            let element = $(`<h3 class="tokenizer-cell"></h3>`).appendTo(row_element);
            element.text(cell);
        }
    }
}


/**
 * Registers callbacks for each of the table buttons.
 */
function register_table_button_callbacks(){

    // Get the page number element
    let page_number_element = $("#page-number");

    // Generate button
    $("#generate-button").click(function(){
        page_number_element.val(1);
        create_table();
    });

    // Search bar
    $("#search-input").on("input", function(){ reset_page_number = true; });

    // Rows per page
    $("input[type=radio][name=rows-per-page]").change(function(){
        reset_page_number = true;
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

    // First button
    $("#first-button").click(function(){
        page_number_element.val(1);
        create_table();
    });

    // Last button
    $("#last-button").click(function(){
        page_number_element.val(page_count);
        create_table();
    });
}
