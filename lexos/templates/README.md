# Structure of passed in variables to templates:

+ previews: If showing the file previews, the variable to be passed to the template parser (Jinja) (used to create the HTML) will be a list of 3-tuples of the format:
  + (fileID, filename, file_contents) where:
    + fileID is the unique identifier for the file (useful for resolving duplicate filenames)
    + filename is the original (and possible modified) name/viewing-label for the uploaded file
    + file_contents is the string containing a little preview of the file

+ num_active_files: The template parser will also be provided with the number of active files currently being acted on
