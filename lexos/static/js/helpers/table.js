/**
 * Creates a table.
 * @param {string} parent_element_query: The query for the table's parent
 *      element.
 * @param {string[][]} data: The data to display.
 * @param {string[]} head: The column labels.
 * @param {string} title: The title.
 * @param {function} head_cell_click_callback: The function to call when a
 *      head cell is clicked.
 * @param {number} selected_head_cell_id: The ID of the selected head cell.
 */
function create_table(parent_element_query, data, head = [], title = '',
    head_cell_click_callback = null, selected_head_cell_id = 0){

    // Create the layout
    let table_element = $(`
        <div class="hidden lexos-table">
            <h3 class="lexos-table-head"></h3>
            <div class="lexos-table-body firefox-hidden-scrollbar"></div>
        </div>
    `).appendTo(parent_element_query);

    let table_head_element = table_element.find(".lexos-table-head");
    let table_body_element = table_element.find(".lexos-table-body");

    // Create the title
    if(title !== ""){
        table_element.css("grid-template-rows",
            "min-content min-content 1fr");
        $(`<h3 class="lexos-table-title">${title}</h3>`)
            .prependTo(table_element);
    }

    // For each head cell...
    for(const cell of head){

        // Create the cell element and append it to the table head element
        let cell_element = $(`<h3 class="lexos-table-head-cell"></h3>`)
            .appendTo(table_head_element);

        // Set the cell element's text
        cell_element.text(cell);
    }

    // If a head cell click callback was provided, initialize the selectable
    // head cells
    if(head_cell_click_callback) initialize_selectable_head_cells(
        head_cell_click_callback, selected_head_cell_id);

    // For each row...
    for(const row of data){

        // Create the row element and append it to the table element
        let row_element = $(`<div class="lexos-table-row"></div>`)
            .appendTo(table_body_element);

        // For each cell...
        for(const cell of row){

            // Create the cell element and append it to the row element
            let cell_element = $(`<h3 class="lexos-table-cell"></h3>`)
                .appendTo(row_element);

            // Set the cell element's text
            cell_element.text(cell);
        }
    }
}

/**
 * Initialize the selectable head cells.
 * @param {function} head_cell_click_callback: The function to call when a
 *      head cell is clicked.
 * @param {number} selected_head_cell_id: The ID of the selected head cell.
 */
function initialize_selectable_head_cells(
    head_cell_click_callback, selected_head_cell_id){

    // Assign IDs to each head cell
    let id = 0;
    let head_cell_elements = $(".lexos-table-head-cell");
    head_cell_elements.each(function(){ $(this).attr("id", id++); });

    // Apply the "selected-cell" class to the head cell of the
    // selected column
    $(`.lexos-table-head #${selected_head_cell_id}`).addClass("selected-cell");

    // If a head cell is clicked...
    head_cell_elements.click(function(){

        // Get the ID of the selected row
        selected_head_cell_id = $(this).attr("id");

        // Remove the "selected-cell" class from all head cells
        $(".lexos-table-head-cell").each(function(){
            $(this).removeClass("selected-cell");
        });

        // Apply the "selected-cell" class to the head cell of the
        // selected column
        $(`.lexos-table-head #${selected_head_cell_id}`)
            .addClass("selected-cell");

        // Call the callback
        head_cell_click_callback(selected_head_cell_id);
    });
}
