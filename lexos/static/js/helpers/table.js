/**
 * Creates a table.
 * @param {string} parent_element_query: The query for the table's parent
 *      element.
 * @param {string} title: The title of the table.
 * @param {string[][]} data: The data for the table to display.
 */
function create_table(title, parent_element_query, data){

    // Create the table
    let table_element = $(`
        <div class="lexos-table">
            <h3 class="lexos-table-title"></h3>
            <div class="lexos-table-body"></div>
        </div>
    `).appendTo(parent_element_query);

    let table_body_element = table_element.find(".lexos-table-body");

    // Set the table title element to the HTML-escaped title
    table_element.find(".lexos-table-title").text(title);

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
