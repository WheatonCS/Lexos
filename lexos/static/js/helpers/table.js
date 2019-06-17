/**
 * Creates a table.
 * @param {string} parent_element_query: The query for the table's parent
 *      element.
 * @param {string[][]} data: The data to display.
 * @param {string} head: The column labels.
 * @param {string} title: The title.
 */
function create_table(parent_element_query, data, head = "", title = ""){

    // Create the layout
    let table_element = $(`
        <div class="hidden lexos-table">
            <h3 class="lexos-table-head"></h3>
            <div class="lexos-table-body"></div>
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
