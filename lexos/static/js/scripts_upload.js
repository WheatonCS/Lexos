/**
 * Alias function.
 * @return {object} element id object.
 * @param {string} id - id of an html element.
 */
function $id (id) {
  return document.getElementById(id)
}

/**
 * Checks if the file type is valid.
 * @return {boolean} bool - true if file type is valid.
 * @param {string}  filename - name of the file.
 */
function AllowedFileType (filename) {
  const allowedFileTypes = ['txt', 'xml', 'html', 'sgml', 'lexos']
  // Get the file file extension
  let fileType = filename.split('.')[filename.split('.').length - 1]
  // Search uploaded file's extension to the list 'allowedFileTypes'
  // Return -1 if the file format is different from the list above
  return $.inArray(fileType, allowedFileTypes) > -1
}

/**
 * File Drag Hover.
 * @return {void}
 * @param {object} e - event.
 */
function fileDragHover (e) {
  e.stopPropagation()
  e.preventDefault()
  e.target.className = (e.type === 'dragover' ? 'hover' : '')
}

/**
 * @return {void}
 * @description { Set progress bar back to default.
  when a file is uploaded: bar changes to 'Complete'.
  After the upload it set the bar back to 'Ready for Files to Upload'.
 */
function resetProgressBar () {
  const progressBar = $('#progress-bar')
  const status = $('#status')
  progressBar.html('').css({'width': '0px'})
  progressBar.show()
  status.css('z-index', 50000)
  status.show()
}

/**
 * Upload and display file contents.
 * @return {void}
 * @param {object} file - file object.
 * @param {int} fileSize - size of the File uploaded.
 */
function UploadAndParseFile (file, fileSize) {
  let filename = file.name.replace(/ /g, '_')
  const status = $('#status-analyze')
  // Make the loading icon circle visible
  status.css({'visibility': 'visible'})

  if (AllowedFileType(file.name) && file.size <= fileSize) {
    if (file.size === 0) {
      $('#error-modal-message').html(`Cannot process blank file -- ${file.name}`)
      $('#error-modal').modal()
      status.css({'visibility': 'hidden'})
    } else {
      sendAjaxRequest(file, filename)
        .done(function () {
          let reader = new FileReader()
          reader.onload = function (e) {
            const template = $($('#file-preview-template').html())
            template.find('.file-name').html(filename)
            // Truncate the file name with css
            template.find('.file-name').css({
              'width': '90%',
              'margin': 'auto',
              'white-space': 'nowrap',
              'overflow': 'hidden',
              'text-overflow': 'ellipsis'
            })
            let fileType = ''
            if (file.type === '') {
              fileType = 'Lexos Workspace'
              template.find('.file-information').find('.file-type').html(fileType)
            } else {
              template.find('.file-information').find('.file-type').html(file.type)
              e.target.result.replace(/</g, '&lt;').replace(/>/g, '&gt;')
            }
            let fileSize = file.size
            if (fileSize < 1024) {
              template.find('.file-information').find('.file-size').html(`${file.size} bytes`)
            } else if (file.size < 1048576) {
              const fileSizeInKB = (file.size / 1024).toFixed(1)
              template.find('.file-information').find('.file-size').html(`${fileSizeInKB} KB`)
            } else {
              const fileSizeInMB = (file.size / 1024 / 1024).toFixed(1)
              template.find('.file-information').find('.file-size').html(`${fileSizeInMB} MB`)
            }
            $('#manage-previews').prepend(template)
          }
          reader.readAsText(file)
          $('#activeDocIcon').css('display', 'block')
          status.hide()
        })

        .fail(function (jqXHR, textStatus, errorThrown) {
          alert(`${textStatus} : ${errorThrown}`)
          status.css({'visibility': 'hidden'})
        })
        .always(function () {
          status.css({'visibility': 'hidden'})
        })
    }
  } else if (!AllowedFileType(file.name)) {
    $('#error-modal-message').html(`Upload for  ${filename}  failed.\n\nInvalid file type.`)
    $('#error-modal').modal()
    // These are to hide the loading icon.
    status.css({'visibility': 'hidden'})
    status.css({'opacity': '0'})
  } else {
    // These are to hide the loading icon.
    status.css({'visibility': 'hidden'})
    status.css({'opacity': '0'})
    const MAX_FILE_SIZE_INT = $('#MAX_FILE_SIZE_INT').val()
    const MAX_FILE_SIZE_UNITS = $('#MAX_FILE_SIZE_UNITS').val()
    $('#error-modal-message').html(`Upload for ${filename}  failed.\n\nFile bigger than
     ${MAX_FILE_SIZE_INT} ${MAX_FILE_SIZE_UNITS}B`)
    $('#error-modal').modal()
    // Without this, it puts a blue background on the progress bar.
    $('#progress').css('background', 'transparent')
  }
}

/**
 * @return {ajax} ajax data.
 * @param {object} file - file object.
 * @param {string} filename - name of the file.
 */
function sendAjaxRequest (file, filename) {
  return $.ajax({
    type: 'POST',
    url: document.URL,
    data: file,
    processData: false,
    async: false,
    contentType: file.type,
    headers: {'X-FILENAME': encodeURIComponent(filename)}
  })
}

/**
 * Drag and drop of files.
 * @return {void}
 * */
function Init () {
  const fileselect = $id('fileselect')
  const filedrag = $id('dragndrop')

  // File select
  fileselect.addEventListener('change', FileSelectHandler, false)

  // Is XHR2 available?
  let xhr = new XMLHttpRequest()
  if (xhr.upload) {
    // file drop
    filedrag.addEventListener('dragover', fileDragHover, false)
    filedrag.addEventListener('dragleave', fileDragHover, false)
    filedrag.addEventListener('drop', FileSelectHandler, false)
  }
}

/**
 * file selection.
 * @return {void}
 * @param {object} e - event.
 */
function FileSelectHandler (e) {
  const counter = $('#counter')
  // Value of the input tag so that it gets the number of active files
  let numberOfFileDone = parseInt(counter.val())
  // cancel event and hover styling
  fileDragHover(e)
  // fetch FileList object
  let files = e.target.files || e.dataTransfer.files
  // Total number of files uploaded.
  let totalFiles = files.length
  // Resets the progress bar to defualt message after a file upload.
  resetProgressBar()

  const progress = $('#progress')
  const progressBar = $('#progress-bar')

  // Process all File objects
  for (let f of files) {
    let added = 0

    if (f.size < $id('MAX_FILE_SIZE').value && AllowedFileType(f.name)) {
      numberOfFileDone += 1
      added = 1
    }
    let fileSize = $id('MAX_FILE_SIZE').value
    UploadAndParseFile(f, fileSize)
    // Loading progress bar.
    if (f.type === '') {
      progress.html('Loading Workspace')
    } else {
      let calculatedWidth = String(180 * numberOfFileDone / totalFiles) + 'px'
      progress.html(numberOfFileDone + 'of' + totalFiles).css('color', '#3498DB')

      progressBar.css({'width': calculatedWidth})
      if (numberOfFileDone / totalFiles > 0.5) {
        progress.css('color', '#FFF')
      }
      progressBarStatus(f, added)
      const faFolderOpen = $('.fa-folder-open-o')
      faFolderOpen[0].dataset.originalTitle = `You have ${numberOfFileDone} active document(s)`
      faFolderOpen.fadeIn(200)
    }
  }
  showProgress()
  // Convert the integer back to string and put it as a value in the input tag.
  let numActiveFile = numberOfFileDone.toString()
  counter.attr('value', numActiveFile)
  $('#status').delay(1200).hide(0)
}

/**
 * Displays the message on the 'progress' bar.
 * @return {void}
 */
function showProgress () {
  $('#status').css('z-index', 50000).show()
  $('#progress').html('Ready For Files To Upload').css('color', '#074178').delay(3000).show()
  $id('fileselect').value = ''
  // this allows the event to fire on "change" in chrome. the value property changing is the
  // normal trigger, for some reason firefox overwrote this with their own behavior.
}
/**
 * Changes the message on the progress bar according to the file.
 * if file valid: "Complete!" else: "Invalid File!"
 * @return {void}
 * @param {string} f - name of the file.
 * @param {int} added - 1 id file is added.
 */
function progressBarStatus (f, added) {
  if (added === 1 && f.size < $id('MAX_FILE_SIZE').value && f.size !== 0 && AllowedFileType(f.name)) {
    $('#progress-bar').html('Complete!').css({
      'color': '#FFF',
      'text-align': 'center',
      'width': '175px',
      'height': '20px'
    }).fadeOut(2000)
  } else {
    $('#progress-bar').html('Invalid File!').css({
      'color': '#FFF',
      'text-align': 'center',
      'width': '175px',
      'height': '20px'
    }).fadeOut(2000)
  }
}

$(function () {
  // Message for when you hover on the open folder icon on the top right.
  $('[data-toggle="tooltip"]').tooltip()
  $('#uploadbrowse').click(function () {
    $('#fileselect').click()
  })

  // Call initialization function
  if (window.File && window.FileList && window.FileReader) {
    Init()
  }
})
