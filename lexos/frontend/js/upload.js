let files = []

$(function () {
  // Redirect "Browse..." button clicks to the file selection input element
  // which will open an OS file selection window
  $('#browse-button').click(function () { $('#file-select-input').click() })

  // When the user finishes selecting files using the OS file selection
  // window, upload the selected files
  $('#file-select-input').change(upload_files)

  // Upload files dropped on the drag and drop section
  const drag_and_drop_section = $('#drag-and-drop-section')
  drag_and_drop_section.on('drop', upload_files)

  // Prevent the default drag and drop action of opening the file in the
  // browser
  $('body').on('dragover dragenter drop', drag_and_drop_intercept)
  drag_and_drop_section.on('dragover dragenter', drag_and_drop_intercept)

  // If the "Scrape" button is pressed...
  $('#scrape-button').click(scrape)

  // Highlight the drag and drop section when files are dragged over it
  initialize_drag_and_drop_section_highlighting()

  // Initialize the tooltips
  initialize_tooltips()

  // Initialize the walkthrough
  initialize_walkthrough(walkthrough)
})

/**
 * Performs scraping on the given URLs.
 * @returns {void}
 */
function scrape () {
  // Disable the "Scrape" button
  disable('#scrape-button')

  // Remove any existing errors
  remove_errors()

  // Send the scrape request
  send_ajax_request('/upload/scrape', $('#scrape-input').val())

    // Always enable the "Scrape" button
    .always(function () { enable('#scrape-button') })

    // If the request was successful, display the uploaded files in the
    // "Upload List" section.
    .done(function (response) {
      for (const file_name of response) {
        create_upload_preview(file_name)
          .find('.upload-preview-content').removeClass('disabled')
      }
    })

    // If the request failed, display an error.
    .fail(function () {
      error('Scraping failed.')
    })
}

/**
 * Uploads the files selected via the OS file selection window or drag and drop.
 * @param {event} event The event that triggered the callback.
 * @returns {void}
 */
function upload_files (event) {
  // Remove any existing error messages
  remove_errors()

  // For each selected file...
  for (let file of Object.values(event.target.files ||
        event.originalEvent.dataTransfer.files)) {
    // Validate the file
    if (!validate_file(file)) continue

    // Replace the file name's spaces with underscores
    file.name = file.name.replace(/ /g, '_')

    // Create the upload preview and add the progress element to the file
    // element
    file['upload_preview_element'] = create_upload_preview(file.name)

    // Add the file to the upload list
    files.unshift(file)
  }

  // Upload each file
  send_file_upload_requests()
}

/**
 * Validates the given file.
 * @param {any} file The file to validate.
 * @returns {boolean} Whether the file is valid.
 */
function validate_file (file) {
  // If the file exceeds the 256 MB size limit, display an error message
  // and return false
  if (file.size > 256000000) {
    error('One or more files exceeded the 256 MB size limit.')
    return false
  }

  // If the file is empty, display an error message and return false
  if (file.size <= 0) {
    error('One or more uploaded files were empty.')
    return false
  }

  // If the file is not of a supported type, display an error message and
  // return false
  if (!file_type_supported(file.name)) {
    error('One or more files were of an unsupported file type.')
    return false
  }

  return true
}

/**
 * Uploads the given file.
 * @returns {void}
 */
function send_file_upload_requests () {
  // Get the next file
  let file = files.pop()

  // If there are no more files to upload, display an upload complete message.
  if (!file) {
    show_message('All uploads have completed.')
    return
  }

  // Send a request to upload the file
  $.ajax({
    xhr: initialize_upload_progress_callback(file),
    type: 'POST',
    url: 'upload/add-document',
    data: file,
    processData: false,
    contentType: file.type,
    headers: {'file-name': encodeURIComponent(file.name)},
    success: function(data){
      console.log(data)
    }
  })

  // If the request is successful, call the "upload_success_callback()"
  // function and upload the next file in the list
    .done(function () { send_file_upload_requests() })

  // If the request failed, display an error
    .fail(function () {
      error('One or more files encountered errors during upload.')
    })
}

/**
 * Initializes the XHR file upload progress callback.
 * @param {any} file The file whose upload preview will be updated.
 * @returns {function(): Window.XMLHttpRequest} The XHR object.
 * @returns {void}
 */
function initialize_upload_progress_callback (file) {
  return function () {
    // Create the XHR object
    let xhr = $.ajaxSettings.xhr()

    // When upload progress has been made...
    xhr.upload.onprogress = function (event) {
      // Update the file's upload preview with the file's upload
      // progress
      let progress = event.loaded / event.total
      let progress_bar_element =
        file.upload_preview_element.find('.progress-bar')
          .css('width', `${progress * 100}%`)

      // If the upload has completed, increase the upload preview's
      // opacity
      if (progress >= 1) {
        progress_bar_element.css('opacity', '0')
        file.upload_preview_element.find('.upload-preview-content')
          .removeClass('disabled')
      }
    }

    return xhr
  }
}

/**
 * Checks if the file type is supported.
 * @param {string} filename: The name of the file to check.
 * @return {boolean} bool: Whether the file type is supported.
 */
function file_type_supported (filename) {
  const supported_file_types = ['txt', 'xml', 'html', 'sgml', 'lexos', 'docx']

  // Get the file's extension
  let fileType = filename.split('.')[filename.split('.').length - 1]

  // Return whether the file type is supported
  return $.inArray(fileType, supported_file_types) > -1
}

/**
 * Create an upload preview element.
 * @param {string} file_name The name of the file.
 * @returns {void}
 */
function create_upload_preview (file_name) {
  // Remove the "No Uploads" text if it exists
  $('#no-uploads-text').remove()

  // Update the "Active Document Count" element
  let active_documents_element = $('#active-document-count')
  let active_documents = parseInt(active_documents_element.text()) + 1
  active_documents_element.text(active_documents.toString())

  // Create the upload preview element
  let upload_preview_element = $(`
    <div id="preview-${active_documents}" class="hidden upload-preview">
      <h3 class="disabled upload-preview-content"></h3>
      <div class="progress-bar"></div>
    </div>
  `).appendTo('#upload-previews-grid')

  // Add the HTML-escaped file name to the upload preview element
  upload_preview_element.find('.upload-preview-content')
    .text(file_name)

    // Fade in the preview element
  fade_in(`#preview-${active_documents}`, 'var(--long-fade-duration)')

  // Return the upload preview element
  return upload_preview_element
}

/**
 * Intercepts file drag and drop events, preventing the default action of
 * opening the dropped file in the browser.
 * @param {Event} event The event that triggered the callback.
 * @returns {void}
 */
function drag_and_drop_intercept (event) {
  event.stopPropagation()
  event.preventDefault()
}

/**
 * Makes the drag and drop section highlighted when files are dragged over it.
 * @returns {void}
 */
function initialize_drag_and_drop_section_highlighting () {
  let drag_counter = 0
  const drag_and_drop_section = $('#drag-and-drop-section')

  drag_and_drop_section.on('dragenter', function () {
    ++drag_counter
    drag_and_drop_section.addClass('highlighted')
  })

  drag_and_drop_section.on('dragleave', function () {
    if (--drag_counter === 0) { drag_and_drop_section.removeClass('highlighted') }
  })

  drag_and_drop_section.on('drop', function () {
    drag_counter = 0
    drag_and_drop_section.removeClass('highlighted')
  })
}

/**
 * Initializes the tooltips.
 * @returns {void}
 */
function initialize_tooltips () {
  // "Upload"
  create_tooltip('#upload-tooltip-button', `Click the "Browse" button or
    drag and drop a file into the "Drag Files Here" section. The maximum
    file size is 250 MB, and the supported file types are: .txt, .html,
    .xml, .sgml, and .lexos.`)

  // "Scrape"
  create_tooltip('#scrape-tooltip-button', `Enter the URLs of websites you
    wish to extract text from. Separate each URL with a new line or a
    comma.`, true)

  // "Upload List"
  create_tooltip('#upload-list-tooltip-button', `All uploaded and scraped
    files will appear here. When uploading large files or many different
    files, you will see blue bars indicating upload progress. Wait for
    all files to finish uploading before proceeding.`, true)
}

/**
 * Initializes the walkthrough.
 * @returns {void}
 */
function walkthrough () {
  let intro = introJs()
  intro.setOptions({steps: [
    {
      element: '#lexos-dragon',
      intro: `Welcome to Lexos!<br><br>For a high contrast color scheme, click the dragon logo at the top left and
      select the Grey Light theme.`,
      position: 'right'
    },
    {
      element: '#upload-section',
      intro: `This is the Upload section. You can upload the files you
        want to work with here.`,
      position: 'right'
    },
    {
      element: '#browse-button',
      intro: `Click the "Browse..." button to select files to upload...`,
      position: 'right'
    },
    {
      element: '#drag-and-drop-section',
      intro: `...or drag and drop files here.`,
      position: 'top'
    },
    {
      element: '#scrape-section',
      intro: `The Scrape section extracts text from webpages for use in Lexos.`,
      position: 'bottom'
    },
    {
      element: '#scrape-input',
      intro: 'You can enter newline-separated URLs here.',
      position: 'bottom'
    },
    {
      element: '#scrape-button',
      intro: `When you have finished entering URLs, you can press the
        "Scrape" button to extract text from the webpages.`,
      position: 'bottom'
    },
    {
      element: '#upload-list',
      intro: `The names of successfully uploaded and scraped files
        will appear here.`,
      position: 'top'
    },
    {
      element: '#help-button',
      intro: `For a more in-depth look at this page, visit the Help section.`,
      position: 'bottom'
    },
    {
      element: '#manage-button',
      intro: `This concludes the Upload walkthrough! When you have
        finished uploading documents, try visiting the Manage page.
        You can click outside of this message box at any time to close
        the walkthrough.`,
      position: 'bottom'
    }
  ]})

  return intro
}
