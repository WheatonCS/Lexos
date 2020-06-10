/**
 * Creates a preview for each active document.
 * @param {string} response: The response from the
 *     get-document-previews request.
 * @returns {void}
 */
function initialize_document_previews (response) {
  let previews = parse_json(response)

  // If there are no previews, display "No Active Documents" text
  if (!previews.length) {
    add_text_overlay('#previews', 'No Active Documents')
    return
  }

  // Create a preview for each active document
  for (const preview of previews) { create_document_preview(preview[2], preview[3]) }

  // Remove the loading overlay, fade in the previews, and enable the
  // buttons
  finish_document_previews_loading()
}

/**
 * Creates a document preview with the given name and text.
 * @param {string} preview_name The name of the document.
 * @param {string} preview_text The preview text.
 * @returns {void}
 */
function create_document_preview (preview_name, preview_text) {
  // Create the document preview
  let preview = $(`
        <div class="preview hidden">
            <h3 class="preview-name"></h3>
            <h3 class="preview-text"></h3>
        </div>
    `).appendTo('#previews')

  // HTML-escape the text and add it to the document preview
  preview.find('.preview-name').text(preview_name)
  preview.find('.preview-text').text(preview_text)
}

/**
 * Displays the loading overlay and disables the buttons.
 * @returns {void}
 */
function start_document_previews_loading () {
  start_loading('#previews')
  disable('#preview-button, #apply-button, #download-button')
}

/**
 * Removes the loading overlay, fades in the previews, and enables the buttons.
 * @returns {void}
 */
function finish_document_previews_loading () {
  // Remove the loading overlay and fade in the previews
  finish_loading('#previews', '.preview')

  // Enable the buttons
  $('#preview-button, #apply-button, #download-button')
    .removeClass('disabled')
}
