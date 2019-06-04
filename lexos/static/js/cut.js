let document_previews;
$(function(){

    // Display the loading overlay on the "Previews" section
    start_loading("#previews");

    // Load the appropriate content for the "Cut Settings" element
    load_cut_settings_section();

    // Create a preview for each active document
    $.ajax({type: "GET", url: "document-previews"})
    .done(function(response){
        document_previews = JSON.parse(response);
        initialize_document_previews(response);
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
        error("Failed to cut the documents");
        add_text_overlay("#previews", "No Previews");
        finish_document_previews_loading();
    })
}


/**
 * Validate the inputs.
 * @returns {boolean}: Whether the inputs are valid.
 */
function validate_inputs(){



    // Validate no settings for the "Milestone" cut mode
    if(cut_mode === "milestone"){
        let milestone = $("#milestone-input input").val();
        if(milestone.length <= 0)
        { error("A milestone must be provided"); return false; }
        return true;
    }

    // Segment size
    let segment_size = $("#segment-size-input input").val();
    if(!segment_size || segment_size < 1 || isNaN(segment_size))
    { error("Invalid segment size."); return false; }
    segment_size = parseInt(segment_size);

    // Only validate the segment size for the "Segments" cut mode
    if(cut_mode === "number")  return true;

    // Overlap
    let overlap = $("#overlap-input input").val();
    if(!overlap ||  overlap < 0 || isNaN(overlap))
    { error("Invalid overlap size."); return false; }
    overlap = parseInt(overlap);

    if(overlap > segment_size){ error("The overlap cannot be "+
        "greater than the segment size."); return false; }

    // Merge threshold
    let merge_threshold = $("#merge-threshold-input input").val();
    if(!merge_threshold ||  merge_threshold < 0 ||
        merge_threshold > 100 || isNaN(merge_threshold))
    { error("Invalid merge threshold."); return false; }


    return true;
}


/**
 * Creates the document previews.
 * @param {string} response: The response containing the new previews.
 */
function create_document_previews(response){
    let previews = JSON.parse(response);

    // If there are no previews, display "No Previews" text
    if(!previews.length) add_text_overlay("#previews", "No Previews");

    // Otherwise, create the previews
    else for(const preview of previews)
        create_document_preview(preview[2], preview[3]);

    // Remove the loading overlay, fade in the previews, and enable the
    // buttons for the document previews section
    finish_document_previews_loading();
}
