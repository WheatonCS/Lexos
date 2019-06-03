$(function(){

    // Display the loading overlay and disable the buttons on the document
    // previews section
    start_document_previews_loading();

    // Create a preview for each active document
    $.ajax({type: "GET", url: "document-previews"})
    .done(function(response){ initialize_document_previews(response); });

    // Disable the punctuation options when the "Remove Punctuation" checkbox
    // is unchecked
    let punctuation_checkbox_element = $("#punctuation-checkbox");
    punctuation_checkbox_element.click(function(){
        let punctuation_options_element = $("#punctuation-options");
        if(punctuation_checkbox_element.is(":checked"))
            punctuation_options_element.removeClass("disabled");
        else punctuation_options_element.addClass("disabled");
    });

    // Scrub the documents when the "Preview" and "Apply" buttons are pressed
    $("#preview-button").click(function(){ scrub("preview"); });
    $("#apply-button").click(function(){ scrub("apply"); });

    // Create the tag options popup when the "Scrub Tags" "Options" button is
    // pressed
    $("#scrub-tags-settings-button").click(function(){
        $.ajax({type: "GET", url: "scrub/get-tag-options"})
        .done(create_tag_options_popup);
    });
});


/**
 * Creates the tags options popup.
 * @param {string} response: The response from the "scrub/get-tags" request.
 */
function create_tag_options_popup(response){

    // Parse the response
    let tags = JSON.parse(response);

    // Create the popup
    create_ok_popup("Tag Options");
    let popup_content_element = $("#popup-content");

    // If there are no tags, display "No Tags" text and return
    if(!tags.length){
        add_text_overlay("#popup-content", "No Tags");
        return;
    }

    // Otherwise, create the table head and body
    $(`
        <div id="tag-table-head">
            <h3>Tag</h3>
            <h3>Action</h3>
            <h3>Replacement</h3>
        </div>
        <div id=tag-table-body></div>
    `).appendTo(popup_content_element);

    // Create a row for each tag
    for(const tag of tags){

        // Replace non-alphanumeric characters with dashes
        let formatted_tag = tag[0].replace(/[^A-Za-z0-9 ]/, '-');

        // Create the row element
        let row_element = $(`
            <div class="tag-table-row">
                <h3></h3>
                <div>
                    <label class="circle-label"><input id="${formatted_tag}-remove-tag-button" type="radio" name="${formatted_tag}-action" value="remove-tag"><span>Remove Tag</span></label>
                    <label class="circle-label"><input id="${formatted_tag}-remove-element-button" type="radio" name="${formatted_tag}-action" value="remove-element"><span>Remove All</span></label>
                    <label class="circle-label"><input id="${formatted_tag}-replace-element-button" type="radio" name="${formatted_tag}-action" value="replace-element"><span>Replace</span></label>
                    <label class="circle-label"><input id="${formatted_tag}-leave-alone-button" type="radio" name="${formatted_tag}-action" value="leave-alone"><span>None</span></label>
                </div>
                <input type="text" spellcheck="false" autocomplete="off" value="${tag[2]}">
            </div>
        `).appendTo("#tag-table-body");

        // Add the HTML-escaped tag name to the row element
        row_element.find("h3").text(tag[0]);

        // Check the appropriate option
        row_element.find(`#${formatted_tag}-${tag[1]}-button`).prop("checked", true);
    }

    // Save the tag options when the "OK" button is pressed
    $("#popup-ok-button").click(save_tag_options);
}


/**
 * Saves the tag options.
 */
function save_tag_options(){

    //Create the payload
    let rows = $(".tag-table-row");
    let payload = {};

    // For each row in the tag options table...
    for(const row of rows){

        // Get the tag name and attribute
        let tag = $(row).find("h3").text();
        let attribute = $(row).find(`input[type="text"]`).val();

        // Get the scrubbing action
        let action;
        let labels = $(row).find("label input");
        for(const label of labels)
            if($(label).prop("checked")) action = $(label).val();

        // Add the data to the payload
        payload[tag] = `${action},${tag}`;
        payload[`attributeValue${tag}`] = attribute;
    }

    // Send a request to save the tag options
    return $.ajax({
        type: "POST",
        url: "scrub/save-tag-options",
        data: JSON.stringify(payload),
        contentType: "application/json; charset=utf-8"
    })

    // If the request is successful, close the popup
    .done(close_popup);
}


/**
 * Performs scrubbing on the active documents.
 * @param {string} action: The action for the scrub operation (preview or apply).
 */
function scrub(action){

    // Display the loading overlay and disable the buttons on the document
    // previews section
    start_document_previews_loading();

    // Set the action
    let form_data = new FormData($("form")[0]);
    form_data.append("action", action);

    // Send the request
    $.ajax({
        type: "POST",
        url: "scrub/execute",
        processData: false,
        contentType: false,
        data: form_data
    })
    .done(update_document_previews);
}


/**
 * Updates the document previews.
 *
 * @param {string} response: The response containing the new previews.
 */
function update_document_previews(response){
    let previews = JSON.parse(response);

    // If there are no previews, display "No Previews" text and return
    if(!previews.length){
        add_text_overlay("#previews", "No Previews");
        return;
    }

    // Create the previews as hidden elements
    for(const preview of previews)
        create_document_preview(preview[0], preview[1]);

    // Remove the loading overlay, fade in the previews, and enable the
    // buttons for the document previews section
    finish_document_previews_loading();
}
