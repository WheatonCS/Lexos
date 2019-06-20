$(function(){
    // If guide button is clicked...
    $("#guide-button").click(function() {
        tool_intro();
    });

    // Create the table displaying the uploaded documents
    create_table();

    // Initialize the selection box
    initialize_selection_box();

    // Create the context menu hide callbacks
    $(window).on("mousedown resize", hide_context_menu);
    $("#main-section").on("scroll", hide_context_menu);

    // Create the context menu button callbacks
    $("#preview-button").mousedown(preview);
    $("#edit-name-button").mousedown(edit_name);
    $("#edit-class-button").mousedown(edit_class);
    $("#delete-button").mousedown(delete_document);
    $("#merge-selected-button").mousedown(merge_selected);
    $("#edit-selected-classes-button").mousedown(edit_selected_classes);
    $("#delete-selected-button").mousedown(delete_selected);
    $("#select-all-button").mousedown(select_all);
    $("#deselect-all-button").mousedown(deselect_all);

    // Toggle selection when the "A" key is pressed
    key_down_callback('A', toggle_selection);
});

/**
 * Toggles between selecting and deselecting all documents.
 * @param {event} event: The event that triggered the callback.
 * @param {boolean} pressed: Whether the key was pressed or released.
 */
function toggle_selection(event, pressed){

    // If a popup is being displayed, return
    if($("#popup").length) return;

    // Check whether all documents are selected
    let all_selected = true;
    $(".table-row").each(function(){
        if(!$(this).hasClass("selected-table-row")) all_selected = false;
    });

    // If all documents are selected, deselect all. Otherwise, select all
    if(all_selected) deselect_all();
    else select_all();
}


/**
 * Creates the table displaying the uploaded documents.
 */
let documents = [];
function create_table(){

    // Display the loading overlay on the table body
    start_loading("#table-body");

    // Get the uploaded documents
    $.ajax({type: "GET", url: "manage/documents"})

        // If the request is successful, create the table
        .done(function(json_response){

            documents = parse_json(json_response);

            // If there are no documents, display "No Documents" text and
            // return
            if(documents.length === 0){
                add_text_overlay("#table-body", "No Documents");
                return;
            }

            // Otherwise, enable the "Download" button
            enable("#download-button");

            // Create the table content
            for(let i = 0; i < documents.length; ++i){
                const d = documents[i];
                append_row(d.id, i+1, d.state, d.label,
                    d.class, d.source, d.preview);
            }

            // Remove the loading overlay and fade in the table content
            finish_loading("#table-body", "#table-body");
        })

        // Otherwise, display an error
        .fail(function(){
            error("Failed to fetch the documents.");
            add_text_overlay("#table-body", "Loading Failed");
        });
}


/**
 * Appends a row to the table.
 * @param {string} id: The ID of the document.
 * @param {number} row_number: The number of the row.
 * @param {string} active: Whether the document is active ("true" or "false").
 * @param {string} label: The name of the document.
 * @param {string} class_name: The class name of the document.
 * @param {string} source: The source name of the document.
 * @param {string} preview: The preview of the document.
 */
function append_row(id, row_number, active, label, class_name, source, preview){

    // Create a new row and append it to the "table-body" element
    let row = $(`
        <div id="${id}" class="table-row">
            <div class="active-indicator"></div>
            <h3 class="table-cell">${row_number}</h3>
            <h3 class="table-cell"></h3>
            <h3 class="table-cell"></h3>
            <h3 class="table-cell"></h3>
            <h3 class="table-cell"></h3>
        </div>
    `).appendTo("#table-body");

    // HTML-escape the text and add it to the row
    $(row.find(".table-cell")[1]).text(label);
    $(row.find(".table-cell")[2]).text(class_name);
    $(row.find(".table-cell")[3]).text(source);
    $(row.find(".table-cell")[4]).text(preview);

    // If the row is active, add the "selected-table-row" class
    if(active) row.addClass("selected-table-row");

    // Add the context menu callback to the row
    row.on("contextmenu", show_context_menu);
}


/**
 * Shows a custom context menu.
 * @param {Event} event: The event that triggered the callback.
 */
let context_menu_document_id;
function show_context_menu(event){

    // Prevent the default context menu from appearing
    event.preventDefault();

    // Save the ID of the right-clicked document for use in other functions
    context_menu_document_id = JSON.stringify(parseInt($(this).attr("id")));

    // Set the custom context menu's position to the right-click and make it
    // visible and clickable
    let position = get_mouse_position(event);

    let page_size = get_page_size();
    let context_menu_size = get_element_size("#context-menu");
    let context_menu_far_position = point_add(position, context_menu_size);

    if(context_menu_far_position.x > page_size.x)
        position.x -= context_menu_size.x;

    if(context_menu_far_position.y > page_size.y)
        position.y -= context_menu_size.y;

    $("#context-menu").css({"pointer-events": "auto", "opacity": "1",
        "left": `${position.x}px`, "top": `${position.y}px`});
}


/**
 * Hides the custom context menu.
 * @param {Event} event: The event that triggered the callback.
 */
function hide_context_menu(event){

    // Hide the custom context menu and make it unclickable
    $("#context-menu").css({"pointer-events": "none", "opacity": "0"});
}


/**
 * Creates a popup containing a preview of the document that was right-clicked.
 */
function preview(){

    // Send a request to get the preview of the document that was right-clicked
    send_request("preview", context_menu_document_id)

        // If the request is successful create a popup and append the
        // HTML-escaped document preview to it
        .done(function(response){
            create_popup("Preview");
            let preview = $(`<h3 id="document-preview-text"></h3>`)
                .appendTo("#popup-content");
            preview.text(parse_json(response).previewText);
        })

        // If the request failed, display an error
        .fail(function(){ error(`Failed to retrieve 
            the document's preview.`); });
}


/**
 * Renames the document that was right-clicked.
 */
function edit_name(){

    // Create a popup containing a text input
    create_text_input_popup("Document Name");

    // Set the popup's initial text input to the existing document name
    $("#popup-input").val(documents[context_menu_document_id].label);

    // If the popup's "OK" button is clicked
    $("#popup-ok-button").click(function(){

        // Make a request to set the name of the document that was
        // right-clicked to the content of the popup's text input field
        send_request("edit-name",
            [context_menu_document_id, $("#popup-input").val()])

            // If the request was successful, close the popup and recreate the
            // table
            .done(function(){ close_popup();  create_table(); })

            // If the request failed, display an error
            .fail(function(){ error("Failed to edit the document's name."); });
    });
}


/**
 * Sets the class name of the document that was right-clicked.
 */
function edit_class(){

    // Create a popup containing a text input
    create_text_input_popup("Document Class");

    // Set the popup's initial text input to the existing document class
    $("#popup-input").val(documents[context_menu_document_id].class);

    // When the popup's "OK" button is clicked
    $("#popup-ok-button").click(function(){

        // Make a request to set the class of the document that was
        // right-clicked to the content of the popup's text input field
        send_request("set-class",
            [context_menu_document_id, $("#popup-input").val()])

            // If the request was successful, close the popup and recreate the
            // table
            .done(function(){ close_popup(); create_table(); })

            // If the request failed, display an error
            .fail(function(){ error("Failed to set the document's class."); });
    });
}


/**
 * Deletes the document that was right-clicked.
 */
function delete_document(){

    // Send a request to delete the document that was right-clicked
    send_request("delete", context_menu_document_id)

        // If the request was successful, recreate the table
        .done(create_table)

        // If the request failed, display an error
        .fail(function(){ error("Failed to delete the document."); });
}


/**
 * Merges the selected documents.
 */
function merge_selected(){

    let selected_document_ids = get_selected_document_ids();
    let first_selected_document = documents[selected_document_ids[0]];

    // Create the popup
    create_ok_popup("Merge Active");
    $(`
        <h3>Name: </h3>
        <label><input id="merge-name-input" name="" value="Merge-${first_selected_document.label}" type="text" spellcheck="false" autocomplete="off"></label>
        <br>
        <label>
            <input id="merge-milestone-checkbox" name="" type="checkbox">
            <span></span>
            Milestone:
            <input id="merge-milestone-input" name="" value="#EOF#" type="text" spellcheck="false" autocomplete="off">
         </label>

    `).appendTo("#popup-content");

    // If the popup's "OK" button is clicked...
    $("#popup-ok-button").click(function(){

        // Create the payload
        let payload = [
            selected_document_ids,
            $("#merge-name-input").val(),
            first_selected_document.source,
            $("#merge-milestone-checkbox").is(":checked") ?
                $("#merge-milestone-input").val() : ""
        ];

        // Send the merge request
        send_request("merge-selected", payload)

            // If the request was successful, close the popup and recreate the
            // table
            .done(function(){ close_popup(); create_table(); })

            // If the request failed, display an error
            .fail(function(){
                error("Failed to merge the active documents.");
            });
    });
}


/**
 * Edits the class names of the selected documents.
 */
function edit_selected_classes(){

    // Create a popup containing a text input
    create_text_input_popup("Document Class");

    // If the popup's "OK" button is clicked...
    $("#popup-ok-button").click(function(){

        // Send a request to set the class names of the selected documents
        // to the value in the popup's text input
        send_request("edit-selected-classes",
            [get_selected_document_ids(), $("#popup-input").val()])

            // If the request was successful, close the popup and recreate the
            // table
            .done(function(){ close_popup(); create_table(); })

            // If the request failed, display an error
            .fail(function(){
                error("Failed to edit the active documents' classes.");
            });
    });
}


/**
 * Deletes the selected documents.
 */
function delete_selected(){

    // Send a request to delete the selected documents
    send_request("delete-selected")

        // If the request was successful, recreate the table
        .done(create_table)

        // If the request failed, display an error
        .fail("Failed to delete the active documents");
}


/**
 * Selects all the documents in the table.
 */
function select_all(){

    let id_list = [];

    // For each row in the table...
    $(".table-row").each(function(){

        // Add the document's ID to "id_list"
        id_list.push($(this).attr("id"));

        // Give the row the class that indicates it is selected
        $(this).addClass("selected-table-row");
    });

    // Send a request to activate all the documents
    send_request("activate", id_list)

        // If the request failed, display an error
        .fail(function(){ error("Failed to activate the documents."); });
}


/**
 * Deselects all the documents.
 */
function deselect_all(){

    let id_list = [];

    // For each row in the table...
    $(".table-row").each(function(){

        // Add the document's ID to "id_list"
        id_list.push($(this).attr("id"));

        // Remove the class that indicates the row is selected
        $(this).removeClass("selected-table-row");
    });

    // Send a request to deactivate all the documents
    send_request("deactivate", id_list)

        // If the request failed, display an error
        .fail(function(){ error("Failed to deactivate the documents."); });
}


/**
 * Sends a JSON POST request to the given URL.
 * @param {string} url: The URL to send the request to.
 * @param {object} payload: The JSON payload to send.
 * @returns {jqXHR}: The jQuery request object.
 */
function send_request(url, payload = ""){

    // Disable the download button
    disable("#download-button");

    // Send the request
    return $.ajax({
        type: "POST",
        url: "manage/"+url,
        data: JSON.stringify(payload),
        contentType: "application/json; charset=utf-8"
    })

    // If the request is successful...
    .done(function(){
        update_active_document_count()
            .done(function(response){

                // If there is at least one active document, enable the
                // "Download" button
                if(parseInt(response) >= 1) enable("#download-button");
            });
    });h
}


/**
 * Gets the IDs of the currently selected documents.
 * @returns {Number[]}: The selected document IDs.
 */
function get_selected_document_ids(){
    let id_list = [];
    $(".table-row").each(function(){
        if($(this).hasClass("selected-table-row"))
            id_list.push(parseInt($(this).attr("id")));
    });

    return id_list;
}

function tool_intro() {
        // Intro Guide Stuff
    let introguide = introJs();

    introguide.setOptions({
        steps: [
            {
                element: '#table',
                intro: 'This is the Manage page.',
                position: 'top',
            },
            {
                element: '#active',
                intro: 'Active documents will have a blue highlight to them. You can deactivate documents by clicking while holding down "D".',
                position: 'bottom'
            },
            {
                element: '#document',
                intro: 'The Document column holds custom document names. You can rename documents by right clicking.',
                position: 'bottom'
            },
            {
                element: '#class',
                intro: 'If you want to group documents together, you may give them a class by right clicking.',
                position: 'bottom'
            },
            {
                element: '#excerpt',
                intro: 'Excerpt will give you a preview of your document.',
                position: 'bottom'
            },
            {
                element: '#help-button',
                intro: 'Check our Help section for more advice on the Manage page.',
                position: 'bottom'
            },
            {
                element: '#prepare-button',
                intro: 'Once you\'re satisfied with your active documents, you can move on to the Prepare step! Exit this tutorial and click "Scrub" from the dropdown menu.',
                position: 'bottom'
            }
        ]
    })
    introguide.start();
}
