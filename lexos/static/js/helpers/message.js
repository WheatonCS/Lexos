const message_duration = 5000
var message_timeout

/**
 * Displays a message.
 * @param {string} message The message to display.
 * @returns {void}
 */
async function show_message (message) {
  // If the element already exists, update its message
  let existing_message_element = $('#message')
  if (existing_message_element.length) {
    existing_message_element.find('.message-text').html(message)
    reset_message_timeout()
    return
  }

  // Otherwise, create the message
  let message_element =
  $(`
    <div id="message">
      <span class="message-text">${message}</span>
    </div>
  `)

  // Remove the message after a set duration
  reset_message_timeout()

  // Append and fade in the message
  $('#main-grid').append(message_element)
  setTimeout(() => message_element.css('opacity', '1'), 33)
}

/**
 * Resets the message's timeout.
 * @returns {void}
 */
function reset_message_timeout () {
  clearTimeout(message_timeout)
  message_timeout = setTimeout(remove_message, message_duration)
}

/**
 * Removes the message if it exists.
 * @returns {void}
 */
async function remove_message () {
  let existing_message_element = $('#message')

  if (existing_message_element.length) {
    clearTimeout(message_timeout)
    existing_message_element.css('opacity', '0')
    setTimeout(existing_message_element.remove, 500)
  }
}
