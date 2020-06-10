let table

$(function () {
  // Initialize validation
  initialize_validation(validate_analyze_inputs)

  // Initialize the table
  table = new Table('tokenizer', 'tokenize/table', '#table-section', '',
    validate_analyze_inputs, null, true, false, false, true, true, true, true)

  // Initialize the download button
  initialize_download_button()

  // Create the table
  initialize()

  // Initialize the "Orientation" tooltip
  create_tooltip('#orientation-tooltip-button', `This option will not be
    represented in the table below, but will be applied to the file sent
    when the "Download" button is clicked.`)

  // Initialize the analyze tooltips
  initialize_analyze_tooltips()

  // Initialize the walkthrough
  initialize_walkthrough(walkthrough)
})

/**
 * Initializes the download button.
 * @returns {void}
 */
function initialize_download_button () {
  // Create the download button
  let download_button = $(`<span class="button">Download</span>`)
    .appendTo(table.table_element.find('.lexos-table-buttons'))

  // If the download button is clicked...
  download_button.click(function () {
    // Create the popup
    let popup_container_element = create_ok_popup('Download')

    $(`
      <label><input name="csv_orientation" value="Documents as Rows" type="radio" checked><span></span>Documents as Rows</label><br>
      <label><input name="csv_orientation" value="Documents as Columns" type="radio"><span></span>Documents as Columns</label>
    `).appendTo(popup_container_element.find('.popup-content'))

    // If the popup's "OK" button is clicked...
    $(popup_container_element.find('.popup-ok-button')).click(function () {
      // Send a request to create the table with the selected orientation
      table.create(false)

        // If the request is successful, download the table and close
        // the popup
        .done(function () {
          download(table.csv, `${table.name}-table.csv`)
          close_popup()
        })
    })
  })
}

/**
 * Creates the token table.
 * @returns {void}
 */
function initialize () {
  // If there are no active documents, display "No Active Documents"
  // text and return
  if (!active_document_count) {
    add_text_overlay('.lexos-table-content', 'No Active Documents')
    return
  }

  // Create the token table
  table.create()
}

/**
 * Initializes the walkthrough.
 * @returns {void}
 */
function walkthrough () {
  let intro = introJs()
  intro.setOptions({steps: [
    {
      intro: `Welcome to Tokenize!`,
      position: 'top'
    },
    {
      element: '#tokenize-section',
      intro: `Tokenize determines how terms are counted when generating data.`,
      position: 'top'
    },
    {
      element: '#normalize-section',
      intro: `Normalize determines if and how term totals are weighted.`,
      position: 'top'
    },
    {
      element: '#cull-section',
      intro: `Cull limits the number of terms used to generate data and
        is optional.`,
      position: 'top'
    },
    {
      element: '#table-section',
      intro: `Here is your generated data table from the options
        selected above.`,
      position: 'top'
    },
    {
      element: '#sort-radio-option',
      intro: `You can sort your data table with these options, and by
        clicking column headers on the data table.`,
      position: 'top'
    },
    {
      element: '#table-button-section',
      intro: `Here you can generate a data table. You can also choose to
        download the data table as a CSV file.`,
      position: 'top'
    },
    {
      element: '#help-button',
      intro: `For a more in-depth look at this page, visit the Help section.`,
      position: 'bottom'
    },
    {
      intro: `This concludes the Tokenize walkthrough!`,
      position: 'top'
    }
  ]})

  return intro
}
