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
function load_cut_settings_section(){

    let cut_settings_grid_element = $("#cut-settings-grid");
    cut_settings_grid_element.css("opacity", "0");
    let cut_mode = $("#cut-mode-grid input:checked").val();
    let settings_elements;

    // Remove any existing content in the "Cut Settings" section
    cut_settings_grid_element.empty();

    // If the cut mode is set to "Segments"...
    if(cut_mode === "number") settings_elements = $(`
        <div><h3>Segments</h3><input name="cutValue" type="text" spellcheck="false" autocomplete="off"></div>
    `);

    // Otherwise, if the cut mode is set to "Milestones"...
    else if(cut_mode === "milestone") settings_elements = $(`
        <div><h3>Milestone</h3><input id="milestone-input" name="MScutWord" type="text" spellcheck="false" autocomplete="off"></div>
    `);

    // Otherwise, if the cut mode is set to "Tokens", "Characters", or "Lines"...
    else settings_elements = $(`
        <div><h3>Segment Size</h3><input name="cutValue" type="text" spellcheck="false" autocomplete="off"></div>
        <div><h3>Overlap</h3><input name="cutOverlap" type="text" spellcheck="false" autocomplete="off" value="0"></div>
        <div><h3>Merge Threshold</h3><input name="cutLastProp" type="text" spellcheck="false" autocomplete="off" value="50"></div>
    `);

    // Append the appropriate settings to the "Cut Settings" section
    settings_elements.appendTo(cut_settings_grid_element);

    // Check the legacy "MScutWord" input if the cut mode is "milestone"
    $("#milestone-input").prop("checked", cut_mode === "milestone");

    // Fade in the settings
    fade_in(cut_settings_grid_element);
}


/**
 * Cuts the active documents.
 * @param {string} action: The cut operation action ("preview" or "apply").
 */
function cut(action){

    // Display the loading overlay and disable the buttons on the document
    // previews section
    start_document_previews_loading();

    // Load the form data and add an entry for the cut action
    let form_data = new FormData($("form")[0]);
    form_data.append("action", action);

    // Create a copy of the cut settings for each document to satisfy legacy
    // requirements
    let options = ["cutType", "cutValue", "cutOverlap", "cutLastProp"]
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
    .done(create_document_previews);
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
        for(let i = 0; i < preview[3].length; ++i)
            create_document_preview(preview[1]+'_'+(i+1), preview[3][i][1]);

    // Remove the loading overlay, fade in the previews, and enable the
    // buttons for the document previews section
    finish_document_previews_loading();
}
