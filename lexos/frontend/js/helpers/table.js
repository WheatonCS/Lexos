/**
 * Table class.
 */
class Table {
  /**
   * Creates a basic table.
   * @param {string} parent_element_query The query for the table's parent element.
   * @param {string[]} data The data to display.
   * @param {string[]} head The column labels.
   * @param {string} title The title.
   * @param {string} csv The CSV data to send when the "Download" button is clicked.
   * @returns {void}
   */
  static create_basic_table (parent_element_query, data, head = [], title = '', csv = '') {
    // Create the layout
    let table_element = $(`
            <div class="hidden lexos-table">
                <div class="lexos-table-top"></div>
                <div class="basic-lexos-table-content">
                    <div class="lexos-table-body firefox-hidden-scrollbar"></div>
                </div>
            </div>
        `).appendTo(parent_element_query)

    let table_top_element = table_element.find('.lexos-table-top')
    let table_body_element = table_element.find('.lexos-table-body')
    let table_content_element = table_element.find('.lexos-table-content')

    // Create the title
    if (title !== '') {
      $(`<h3 class="lexos-table-title">${title}</h3>`)
        .prependTo(table_top_element)
    }

    // Create the "Download" button
    if (csv !== '') {
      $(`<span class=button>Download</span>`)
        .appendTo(table_top_element)
        .click(function () { download(csv, `${title}-table.csv`) })
    }

    // If there is no table top data, remove the element
    if (title === '' && csv === '') table_top_element.remove()

    // For each head cell...
    for (const cell of head) {
      // Create the cell element and append it to the table head element
      let cell_element = $(`
                <h3 class="lexos-table-head">
                    <h3 class="lexos-table-head-cell"></h3>
                </h3>
            `)
        .appendTo(table_content_element)

      // Set the cell element's text
      cell_element.text(cell)
    }

    // If there is no head, increase the body size
    if (!head.length) table_body_element.css('height', '100%')

    // For each row...
    for (const row of data) {
      // Create the row element and append it to the table element
      let row_element = $(`<div class="lexos-table-row"></div>`)
        .appendTo(table_body_element)

      // For each cell...
      for (const cell of row) {
        // Create the cell element and append it to the row element
        let cell_element = $(`<h3 class="lexos-table-cell"></h3>`)
          .appendTo(row_element)

        // Set the cell element's text
        cell_element.text(cell)
      }
    }
  }

  /**
   * Initializes the table.
   * @param {string} name The name of the table.
   * @param {string} request_url The URL to send the request for table data to.
   * @param {string} parent_element_query The query for the table's parent element.
   * @param {string} title The text to display on the table's title.
   * @param {function} validation_callback The validation function to call
   *   before generating the table.
   * @param {function} completion_callback The function to call after table
   *   generation has completed.
   * @param {boolean} generate_button Whether to give the table a generate button.
   * @param {boolean} download_button Whether to give the table a download button.
   * @param {boolean} tooltip Whether to display a tooltip button.
   * @param {boolean} sortable Whether the table is sortable.
   * @param {boolean} backend_sort Whether the table is to be sorted in the
   *   backend or the frontend.
   * @param {boolean} searchable Whether the table is searchable.
   * @param {boolean} paginated:Whether the table has pages.
   */
  constructor (name, request_url, parent_element_query, title = '',
    validation_callback = null, completion_callback = null,
    generate_button = false, download_button = false, tooltip = false,
    sortable = false, backend_sort = false, searchable = false,
    paginated = false) {
    // Initialize the members
    this.name = name
    this.request_url = request_url
    this.parent_element_query = parent_element_query
    this.title = title
    this.validation_callback = validation_callback
    this.completion_callback = completion_callback
    this.generate_button = generate_button
    this.download_button = download_button
    this.tooltip = tooltip
    this.sortable = sortable
    this.backend_sort = backend_sort
    this.searchable = searchable
    this.paginated = paginated

    this.selected_column_id = '0'
    this.page_count = 1
    this.current_page = 1
    this.csv = ''

    // Create the table layout
    this._create_layout()

    // Initialize the table's buttons
    this._initialize_buttons()

    // Show the table
    this.table_element.removeClass('hidden')
  }

  /**
   * Sends a request for the table data and creates the table.
   * @param {boolean} display Whether to display the loading overlay.
   * @returns {void}
   */
  create (display = true) {
    // Validate the inputs
    if (this.validation_callback && !this.validation_callback(true)) return
    this._validate_inputs()
    if (this.paginated) this.current_page = this.page_number_element.val()

    // Remove any error messages
    remove_errors()

    // Display the loading overlay
    if (display) {
      start_loading(`#${this.name}-table-content`,
        `#${this.name}-table-generate-button,
          #${this.name}-table-download-button,
          #${this.name}-table-previous-button,
          #${this.name}-table-next-button`)
    }

    // Send the request for data
    let table = this
    return send_ajax_form_request(this.request_url)

      // Always call the completion callback
      .always(function (response) {
        table._finish_loading()
        if (table.completion_callback) { table.completion_callback(response) }
      })

      // If the request was successful...
      .done(function (response) {
        // Check for errors
        if (response.hasOwnProperty('error')) {
          error(response.error)
          add_text_overlay(`#${table.name}-table-content`, 'Loading Failed')
          return
        }

        // Update the CSV
        table.csv = response[`${table.name}-table-csv`]

        // If a table display update is undesired, return
        if (!display) return

        // Update the page count and number
        table.page_count = response[`${table.name}-table-page-count`]
        $(`#${table.name}-table-page-count`).text(table.page_count)
        table._validate_inputs()

        // If data was returned, display it
        if (response[`${table.name}-table-body`].length) {
          table.display(response[`${table.name}-table-body`], response[`${table.name}-table-head`])

        // Otherwise, if no data was returned, display "No Results"
        // text
        } else {
          add_text_overlay(`#${table.name}-table-content`,
            'No Results')
        }
      })

      // If the request failed, display an error
      .fail(function () {
        error('Failed to retrieve the table data.')
        add_text_overlay(`#${table.name}-table-content`, 'Loading Failed')
      })
  }

  /**
   * Creates the table head and body.
   * @param {string[]} body The data to display.
   * @param {string[]} head The column labels.
   * @returns {void}
   * @private
   */
  display (body, head = []) {
    // Create the head and body elements
    $(`
        <h3 id="${this.name}-table-head" class="lexos-table-head"></h3>
        <div id="${this.name}-table-body" class="lexos-table-body firefox-hidden-scrollbar"></div>
    `).appendTo($(`#${this.name}-table-content`))

    this.body = body
    let table_head_element = $(`#${this.name}-table-head`)
    let table_body_element = $(`#${this.name}-table-body`)

    // Hide the head and body
    table_head_element.addClass('hidden')
    table_body_element.addClass('hidden')

    // For each head cell...
    for (const cell of head) {
      // Create the cell element and append it to the table head element
      let cell_element = $(`<h3 class="lexos-table-head-cell"></h3>`)
        .appendTo(table_head_element)

      // Set the cell element's text
      cell_element.text(cell)
    }

    // If the table is sortable, make the head cells selectable
    if (this.sortable) this._initialize_head_cells()

    // For each row...
    for (const row of body) {
      // Create the row element and append it to the table element
      let row_element = $(`<div class="lexos-table-row"></div>`)
        .appendTo(table_body_element)

      // For each cell...
      for (const cell of row) {
        // Create the cell element and append it to the row element
        let cell_element = $(`<h3 class="lexos-table-cell"></h3>`)
          .appendTo(row_element)

        // Set the cell element's text
        cell_element.text(cell)
      }
    }

    // Remove the loading overlay, show the table content, and
    // enable the buttons
    this._finish_loading()
  }

  /**
   * Validates the table's inputs.
   * @returns {void}
   * @private
   */
  _validate_inputs () {
    // If the table is not paginated, return
    if (!this.paginated) return

    // Otherwise, check that the page number input is a number
    let page_number = this.page_number_element.val()
    let parsed_value = +page_number
    if (!page_number || isNaN(parsed_value)) page_number = 1

    // Check that page number input is within bounds
    else if (page_number < 1) page_number = 1
    else if (page_number > this.page_count) page_number = this.page_count

    // Assign the validated page number to the element
    this.page_number_element.val(page_number)
  }

  /**
   * Creates the layout of the table.
   * @returns {void}
   * @private
   */
  _create_layout () {
    // Create the layout
    this.table_element = $(`
      <div id="${this.name}-table" class="hidden lexos-table">
        <div class="lexos-table-top"></div>
        <div id="${this.name}-table-content" class="lexos-table-content">
            <h3 class="centerer">No Results</h3>
        </div>
        <input name="${this.name}_table_selected_column" value="0" type="hidden">
      </div>
    `).appendTo(this.parent_element_query)

    let table_top_element = this.table_element.find('.lexos-table-top')

    // If there is a title, create the title
    if (this.title !== '') {
      $(`<h3 class="lexos-table-title">${this.title}</h3>`)
        .appendTo(table_top_element)
    }

    // If the table is searchable, create the search input
    if (this.searchable) {
      $(`
        <div>
          <label for="${this.name}_table_search_input">Search: </label><input id="${this.name}_table_search_input" name="${this.name}_table_search_input" type="text" spellcheck="false" autocomplete="off"></label>
        </div>
      `).appendTo(table_top_element)
    }

    // If the table is paginated, create the row count option
    if (this.paginated) {
      $(`
        <fieldset>
          <div class="table-top-radio-option">
            <legend>Rows:</legend>
            <label><input name="${this.name}_table_row_count" value="10" type="radio" checked><span></span>10</label>
            <label><input name="${this.name}_table_row_count" value="50" type="radio"><span></span>50</label>
            <label><input name="${this.name}_table_row_count" value="100" type="radio"><span></span>100</label>
          </div>
        </fieldset>
      `).appendTo(table_top_element)
    }

    // If the table is sortable, create the sort direction option
    if (this.sortable) {
      $(`
        <fieldset>
          <div id="sort-radio-option" class="table-top-radio-option">
          <legend>Order:</legend>
          <label><input name="${this.name}_table_sort_mode" value="Ascending" type="radio" checked><span></span>Ascending</label>
          <label><input name="${this.name}_table_sort_mode" value="Descending" type="radio"><span></span>Descending</label>
          </div>
        </fieldset>
      `).appendTo(table_top_element)
    }

    // If the table needs a button, create the button section
    let button_section_element
    if (this.download_button || this.generate_button || this.tooltip) {
      button_section_element = $(`<div id="table-button-section" class="lexos-table-buttons"></div>`)
        .appendTo(table_top_element)
    }

    // If the table needs a generate button, create one
    if (this.generate_button) {
      $(`
        <span id="${this.name}-table-generate-button" class="disabled important-button">Generate</span>
      `).appendTo(button_section_element)
    }

    // If the table needs a download button, create one
    if (this.download_button) {
      $(`
        <span id="${this.name}-table-download-button" class="disabled button">Download</span>
      `).appendTo(button_section_element)
    }

    // If the table needs a tooltip button, create one
    if (this.tooltip) {
      $(`
        <span id="${this.name}-table-tooltip-button" class="tooltip-button">?</span>
      `).appendTo(button_section_element)
    }

    // If the table is paginated, create the page navigation buttons
    if (this.paginated) {
      $(`
        <div class="lexos-table-bottom">
            <div>
                <label for="${this.name}_table_page_number">Page</label><input id="${this.name}_table_page_number" name="${this.name}_table_page_number" type="text" spellcheck="false" autocomplete="off" value="1">
                <h3>of </h3>
                <h3 id="${this.name}-table-page-count">1</h3>
            </div>
            <div class="lexos-table-navigation-buttons">
                <span id="${this.name}-table-previous-button" class="disabled button">Previous</span>
                <span id="${this.name}-table-next-button" class="disabled button">Next</span>
            </div>
        </div>
      `).appendTo(this.table_element)

      this.page_number_element =
        $(`input[name="${this.name}_table_page_number"]`)
    }
  }

  /**
     * Assigns callbacks to the table's buttons.
     * @returns {void}
     * @private
     */
  _initialize_buttons () {
    let table = this
    $(`#${this.name}-table-generate-button`).click(function () {
      table.create()
    })

    $(`#${this.name}-table-download-button`).click(function () {
      download(table.csv, `${table.name}-table.csv`)
    })

    $(`#${this.name}-table-previous-button`).click(function () {
      table._change_page(false)
    })

    $(`#${this.name}-table-next-button`).click(function () {
      table._change_page(true)
    })
  }

  /**
   * Increments or decrements the page number and creates the table.
   * @param {boolean} next Whether to go to the next or previous page.
   * @returns {void}
   * @private
   */
  _change_page (next) {
    this._validate_inputs()
    this.page_number_element.val(parseInt(
      this.page_number_element.val()) + (next ? 1 : -1))
    this._validate_inputs()
    if (this.page_number_element.val() !== this.current_page) this.create()
  }

  /**
   * Initializes the table's head cells to be selectable.
   * @returns {void}
   * @private
   */
  _initialize_head_cells () {
    // Assign IDs to each head cell
    let id = 0
    let head_cell_elements =
            $(`#${this.name}-table .lexos-table-head-cell`)
    head_cell_elements.each(function () { $(this).attr('id', id++) })

    // Apply the "selected-cell" class to the head cell of the
    // selected column
    $(`#${this.name}-table .lexos-table-head #${this.selected_column_id}`)
      .addClass('selected-cell')

    // If a head cell is clicked...
    let table = this
    head_cell_elements.click(function () {
      table._head_cell_click_callback($(this))
    })
  }

  /**
   * Applies the highlight to the selected cell and calls the cell selection callback.
   * @param {JQuery} element The clicked element.
   * @returns {void}
   * @private
   */
  _head_cell_click_callback (element) {
    // If the selection is the same, return
    if (element.attr('id') === this.selected_column_id) return

    // Otherwise, update the selected ID
    this.selected_column_id = element.attr('id')

    // Remove the "selected-cell" class from all head cells
    $(`#${this.name}-table .lexos-table-head-cell`).each(function () {
      $(this).removeClass('selected-cell')
    })

    // Apply the "selected-cell" class to the head cell of the
    // selected column
    $(`#${this.name}-table .lexos-table-head #${this.selected_column_id}`)
      .addClass('selected-cell')

    // Set the selected cell input
    $(`input[name="${this.name}_table_selected_column"]`)
      .val(this.selected_column_id)
  }

  /**
     * Remove the loading overlay, show the table content, and
     *  enable the buttons
     * @returns {void}
     * @private
     */
  _finish_loading () {
    finish_loading(`#${this.name}-table-content`,
      `#${this.name}-table-body, #${this.name}-table-head`,
      `#${this.name}-table-generate-button,
        #${this.name}-table-download-button,
        #${this.name}-table-previous-button,
        #${this.name}-table-next-button`)
  }
}
