$(function () {
  /*message for when you hover on the open folder icon on the top right*/
  $('[data-toggle="tooltip"]').tooltip()
  $('#uploadbrowse').click(function () {
    $('#fileselect').click()
  })

  //alias function
  function $id(id) {
    return document.getElementById(id)
  }

  let numberOfFileDone = parseInt($('.fa-folder-open-o')[0].id)
  // file selection
  function FileSelectHandler(e) {
    // cancel event and hover styling
    fileDragHover(e)
    // fetch FileList object
    let files = e.target.files || e.dataTransfer.files
    // total number of files uploaded
    let totalFiles = files.length
    //resets the progress bar to defualt message after a file upload
    resetProgressBar()

    const progress = $('#progress'),
          progressBar = $('#progress-bar')

    //Process all File objects
    for (let i = 0, f; f = files[i]; i++) {
      let added = 0
      if (f.size < $id('MAX_FILE_SIZE').value) {
        numberOfFileDone += 1
        added = 1
      }
      let fileSize = $id('MAX_FILE_SIZE').value
      UploadAndParseFile(f,fileSize)
      // loading progress bar
      if (f.type === '') {
        progress.html('Loading Workspace')
      }
      else {
        let calculatedWidth = String(180 * numberOfFileDone / totalFiles) + 'px'
        progress.html(numberOfFileDone + ' of ' + totalFiles).css('color', '#3498DB')
        progressBar.css({ 'width': calculatedWidth })
        if (numberOfFileDone / totalFiles > 0.5) {
          progress.css('color', '#FFF')
        }
        if (added === 1) {
          progressBar.html('Complete!').css({ 'color': '#FFF', 'text-align': 'center', 'width': '175px', 'height': '20px' }).fadeOut(2000)
          const faFolderOpen = $('.fa-folder-open-o')
          faFolderOpen[0].dataset.originalTitle = 'You have ' + numberOfFileDone + ' active document(s)'
          faFolderOpen.fadeIn(200)
          $('#status').hide()
        }
      }
    }
    progress.html('Ready For Files To Upload').css('color', '#074178').delay(3000).show()
    $id('fileselect').value = '' // this allows the event to fire on "change" in chrome. the value property changing is the
    // normal trigger, for some reason firefox overwrote this with their own behavior.
  }

  // initialize
  function Init() {
    let fileselect = $id('fileselect'),
        filedrag = $id('dragndrop')

    // file select
    fileselect.addEventListener('change', FileSelectHandler, false)

    // is XHR2 available?
    let xhr = new XMLHttpRequest()
    if (xhr.upload) {
      // file drop
      filedrag.addEventListener('dragover', fileDragHover, false)
      filedrag.addEventListener('dragleave', fileDragHover, false)
      filedrag.addEventListener('drop', FileSelectHandler, false)
    }
  }

  //Call initialization function
  if (window.File && window.FileList && window.FileReader) {
    Init()
  }
})


/**
 * @return {boolean}
 */
//Checks the type of file uploaded.
function AllowedFileType(filename) {
  const allowedFileTypes = ['txt', 'xml', 'html', 'sgml', 'lexos']
  //Get the file file extension
  let fileType = filename.split('.')[filename.split('.').length - 1]
  //search uploaded file's extension to the list 'allowedFileTypes'
  //Return -1 if the file format is different from the list above
  return $.inArray(fileType, allowedFileTypes) > -1;
}

//File drag hover
function fileDragHover(e) {
  e.stopPropagation()
  e.preventDefault()
  e.target.className = (e.type === 'dragover' ? 'hover' : '')
}


/*Set progress bar back to default.
  when a file is uploaded: bar changes to 'Complete'
  After the upload it set the bar back to 'Ready for Files to Upload'*/
function resetProgressBar() {
  const progressBar = $('#progress-bar')
  const status = $('#status')
  progressBar.html('').css({'width': '0px'})
  progressBar.show()
  status.css('z-index', 50000)
  status.show()
}


// upload and display file contents
function UploadAndParseFile(file,fileSize) {
    let filename = file.name.replace(/ /g, '_')

    if (AllowedFileType(file.name) && file.size <= fileSize) {
      if (file.size === 0) {
        alert('Cannot process blank file -- ' + file.name)
      }
      else {
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
              let file_type = ''
              if (file.type === '') {
                file_type = 'Lexos Workspace'
                template.find('.file-information').find('.file-type').html(file_type)
              }
              else {
                template.find('.file-information').find('.file-type').html(file.type)
                e.target.result.replace(/</g, '&lt;').replace(/>/g, '&gt;')
              }
              let file_size = file.size
              if (file_size < 1024) {
                template.find('.file-information').find('.file-size').html(file.size + 'bytes')
              }
              else if (file.size < 1048576) {
                file_size = (file.size / 1024).toFixed(1)
                template.find('.file-information').find('.file-size').html(file_size + 'KB')
              }
              else {
                file_size = (file.size / 1024 / 1024).toFixed(1)
                template.find('.file-information').find('.file-size').html(file_size + 'MB')
              }
              $('#manage-previews').prepend(template)
            }
            reader.readAsText(file)
            $('#activeDocIcon').css('display', 'block')
            $('#status').hide()
          })

          .fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown)
          })
      }
    }
    else if (!AllowedFileType(file.name)) {
      alert('Upload for ' + filename + ' failed.\n\nInvalid file type.')
    }
    else {
      alert('Upload for ' + filename + ' failed.\n\nFile bigger than ' + MAX_FILE_SIZE_INT.value + ' ' + MAX_FILE_SIZE_UNITS.title + 'B.')
    }
}


/*Send ajax request*/
function sendAjaxRequest(file,filename) {
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
