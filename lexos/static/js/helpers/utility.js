/**
 * Gets the scroll offset of the given element.
 * @param {string} query: The element to query for.
 * @returns {{x, y}}: The scroll offset.
 */
function get_scroll_offset(query){
    let element = $(query);
    return {x: element.scrollLeft(), y: element.scrollTop()};
}


/**
 * Gets the scroll offset of the window.
 * @returns {{x, y}}: The scroll offset.
 */
function get_window_scroll_offset(){
    let window_element = $(window);
    return {x: window_element.scrollLeft(), y: window_element.scrollTop()};
}

/**
 * Gets the mouse position relative to the window.
 * @returns {{x, y}}: The mouse position.
 */
function get_mouse_position(event){
    return {x: event.pageX, y: event.pageY};
}


/**
 * Gets the form as a JSON string.
 * @param {object} additional_entries: Additional entries to append to the
 *      form.
 * @returns {string}: The form as a JSON string.
 */
function get_form_json(additional_entries = {}){

    // Serialize the form
    let form = $("form").serializeArray()
        .reduce(function(a, x){ a[x.name] = x.value; return a; }, {});

    // Add the additional entries
    for(const [key, value] of Object.entries(additional_entries))
        form[key] = value;

    // Return the form JSON
    return JSON.stringify(form)
}


/**
 * Sends an AJAX request with a JSONified form payload.
 * @param {string} url: The URL to send the request to.
 * @param {object} additional_entries: Additional entries to append to the
 *      form.
 * @returns {jqXHR}: The jQuery request object.
 */
function send_ajax_form_request(url, additional_entries = {}){
    return $.ajax({
        type: "POST",
        url: url,
        contentType: "application/json; charset=utf-8",
        data: get_form_json(additional_entries)
    });
}


/**
 * Adds a text overlay to the elements found in the query.
 * @param {string} query: The element to query for.
 * @param {string} text: The text to show.
 * @param {boolean} fade_in: Whether to fade in the text or not.
 */
function add_text_overlay(query, text, fade_in = false){
    $(query).each(function(){

        // Remove any existing content
        $(this).empty();

        // Create the text
        let text_element = $(`
            <div class="centerer">
                <h3>${text}</h3>
            </div>
        `).appendTo(this);

        // Fade in the text
        if(fade_in){
            text_element.css({"opacity": "0", "transition": "opacity .5s"});
            setTimeout(function(){ text_element.css("opacity", "1"); }, 100);
        }
    });
}


/**
 * Adds a loading overlay to the elements found in the query and disables the
 *      specified elements.
 * @param {string} query: The query for elements to add the loading overlay to.
 * @param {string} disable_query: The query for elements to disable.
 */
function start_loading(query, disable_query = ""){

    // Disable the specified elements
    disable(disable_query);

    // Add a loading overlay to the specified elements
    $(query).each(function(){

        let element = $(this);
        element.empty();

        let loading_overlay_element = $(`
            <div class="loading-overlay centerer" style="opacity: 0; transition: opacity .5s">
                <h3>Loading</h3>
            </div>
        `).appendTo(element);

        setTimeout(function(){ loading_overlay_element.css("opacity", "1"); });
    });
}


/**
 * Removes the loading overlay and fades in the loaded elements.
 * @param {string} loading_overlay_query: The query for the element containing
 *      the loading overlay to remove.
 * @param {string} show_query: The query for elements to show.
 * @param {string} enable_query: The query for elements to enable.
 *      subsequent elements.
 */
function finish_loading(loading_overlay_query,
    show_query, enable_query = ""){

    // Remove the loading overlay from each specified element
    $(loading_overlay_query).each(function(){
        $(this).find(".loading-overlay").remove();
    });

    // Enable each specified element
    enable(enable_query);

    // Fade in each specified element
    fade_in(show_query, ".5s");
}


/**
 * Disables the specified elements.
 * @param {string} query: The query for elements to disable.
 */
function disable(query){
    $(query).each(function(){ $(this).addClass("disabled"); });
}


/**
 * Enables the specified elements.
 * @param {string} query: The query for elements to enable.
 */
function enable(query){
    $(query).each(function(){ $(this).removeClass("disabled"); });
}


/**
 * Shows the specified elements.
 * @param {string} query: The query for elements to show.
 */
function show(query){
    $(query).each(function(){ $(this).removeClass("hidden"); });
}


/**
 * Hides the specified elements.
 * @param {string} query: The query for elements to hide.
 */
function hide(query){
    $(query).each(function(){ $(this).addClass("hidden"); });
}


/**
 * Fades in the elements found in the query.
 * @param {string} query: The query for elements to fade in.
 * @param {string} duration: The CSS duration of the fade in.
 * @param {number} sequential_delay: The delay between fading in
 *      subsequent elements.
 */
function fade_in(query, duration = ".2s", sequential_delay = 0){

    let accumulated_fade_in_delay = 0;
    $(query).each(function(){

        let element = $(this);

        // Set the element's opacity to 0
        element.css({"transition": "none", "opacity": "0"});

        // Show the element
        element.removeClass("hidden");

        // Fade the element after a delay
        setTimeout(function(){
            element.css({"transition":
                `opacity ${duration}`, "opacity": "1"});
        }, accumulated_fade_in_delay+30);

        accumulated_fade_in_delay += sequential_delay;
    });
}


/**
 * Converts rem to px.
 * @param {number} rem: The number of rem.
 * @returns {number}: The number of px.
 */
let px_per_rem = parseInt(getComputedStyle(document.documentElement).fontSize);
function rem_to_px(rem){ return rem*px_per_rem; }


/**
 * Registers a callback for a given key.
 * @param {string} key: The uppercase name of the key.
 * @param {function} callback: The function to call.
 */
function key_callback(key, callback){

    // Register the key press callback
    key_down_callback(key, callback);

    // Register the key release callback
    $(window).keyup(function(event){
        if(event.key.toUpperCase() === key) callback(event, false);
    });
}

/**
 * Registers a callback for a given key press.
 * @param {string} key: The uppercase name of the key.
 * @param {function} callback: The function to call.
 */
function key_down_callback(key, callback){

    // Register the key press callback
    $(window).keydown(function(event){
        if(event.key.toUpperCase() === key &&
            !event.originalEvent.repeat) callback(event, true);
    });
}


/**
 * Displays an error message.
 * @param {string} message: The message to display.
 */
function error(message){

    // Remove any existing error message
    $("#error-section").remove();

    // Hide the footer
    hide("footer");

    // Create the error message
    $(`
        <div id="error-section">
            <h3 id="error-text">${message}</h3>
            <h3 id="error-text-2">${message}</h3>
            <div id="error-button-container">
                <h3 id="error-close-button" class="right-justified button">Dismiss</h3>
            </div>
        </div>
    `).appendTo("body");

    // Fade in the error message
    fade_in("#error-section");

    // If the error message's "Dismiss" button is pressed, close the error
    // message and fade in the footer
    $("#error-close-button").click(function(){
        $("#error-section").remove();
        fade_in("footer");
    });
}


/**
 * Parses the given JSON string and returns the parsed object.
 * @param {string} json: The JSON string to parse.
 * @returns {any}: The parsed object.
 */
function parse_json(json){
    return JSON.parse(json.replace(/\bNaN\b/g, "\"N/A\""));
}


/**
 * Validates an integer input.
 * @param {string} number: The value to validate.
 * @param {number} minimum: The minimum value the number can be.
 * @param {number} maximum: The maximum the value can be.
 * @returns {boolean}: Whether the value is valid.
 */
function validate_number(number, minimum = null, maximum = null){

    // Check that the value is a number
    let parsed_value = +number;
    if(!number || isNaN(parsed_value)) return false;

    // Check that the number is within bounds
    if(minimum !== null && parsed_value < minimum) return false;
    if(maximum !== null && parsed_value > maximum) return false;

    // Return true as all validation checks have passed
    return true;
}


/**
 * Creates a tooltip.
 * @param {string} query: The query for the tooltip button element to append
 *      the tooltip to.
 * @param {string} text: The text to display on the tooltip.
 * @param {boolean} on_right_edge: Whether the tooltip on on the right edge and
 *      thus needs to be translated to the left.
 */
function create_tooltip(query, text, on_right_edge = false){

    let id = get_uuid();
    $(query).click(function(event){

        // Stop propagation so that the tooltip isn't removed undesirably
        event.stopPropagation();

        // If any tooltips exist, remove them. If the clicked button's
        // tooltip was removed, return
        let tooltip_element = $(".lexos-tooltip");
        if(tooltip_element.length){
            let toggled = $(`#${id}`).length;
            console.log(toggled);
            remove_tooltips();
            if(toggled) return;
        }

        // Otherwise, create the tooltip
        $(this).addClass("button-active");
        tooltip_element = $(`
            <div id="${id}" class="hidden lexos-tooltip">
                <h3>${text}</h3>
            </div>
        `).insertAfter(this);

        // If the tooltip is on the right edge, give it the corresponding
        // class
        if(on_right_edge) tooltip_element.addClass("right-edge-tooltip");

        // Set the tooltip position
        let button_element = $(this);
        reposition_tooltip(tooltip_element, button_element);

        // Fade in the tooltip
        fade_in(".lexos-tooltip", ".2s");

        // Stop propagation so that the tooltip isn't removed undesirably
        tooltip_element.click(function(event){
            event.stopPropagation();
        });

        // If the window is resized, reposition the tooltip
        $(window).resize(function(){
            reposition_tooltip(tooltip_element, button_element);
        });

        // If there is a click outside of the tooltip, remove the tooltip
        $("body").click(remove_tooltips);
    });
}


/**
 * Removes any existing tooltips.
 */
function remove_tooltips(){

    $(".button-active").removeClass("button-active");
    $(".lexos-tooltip").remove();
}


/**
 * Repositions the tooltip.
 * @param {jQuery} tooltip_element: The tooltip to reposition.
 * @param {jQuery} button_element: The button element to position the tooltip
 *      relative to.
 */
function reposition_tooltip(tooltip_element, button_element){
    let position = button_element.offset();
    tooltip_element.css({"top": `${position.top}px`,
        "left": `${position.left}px`});
}


/**
 * Generates a UUID.
 * @param {number} length: The number of characters in the UUID.
 * @returns {string}: The UUID.
 */
function get_uuid(length = 16){
    let result = "";
    for(let i = 0; i < length; ++i) result += Math.trunc(Math.random()*9);
    return result;
}
