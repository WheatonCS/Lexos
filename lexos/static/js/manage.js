/**
 * Initializes the manage page after it has loaded.
 */
let d_held = false;
$("document").ready(function(){

    // Table
    update_table();

    // Context menu
    $(window).on("mousedown resize", context_menu_hide_callback);
    $("#main-section").on("scroll", context_menu_hide_callback);

    $("#preview-button").mousedown(preview_callback);
    $("#edit-name-button").mousedown(edit_name_callback);
    $("#edit-class-button").mousedown(edit_class_callback);
    $("#delete-button").mousedown(delete_callback);

    // $("#merge-selected-button").mousedown(merge_selected_callback);
    $("#edit-selected-classes-button").mousedown(edit_selected_classes_callback);
    $("#delete-selected-button").mousedown(delete_selected_callback);

    $("#select-all-button").mousedown(select_all_callback);
    $("#deselect-all-button").mousedown(deselect_all_callback);

    // Selection
    initialize_selection_box();
    let manage_table_body = $("#manage-table-body");
    manage_table_body.mousedown(selection_start_callback);
    manage_table_body.mouseup(selection_end_callback);
});


/**
 * Updates the table displaying the uploaded documents.
 */
let documents = [];
function update_table(){
    let form = $("form").css("opacity", "0");  // Hide the page
    $("#manage-table-body").empty();  // Delete the table if it exists

    // Get the uploaded documents
    $.ajax({type: "GET", url: "manage/documents"}).done(function(json_response){

        documents = JSON.parse(json_response);

        // If there are no documents, display "No Documents" text
        if(documents.length === 0){
            form.html(`<div class="centerer"><h3>No Documents</h3></div>`);
            form.css("opacity", "1");  // Show the page
        }

        // Otherwise, create the table
        else {
            let form = $("form");
            for(const d of documents)
                append_row(d.id, d.state, d.label, d.class, d.source, d.preview);
            form.css("opacity", "1");  // Show the page
        }
    });
}


/**
 * Appends a row to the table.
 *
 * @param {String} id: The ID of the document.
 * @param {String} state: Whether the document is selected ("true" or "false").
 * @param {String} label: The name of the document.
 * @param {String} class_name: The class name of the document.
 * @param {String} source: The source name of the document.
 * @param {String} preview: A preview of the document.
 */
function append_row(id, state, label, class_name, source, preview){

    // Truncate
    label = label.substring(0, 30);
    source = source.substring(0, 30);
    preview = preview.substring(0, 200);

    // Append the row
    let row = $(
        `<div id="${id}" class="manage-table-row">`+
            `<div class="circle"></div>`+
            `<h3 class="manage-table-cell">${label}</h3>`+
            `<h3 class="manage-table-cell">${class_name}</h3>`+
            `<h3 class="manage-table-cell">${source}</h3>`+
            `<h3 class="manage-table-cell">${preview}</h3>`+
        `</div>`
    ).appendTo("#manage-table-body");

    if(state) row.addClass("selected-row");

    row.on("contextmenu", context_menu_show_callback);
}


/**
 * Shows the context menu.
 *
 * @param {Event} event: The event that triggered the callback.
 */
let context_menu_document_id;
function context_menu_show_callback(event){
    event.preventDefault();

    context_menu_document_id = JSON.stringify(parseInt($(this).attr("id")));

    let mouse_position = get_mouse_position(event);
    $("#context-menu").css({"pointer-events": "auto", "opacity": "1",
        "left": `${mouse_position.x}px`, "top": `${mouse_position.y}px`});
}


/**
 * Hides the context menu.
 *
 * @param {Event} event: The event that triggered the callback.
 */
function context_menu_hide_callback(event){
    $("#context-menu").css({"pointer-events": "none", "opacity": "0"});
}


/**
 * Gives a preview popup of the document that was right-clicked.
 */
function preview_callback(){
    send_request("preview", context_menu_document_id)
    .done(function(response){
        create_popup();
        $(`<h3>${JSON.parse(response).previewText}</h3>`)
            .appendTo("#popup-content");
    });
}


/**
 * Renames the document that was right-clicked.
 */
function edit_name_callback(){
    create_text_input_popup();

    $("#popup-ok-button").click(function(){
         send_request("edit-name",
             [context_menu_document_id, $("#popup-input").val()])
        .done(function(){
            close_popup();
            update_table();
        });
    });
}


/**
 * Sets the class name of the document that was right-clicked.
 */
function edit_class_callback(){
    create_text_input_popup();

    $("#popup-ok-button").click(function(){
        send_request("set-class",
            [context_menu_document_id, $("#popup-input").val()])
        .done(function(){
            close_popup();
            update_table();
        });
    });
}


/**
 * Deletes the document that was right-clicked.
 */
function delete_callback(){
    send_request("delete", context_menu_document_id).done(update_table);
}


/**
 * Merges the selected documents.
 */
function merge_selected_callback(){
    // Not implemented
}


/**
 * Edits the class names of the selected documents.
 */
function edit_selected_classes_callback(){
    create_text_input_popup();

    $("#popup-ok-button").click(function(){
        send_request("edit-selected-classes",
            [get_selected_document_ids(), $("#popup-input").val()])
        .done(function(){
            close_popup();
            update_table();
        });
    });
}


/**
 * Deletes the selected documents.
 */
function delete_selected_callback(){
    send_request("delete-selected").done(update_table);
}


/**
 * Selects all the documents.
 */
function select_all_callback(){
    let id_list = [];
    $(".manage-table-row").each(function(){
        id_list.push($(this).attr("id"));
        $(this).addClass("selected-row");
    });

    send_request("activate", id_list);
}


/**
 * Deselects all the documents.
 */
function deselect_all_callback(){
    let id_list = [];
    $(".manage-table-row").each(function(){
        id_list.push($(this).attr("id"));
        $(this).removeClass("selected-row");
    });

    send_request("deactivate", id_list);
}


/**
 * Initializes the selection box.
 */
function initialize_selection_box(){

    // Determine if the "D" key is held and change the selection box color
    // depending on if it is
    $(window).keydown(function(event){
        if(event.which !== 68) return;  // Only accept the "D" key
        d_held = true;
        set_selection_box_color();
    });

    $(window).keyup(function(event){
        if(event.which !== 68) return;  // Only accept the "D" key
        d_held = false;
        set_selection_box_color();
    });

    // Disable the selection box if it is outside of the table body
    $(window).mousemove(function(){ $("#selection-box").css("opacity", "0"); });
}


/**
 * Sets the color of the selection box.
 */
function set_selection_box_color(){
    if(d_held) $("#selection-box").css({"background-color": "#000000"});
    else $("#selection-box").css({"background-color": "#FF6000"});
}


/**
 * Sets the selection box starting point.
 *
 * @param {Event} event: The event which triggered the callback.
 */
let start_mouse_position;
let start_scroll_offset;
function selection_start_callback(event){
    if(event.which !== 1) return; // Only accept left clicks

    start_mouse_position = get_mouse_position(event);
    start_scroll_offset = get_main_section_scroll_offset();

    $("#manage-table-body").on("mousemove", selection_drag_callback);
    $("#main-section").on("scroll", selection_drag_callback);

    // Create the selection box
    let selection_box = $("#selection-box");
    set_selection_box_color();
    selection_box.css({"opacity": ".6", "width": "0", "height": "0",
        "transition": "opacity .2s, background-color .2s"});
}


/**
 * Applies the selection
 *
 * @param {Event} event: The event which triggered the callback.
 */
function selection_end_callback(event){
    if(event.which !== 1) return;  // Only accept left clicks

    // Check that there is a valid starting position
    if(!start_mouse_position || start_mouse_position.x.isNaN) return;

    $(window).unbind("mousemove", selection_drag_callback);
    $("#manage-table-body").unbind("scroll", selection_drag_callback);
    $("#selection-box").css("opacity", "0");  // Remove the selection box

    // Select the appropriate documents
    let modified_id_list = [];
    let mouse_position = get_mouse_position(event);
    let main_section_scroll_offset = get_main_section_scroll_offset();
    let window_scroll_offset = get_window_scroll_offset();

    $(".manage-table-row").each(function(){
        let bounding_box = $(this)[0].getBoundingClientRect();

        // Get the selection minimum and maximum
        let scroll_delta = point_subtract(
            main_section_scroll_offset, start_scroll_offset);
        let selection_start = point_subtract(start_mouse_position, scroll_delta);

        let selection_minimum = point_minimum(selection_start, mouse_position);
        let selection_maximum = point_maximum(selection_start, mouse_position);

        // Check if the element is within the selection
        if(window_scroll_offset.x+bounding_box.left < selection_maximum.x &&
            window_scroll_offset.x+bounding_box.right > selection_minimum.x &&
            window_scroll_offset.y+bounding_box.top < selection_maximum.y &&
            window_scroll_offset.y+bounding_box.bottom > selection_minimum.y){

            // Select or deselect the document
            if(d_held && $(this).hasClass("selected-row")){
                $(this).removeClass("selected-row");
                modified_id_list.push($(this).attr("id"));
            }
            else if(!d_held && !$(this).hasClass("selected-row")){
                $(this).addClass("selected-row");
                modified_id_list.push($(this).attr("id"));
            }
        }
    });

    // Reset the starting position
    start_mouse_position = {x: NaN, y: NaN};

    // Apply the selection if one was made
    if(modified_id_list.length)
        send_request(d_held ? "deactivate" : "activate", modified_id_list);
}


/**
 * Updates the selection box visualization.
 *
 * @param {Event} event: The event which triggered the callback.
 */
let previous_mouse_position;
let scroll_start_position;
function selection_drag_callback(event){

    event.stopPropagation();

    let scroll_offset = get_main_section_scroll_offset();

    // If the event is a mouse move event, get the mouse position
    let mouse_position;
    if(event.type === "mousemove"){
        mouse_position = get_mouse_position(event);
        previous_mouse_position = mouse_position;
        scroll_start_position = scroll_offset;
    }

    // Otherwise the event is a scroll event, so use the previous mouse position
    else mouse_position = previous_mouse_position;

    // Get the position and size of the selection box
    let scroll_delta = point_subtract(scroll_offset, start_scroll_offset);
    let selection_start = point_subtract(start_mouse_position, scroll_delta);

    let position = point_minimum(selection_start, mouse_position);
    let size = point_subtract(point_maximum(
        selection_start, mouse_position), position);

    // Update the selection box's CSS
    let selection_box = $("#selection-box");
    selection_box.css({"left": `${position.x}px`, "top": `${position.y}px`,
        "width": `${size.x}px`, "height": `${size.y}px`});
}


/**
 *
 * @param {String} url: The URL to send the request to.
 * @param {Object} payload: The JSON payload to send.
 * @returns {jqXHR}: The response of the request.
 */
function send_request(url, payload = ""){
    return $.ajax({
        type: "POST",
        url: "manage/"+url,
        data: JSON.stringify(payload),
        contentType: "application/json; charset=utf-8"
    })
    .done(update_active_document_count);
}


/**
 * Gets the IDs of the currently selected documents.
 *
 * @returns {Array}: The selected document IDs.
 */
function get_selected_document_ids(){
    let id_list = [];
    $(".manage-table-row").each(function(){
        if($(this).hasClass("selected-row"))
            id_list.push(parseInt($(this).attr("id")));
    });

    return id_list;
}
