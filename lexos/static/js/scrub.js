let punctuation_options_visible = true;

$(function(){

    // Create a preview for each active document
    $.ajax({
        type: "GET",
        url: "/scrub/get-document-previews",
    })
    .done(initialize_document_previews);

    // Register punctuation button callback
    $("#punctuation-button").click(function(){
        punctuation_options_visible = !punctuation_options_visible;
        console.log(punctuation_options_visible);
        let element = $("#punctuation-options");
        if(punctuation_options_visible) element.removeClass("disabled");
        else element.addClass("disabled");
    });

    // Register the "preview" and "apply" button callbacks
    $("#preview-button").click(function(){
        $("#form-action").val("preview");
        scrub();
    });

    $("#apply-button").click(function(){
        $("#form-action").val("apply");
        scrub();
    });

    // Add the scrub tags "options" button callback
    $("#scrub-tags-settings-button").click(function(){
        $.ajax({type: "GET", url: "scrub/get-tag-options"})
        .done(get_tag_options_callback);
    });
});


/**
 * Creates the tags options popup.
 *
 * @param {string} response: The response from the scrub/get-tags request.
 */
function get_tag_options_callback(response){
    let tags = JSON.parse(response);

    // Create the popup
    create_popup();
    let popup_content_element = $("#popup-content");

    // If there are no tags, display "no tags" text
    if(!tags.length){
        $(`<h3 id="no-tags-text">No Tags</h3>`)
            .insertAfter(popup_content_element);
        return;
    }

    // Otherwise, create the table head
    $(
        `<div id="tag-table-head">`+
            `<h3>Tag</h3>`+
            `<h3>Action</h3>`+
            `<h3>Replacement</h3>`+
        `</div>`
    ).insertBefore(popup_content_element);

    // Create a row for each tag
    for(const tag of tags){

        let formatted_tag = tag[0].replace(/[^A-Za-z0-9 ]/, '-');

        // Create the row
        let row_element = $(
        `<div class="tag-table-row">`+
            `<h3>${tag[0]}</h3>`+
            `<div>`+
                `<label class="circle-label"><input id="${formatted_tag}-remove-tag-button" type="radio" name="${formatted_tag}-action" value="remove-tag"><span>Remove Tag</span></label>`+
                `<label class="circle-label"><input id="${formatted_tag}-remove-element-button" type="radio" name="${formatted_tag}-action" value="remove-element"><span>Remove All</span></label>`+
                `<label class="circle-label"><input id="${formatted_tag}-replace-element-button" type="radio" name="${formatted_tag}-action" value="replace-element"><span>Replace</span></label>`+
                `<label class="circle-label"><input id="${formatted_tag}-leave-alone-button" type="radio" name="${formatted_tag}-action" value="leave-alone"><span>None</span></label>`+
            `</div>`+
            `<input type="text" spellcheck="false" autocomplete="off" value="${tag[2]}">`+
        `</div>`
        ).appendTo(popup_content_element);

        // Check the appropriate option
        row_element.find(`#${formatted_tag}-${tag[1]}-button`).prop("checked", true);
    }

    // Create the "save" button
    $(
        `<div class="centerer">`+
            `<h3 id="popup-save-button" class="selectable">Save</h3>`+
        `</div>`
    ).appendTo("#popup");

    $("#popup-save-button").click(tag_options_save_callback);
}


/**
 * Saves the tag options.
 */
function tag_options_save_callback(){

    //Create the payload
    let rows = $(".tag-table-row");
    let payload = {};

    for(const row of rows){
        // Get the tag name and attribute
        let tag = $(row).find("h3").text();
        let attribute = $(row).find(`input[type="text"]`).val();

        // Get the action
        let action;
        let labels = $(row).find("label input");
        for(const label of labels)
            if($(label).prop("checked")) action = $(label).val();

        // Add the data to the payload
        payload[tag] = `${action},${tag}`;
        payload[`attributeValue${tag}`] = attribute;
    }

    // Send the payload
    return $.ajax({
        type: "POST",
        url: "scrub/save-tag-options",
        data: JSON.stringify(payload),
        contentType: "application/json; charset=utf-8"
    })
    .done(function(){ close_popup(); });
}


/**
 * Creates a preview for each active document.
 *
 * @param {string} response: The response from the
 *     get-document-previews request.
 */
function initialize_document_previews(response){

    let previews = JSON.parse(response);

    // If there are no previews, display "No Previews" text
    if(!previews.length) display_no_previews_text();

    // Otherwise, create a preview for each active document
    for(const preview of previews) create_document_preview(preview[2], preview[3]);
}


/**
 * Creates a document preview with the given name and text.
 *
 * @param {string} preview_name: The name of the document.
 * @param {string} preview_text: The preview text.
 */
function create_document_preview(preview_name, preview_text) {
    $(`
        <div class="preview">
            <h3 class="preview-name">${preview_name}</h3>
            <h3 class="preview-text">${preview_text}</h3>
        </div>
    `).appendTo("#previews");
}


/**
 * Performs scrubbing on the active documents.
 *
 * @returns {jqXHR}: The response of the request.
 */
function scrub(){
    return $.ajax({
        type: "POST",
        url: "scrub/do-scrubbing",
        processData: false,
        contentType: false,
        data: new FormData($("form")[0])
    })
    .done(function(response){
        let previews = JSON.parse(response);
        $("#previews").empty();  // Remove any existing previews
        if(!previews.length) display_no_previews_text();
        else for(const preview of previews)
            create_document_preview(preview[0], preview[1]);
    });
}

function display_no_previews_text(){
    $(
        `<div class="centerer">`+
            `<h3>No Previews</h3>`+
        `</div>`
    ).appendTo("#previews");
}
