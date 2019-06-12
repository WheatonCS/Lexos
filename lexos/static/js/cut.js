let document_previews;
$(function(){

    // Display the loading overlay on the "Previews" section
    start_loading("#previews");

    // Initialize the "Tokenize", "Normalize", and "Cull" tooltips
    initialize_tooltips();

    // Send a request for the document preview data
    $.ajax({type: "GET", url: "document-previews"})

        // If the request was successful, create a preview for each active
        // document
        .done(function(response){
            document_previews = parse_json(response);
            initialize_document_previews(response);
        })

        // If the request failed, display an error and "Loading Failed" text
        .fail(function(){
            error("Failed to retrieve the document previews.");
            add_text_overlay("#previews", "Loading Failed");
            enable("#preview-button, #apply-button");
        });

    // Perform the cutting if the "Preview" or "Apply" button is pressed
    $("#preview-button").click(function(){ cut("preview"); });
    $("#apply-button").click(function(){ cut("apply"); });

    // Load the appropriate content for the "Cut Settings" section when the
    // "Cut Mode" setting is changed
    $("#cut-mode-section input").change(load_cut_settings_section);
});


/**
 * Loads the appropriate content for the "Cut Settings" section.
 */
let cut_mode;
function load_cut_settings_section(){

    let cut_settings_grid_element = $("#cut-settings-grid");
    cut_settings_grid_element.css("opacity", "0");
    cut_mode = $("#cut-mode-grid input:checked").val();

    // If the cut mode is set to "Segments"...
    if(cut_mode === "number"){
        hide("#milestone-input, #overlap-input, #merge-threshold-input");
        show("#segment-size-input");
    }

    // Otherwise, if the cut mode is set to "Milestones"...
    else if(cut_mode === "milestone"){
        hide("#segment-size-input, #overlap-input, #merge-threshold-input");
        show("#milestone-input");
    }

    // Otherwise, if the cut mode is set to "Tokens", "Characters", or "Lines"...
    else {
        hide("#milestone-input");
        show("#segment-size-input, #overlap-input, #merge-threshold-input");
    }

    // Set the legacy "cutByMS" input if the cut mode is "milestone"
    $("#cut-by-milestone-input").val(cut_mode === "milestone" ? "on" : "off")

    // Fade in the settings
    fade_in(cut_settings_grid_element);
}


/**
 * Cuts the active documents.
 * @param {string} action: The cut operation action ("preview" or "apply").
 */
function cut(action){

    // Validate the inputs. If the inputs are invalid, return
    if(!validate_inputs()) return;

    // Remove any existing error messages
    remove_errors();

    // Display the loading overlay and disable the buttons on the document
    // previews section
    start_document_previews_loading();

    // Load the form data and add an entry for the cut action
    let form_data = new FormData($("form")[0]);
    form_data.append("action", action);

    // Create a copy of the cut settings for each document to satisfy legacy
    // requirements
    let options = ["cutType", "cutValue", "cutOverlap",
        "cutLastProp", "MScutWord"]
    for(const document of document_previews)
        for(const option of options)
            form_data.append(option+'_'+document[0], form_data.get(option));

    // Send the cut request
    $.ajax({
        type: "POST",
        url: "cut/execute",
        processData: false,
        contentType: false,
        data: form_data
    })

    // If the request is successful, update the document previews with the
    // cut previews returned in the response
    .done(create_document_previews)


    // If the request failed, display an error and remove the loading overlay
    .fail(function(){
        error("Failed to cut the documents.");
        add_text_overlay("#previews", "Loading Failed");
        enable("#preview-button, #apply-button");
    })
}


/**
 * Creates the document previews.
 * @param {string} response: The response containing the new previews.
 */
function create_document_previews(response){
    let previews = parse_json(response);

    // If there are no previews, display "No Previews" text
    if(!previews.length) add_text_overlay("#previews", "No Previews");

    // Otherwise, create the previews
    else for(const preview of previews)
        create_document_preview(preview[2], preview[3]);

    // Remove the loading overlay, fade in the previews, and enable the
    // buttons for the document previews section
    finish_document_previews_loading();
}


/**
 * Validate the inputs.
 * @returns {boolean}: Whether the inputs are valid.
 */
function validate_inputs(){

    // "Milestone"
    if(cut_mode === "milestone"){
        if($("#milestone-input input").val().length <= 0){
            error("A milestone must be provided.");
            return false;
        }
        return true;
    }

    // "Segment size"
    let segment_size = $("#segment-size-input input").val();
    let int_segment_size = parseInt(segment_size);
    if(!validate_number(segment_size, 1)){
        error("Invalid segment size.");
        return false;
    }

    // "Segments"
    if(cut_mode === "number") return true;

    // "Overlap"
    let overlap = $("#overlap-input input").val();
    let int_overlap = parseInt(overlap);
    if(!validate_number(overlap, 0)){
        error("Invalid overlap size.");
        return false;
    }

    if(int_overlap > int_segment_size){
        error("The overlap cannot be "+
            "greater than the segment size.");
        return false;
    }

    // "Merge threshold"
    if(!validate_number($("#merge-threshold-input input").val(), 0, 100)){
        error("Invalid merge threshold.");
        return false;
    }

    return true;
}


/**
 * Initialize the tooltips.
 */
function initialize_tooltips(){

    // "Cut Mode"
    create_tooltip("#cut-mode-tooltip-button", `Lexos uses spaces between
        tokens to determine where to cut documents into the specified number,
        so this tool may not work if you used Scrubber to strip white spaces
        from your documents.`);

    // "Segment Size"
    create_tooltip("#segment-size-tooltip-button", `A positive integer used to 
        divide up the text. Either the number of letters, words, or lines 
        per segment, or the number of segments per document.`);

    // "Overlap"
    create_tooltip("#overlap-tooltip-button", `The amount of overlapping
        content at the start and end of segments. This number must be smaller
        than the segment size.`, true);

    // "Merge %"
    create_tooltip("#merge-threshold-tooltip-button", `The size of the last
        segment must be at least as large as the given percentage relative to
        other segment sizes. If the length of the last segment is below this
        threshold, it will be attached to the previous segment.`, true);

    // "Milestone"
    create_tooltip("#milestone-tooltip-button", ``);
}
