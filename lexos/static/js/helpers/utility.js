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
 * @returns {String}: The form as a JSON string.
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
 */
function add_text_overlay(query, text){
    $(query).each(function(){

        let element = $(this);
        element.empty();

        let text_element = $(`
            <div class="centerer" style="opacity: 0; transition: opacity .5s">
                <h3>${text}</h3>
            </div>
        `).appendTo(element);

        setTimeout(function(){ text_element.css("opacity", "1"); });
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
    $(disable_query).each(function(){
        $(this).addClass("disabled");
    });

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
 * @param {number} sequential_fade_in_delay: The delay between fading in
 *      subsequent elements.
 */
function finish_loading(loading_overlay_query, show_query,
    enable_query = "", sequential_fade_in_delay = 0){

    // Remove the loading overlay from each specified element
    $(loading_overlay_query).each(function(){
        $(this).find(".loading-overlay").remove();
    });

    // Enable each specified element
    enable(enable_query);

    // Fade in each specified element
    let accumulated_fade_in_delay = 0;
    $(show_query).each(function(){

        let element = $(this);

        // Set the element's opacity to 0
        element.css({"transition": "none", "opacity": "0"});

        // Show the element
        element.removeClass("hidden");

        // Fade the element after a delay
        setTimeout(function(){
            element.css({"transition": "opacity .5s", "opacity": "1"});
        }, accumulated_fade_in_delay+30);

        accumulated_fade_in_delay += sequential_fade_in_delay;
    });
}

/**
 * Enables the specified elements.
 * @param {string} enable_query: The query for elements to enable.
 */
function enable(enable_query){
    $(enable_query).each(function(){
        $(this).removeClass("disabled");
    });
}


/**
 * Fades in the elements found in the query.
 * @param {string} query: The query for elements to fade in.
 */
function fade_in(query){
    $(query).each(function(){

        let element = $(this);

        // Set the opacity to 0
        element.css({"transition": "none", "opacity": "0"});

        // Fade the element in
        setTimeout(function(){
           element.css({"transition": "opacity .5s", "opacity": "1"});
        });
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
