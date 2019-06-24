/**
 * Initializes the selection box.
 */
function initialize_selection_box(){

    // Keep track of whether the "D" key is pressed or not
    key_callback('D', set_d_key);

    // Disable the selection box if the mouse moves outside of the table body
    $(window).mousemove(function(){ $("#selection-box").css("opacity", "0"); });

    // Call the "start_selection()" function on mouse button presses and the
    // "end_selection()" function on mouse releases
    let manage_table_body = $("#table-body");
    manage_table_body.mousedown(start_selection);
    manage_table_body.mouseup(end_selection);
}


/**
 * Keeps track of whether the "D" key is pressed and updates the selection box
 * color accordingly.
 * @param {event} event: The keydown or keyup event that caused the callback.
 * @param {boolean} pressed: Whether the key was pressed.
 */
let d_held = false;
function set_d_key(event, pressed){

    // Set "d_held" to the appropriate value
    d_held = pressed;

    // Make the selection box the corresponding color
    set_selection_box_color();
}


/**
 * Sets the selection box to the appropriate color.
 */
function set_selection_box_color(){

    // If the "D" key is pressed, set the selection box color to the
    // deselection color
    if(d_held) $("#selection-box").css({"background-color": "#000000"});

    // If the "D" key is not pressed, set the selection box to the selection
    // color
    else $("#selection-box").css({"background-color": ""});
}


/**
 * Sets the starting point of the selection box.
 * @param {Event} event: The event which triggered the callback.
 */
let start_mouse_position;
let start_scroll_offset;
function start_selection(event){

    // If the event was a right-click...
    if(event.which !== 1) return;

    // Save the starting mouse position and scroll offset for later use
    start_mouse_position = get_mouse_position(event);
    start_scroll_offset = get_scroll_offset("#table-body");

    // Call "update_selection_box()" on mouse movement and scrolling
    $("#table-body").on("mousemove scroll", update_selection_box);

    // Create the selection box element
    let selection_box = $("#selection-box");
    set_selection_box_color();
    selection_box.css({
        "width": "0",
        "height": "0",
        "opacity": ".4",
        "transition": "opacity .2s, background-color .2s"
    });
}


/**
 * Updates the selection box element's position and size.
 * @param {Event} event: The event which triggered the callback.
 */
let mouse_position;
function update_selection_box(event){

    // Stop mouse click events from propagating to elements outside the table
    // body, as those would cause the "end_selection()" function to be called
    event.stopPropagation();

    // Get the current scroll offset
    let scroll_offset = get_scroll_offset("#table-body");

    // If the event is a mouse movement event, get the mouse position
    if(event.type === "mousemove") mouse_position = get_mouse_position(event);

    // Otherwise, the event is a scroll event. If no previous mouse position
    // was recorded, return
    else if(!mouse_position) return;

    // Otherwise, get the scroll delta and selection start position
    let scroll_delta = point_subtract(scroll_offset, start_scroll_offset);
    let selection_start = point_subtract(start_mouse_position, scroll_delta);

    // Clamp the selection start position to be within the table body
    let table_body_bounding_box = $("#table-body")[0].getBoundingClientRect();

    let table_body_position =
        {x: table_body_bounding_box.left, y: table_body_bounding_box.top};

    let table_body_size =
        {x: table_body_bounding_box.width, y: table_body_bounding_box.height};

    selection_start = point_maximum(point_minimum(selection_start,
        point_add(table_body_position, table_body_size)), table_body_position);

    // Get the selection box position and size
    let position = point_minimum(selection_start, mouse_position);
    let size = point_subtract(point_maximum(
        selection_start, mouse_position), position);

    // Update the selection box's CSS
    let selection_box = $("#selection-box");
    selection_box.css({"left": `${position.x}px`, "top": `${position.y}px`,
        "width": `${size.x}px`, "height": `${size.y}px`});
}


/**
 * Checks that the selection is valid, applies the selection, and cleans up.
 * @param {Event} event: The mouseup event that triggered the callback.
 */
function end_selection(event){

    // If the event was a left mouse button release...
    if(event.which !== 1) return;

    // If there is a valid selection start position...
    if(!start_mouse_position || start_mouse_position.x.isNaN) return;

    // Unbind the update callbacks
    $(window).unbind("mousemove", update_selection_box);
    $("#table-body").unbind("scroll", update_selection_box);

    // Hide the selection box element
    $("#selection-box").css("opacity", "0");

    // Select the appropriate documents
    apply_selection(event);

    // Reset the starting position
    start_mouse_position = {x: NaN, y: NaN};
}


/**
 * Applies the selection.
 * @param {Event} event: The mouseup event that triggered the callback.
 */
function apply_selection(event){

    // Get the current mouse position and scroll offset
    let mouse_position = get_mouse_position(event);
    let window_scroll_offset = get_window_scroll_offset();

    // Get the selection's bounding box
    let scroll_delta = point_subtract(get_scroll_offset(
        "#table-body"), start_scroll_offset);
    let selection_start = point_subtract(start_mouse_position, scroll_delta);
    let selection_minimum = point_minimum(selection_start, mouse_position);
    let selection_maximum = point_maximum(selection_start, mouse_position);

    // For each row in the table...
    let modified = [];
    $(".table-row").each(function(){

        // Get the row element's bounding box
        let bounding_box = $(this)[0].getBoundingClientRect();

        // Check if the row element is within the selection
        if(window_scroll_offset.x+bounding_box.left < selection_maximum.x &&
            window_scroll_offset.x+bounding_box.right > selection_minimum.x &&
            window_scroll_offset.y+bounding_box.top < selection_maximum.y &&
            window_scroll_offset.y+bounding_box.bottom > selection_minimum.y){

            // If the selection would modify the row, add it to the "modified"
            // list
            if(d_held && $(this).hasClass("selected-table-row") ||
                !d_held && !$(this).hasClass("selected-table-row"))
                modified.push($(this));
        }
    });

    // Update the table to represent the selection and get the IDs of the
    // modified documents
    let modified_ids = [];
    for(const element of modified){
        if(d_held) element.removeClass("selected-table-row");
        else element.addClass("selected-table-row");
        modified_ids.push(element.attr("id"));
    }

    // Send a request to apply the selection to the modified documents
    if(modified.length)
        send_request(d_held ? "deactivate" : "activate", modified_ids)
            .fail("Failed to apply the document selection");
}
