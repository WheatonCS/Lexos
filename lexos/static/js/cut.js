let document_previews;
$(function(){
    load_cut_settings_section();

    // Create a preview for each active document
    $.ajax({type: "GET", url: "document-previews"})
    .done(function(response){
        document_previews = JSON.parse(response);
        initialize_document_previews(response);
    });

    // Register the "preview" and "apply" button callbacks
    $("#preview-button").click(function(){ cut("preview"); });
    $("#apply-button").click(function(){ cut("apply"); });

    // Register a "cut mode" change callback
    $("#cut-mode-section input").change(load_cut_settings_section);
});


/**
 * Loads the "cut settings" section.
 */
function load_cut_settings_section(){

    console.log("r")

    let cut_settings_grid_element = $("#cut-settings-grid");
    let cut_mode = $("#cut-mode-grid input:checked").val();
    let settings_elements;

    // Remove any existing contents
    cut_settings_grid_element.empty();

    // Segments mode
    if(cut_mode === "number") settings_elements = $(`
        <div><h3>Number of Segments</h3><input name="cutValue" type="text" spellcheck="false" autocomplete="off"></div>
    `);

    // Milestones mode
    else if(cut_mode === "milestone") settings_elements = $(`
        <div><h3>Milestone</h3><input id="milestone-input" name="MScutWord" type="text" spellcheck="false" autocomplete="off"></div>
    `);

    // Tokens, characters, or lines mode
    else settings_elements = $(`
        <div><h3>Segment Size</h3><input name="cutValue" type="text" spellcheck="false" autocomplete="off"></div>
        <div><h3>Overlap</h3><input name="cutOverlap" type="text" spellcheck="false" autocomplete="off" value="0"></div>
        <div><h3>Merge Threshold</h3><input name="cutLastProp" type="text" spellcheck="false" autocomplete="off" value="50"></div>
    `);

    // Set the legacy milestone input
    $("#milestone-input").prop("checked", cut_mode === "milestone");

    settings_elements.appendTo(cut_settings_grid_element);
}


/**
 * Cuts the active documents.
 *
 * @param {string} action: The action for the cut operation (preview or apply).
 */
function cut(action){

    // Set the action
    let form_data = new FormData($("form")[0]);
    form_data.append("action", action);

    // Create copies of the settings for each document
    let options = ["cutType", "cutValue", "cutOverlap", "cutLastProp"]
    for(const document of document_previews)
        for(const option of options)
            form_data.append(option+'_'+document[0], form_data.get(option));

    // Send the request
    $.ajax({
        type: "POST",
        url: "cut/execute",
        processData: false,
        contentType: false,
        data: form_data
    })
    .done(update_document_previews);
}


/**
 * Updates the document previews.
 * @param {string} response: The response containing the new previews.
 */
function update_document_previews(response){
    let previews = JSON.parse(response);

    // Remove any existing previews
    $("#previews").empty();

    // If there are no previews, display "no previews" text
    if(!previews.length) display_no_previews_text();

    // Otherwise, create the previews
    else for(const preview of previews)
        for(let i = 0; i < preview[3].length; ++i)
            create_document_preview(preview[1]+'_'+(i+1), preview[3][i][1]);
}
