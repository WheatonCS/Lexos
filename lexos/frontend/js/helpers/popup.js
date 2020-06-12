/**
 * Creates a popup.
 * @param {string} title The title to display on the popup.
 * @returns {jQuery} The popup element.
 */
function create_popup (title) {
  // Create the popup element
  let id = get_id(title)
  let popup_container_element = $(`
      <div id="${id}-popup" class="popup-container">
        <div class="popup">
          <div class="vertical-splitter">
            <h3 class="title">${title}</h3>
            <h3 class="right-justified button popup-close-button">Close</h3>
          </div>
          <div class="popup-content"></div>
        </div>
      </div>
    `).appendTo('form')

  // Fade in the popup
  fade_in(`#${id}-popup`)

  // Close the popup when the "Close" button or the background is clicked
  $(`#${id}-popup .popup-close-button`).click(close_popup)
  popup_container_element.click(close_popup)

  // Prevent click events from propagating to the popup container and thus
  // closing the popup undesirably
  $(`#${id}-popup .popup`).click(
    function (event) { event.stopPropagation() })

  return popup_container_element
}

/**
 * Fades out and removes any existing popups.
 * @returns {void}
 */
function close_popup () {
  let popup = $('.popup-container').css('opacity', '0')
  setTimeout(function () { popup.remove() }, 500)
}

/**
 * Creates a popup with an "OK" button.
 * @param {string} title The title to display on the popup.
 * @returns {jQuery} The popup element.
 */
function create_ok_popup (title) {
  let popup_container_element = create_popup(title)

  $(`<span class="popup-ok-button button">OK</span>`)
    .appendTo(popup_container_element.find('.popup'))

  return popup_container_element
}

/**
 * Creates a popup with a text input and "OK" button.
 * @param {string} title The popup element.
 * @returns {jQuery} The popup element.
 */
function create_text_input_popup (title) {
  let popup_container_element = create_ok_popup(title)

  $(`
        <input class="popup-input" type="text" spellcheck="false" autocomplete="off">
    `).appendTo(popup_container_element.find('.popup-content'))

  return popup_container_element
}

/**
 * Creates a popup containing radio button options.
 * @param {string} title The title to display on the popup.
 * @param {string} radio_buttons_name The name of the radio buttons.
 * @param {string} display_element_query The query for the element to display
 *      the selected option's text on.
 * @param {string} input_element_query The query for the input element whose
 *      value  will be set to the selected option.
 * @param {string[]} options The text of each radio button.
 * @param {string[]} values The values of each radio button.
 * @returns {void}
 */
function create_radio_options_popup (title, radio_buttons_name,
  display_element_query, input_element_query, options, values = []) {
  // Get the currently set option from the input element
  let input_element = $(input_element_query)
  let set_option = input_element.val()

  // Display the popup
  return display_radio_options_popup(
    title, radio_buttons_name, set_option, options, values,

    // If the "OK" button is pressed, update the elements and close
    // the popup
    function (selected_element_value, selected_element_name) {
      input_element.val(selected_element_value)
      $(display_element_query).text(selected_element_name)
      close_popup()
    })
}

/**
 * Creates a popup containing radio button options.
 * @param {string} title The title to display on the popup.
 * @param {string} radio_buttons_name The name of the radio buttons.
 * @param {string} set_option The value of the currently set option.
 * @param {string[]} options The text of each radio button.
 * @param {string[]} values The values of each radio button.
 * @param {function} callback The callback to call when a selection has been made.
 * @returns {void}
 */
function display_radio_options_popup (title,
  radio_buttons_name, set_option, options, values, callback) {
  // If no values were provided, set them to the options
  if (values.length !== options.length) values = options

  // Create the popup
  let popup_container_element =
        create_popup(title).addClass('radio-button-popup')
  let popup_element = popup_container_element.find('.popup')
  let popup_content_element = popup_container_element.find('.popup-content')

  // For each option...
  for (let i = 0; i < options.length; ++i) {
    // Create the radio button
    let element = $(`
            <div><label><input type="radio" name="${radio_buttons_name}" value="${values[i]}"><span></span>${options[i]}</label></div>
        `).appendTo(popup_content_element)

    // Check the currently set option's radio button
    if (set_option === values[i]) { element.find('input').prop('checked', true) }
  }

  // Create the "OK" buttons
  $(`<span class="popup-ok-button button">OK</span>`)
    .appendTo(popup_element)

  // If the "OK" button is pressed, call the callback
    .click(function () {
      let selected_element =
                $(`input[name="${radio_buttons_name}"]:checked`)
      callback(selected_element.val(),
        selected_element.closest('div').text().trim())
    })

  return popup_container_element
}
