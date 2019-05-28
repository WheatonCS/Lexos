/**
 * Gets the sum of two point-like objects.
 * @param {{x, y}} a: The first addend.
 * @param {{x, y}} b: The second addend.
 * @returns {{x: number, y: number}}: The product of a and b.
 */
function point_add(a, b){
    return {x: a.x+b.x, y: a.y+b.y};
}


/**
 * Gets the difference of two point-like objects.
 * @param {{x, y}} a: The minuend.
 * @param {{x, y}} b: The subtrahend.
 * @returns {{x: number, y: number}}: The difference of a and b.
 */
function point_subtract(a, b){
    return {x: a.x-b.x, y: a.y-b.y};
}


/**
 * Gets the minimum of two point-like objects.
 * @param {{x, y}} a: The first point.
 * @param {{x, y}} b: The second point.
 * @returns {{x: number, y: number}}: The minimum of a and b.
 */
function point_minimum(a, b){
    return {x: Math.min(a.x, b.x), y: Math.min(a.y, b.y)};
}


/**
 * Gets the maximum of two point-like objects.
 * @param {{x, y}} a: The first point.
 * @param {{x, y}} b: The second point.
 * @returns {{x: number, y: number}}: The maximum of a and b.
 */
function point_maximum(a, b){
    return {x: Math.max(a.x, b.x), y: Math.max(a.y, b.y)};
}


/**
 * Gets the scroll offset of the main section.
 * @returns {{x, y}}: The scroll offset.
 */
function get_main_section_scroll_offset(){
    let main_section = $("#main-section");
    return {x: main_section.scrollLeft(), y: main_section.scrollTop()};
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
 * Gets the mouse position relative to the main section.
 * @returns {{x, y}}: The mouse position.
 */
function get_relative_mouse_position(event){
    let main_section = $("#main-section");
    return {x: event.pageX+main_section.scrollLeft(),
        y: event.pageY+main_section.scrollTop()};
}


/**
 * Gets the mouse position relative to the window.
 * @returns {{x, y}}: The mouse position.
 */
function get_mouse_position(event){
    return {x: event.pageX, y: event.pageY};
}


/**
 * Gets the size of the window in pixels.
 * @returns {{x, y}}: The size of the window.
 */
function get_window_size(){
    let window_element = $(window);
    return {x: window_element.width(), y: window_element.height()};
}


/**
 * Gets the form as a JSON string.
 * @returns {String}: The form as a JSON string.
 */
function get_form_json(){
    return JSON.stringify($("form").serializeArray()
        .reduce(function(a, x){ a[x.name] = x.value; return a; }, {}))
}


/**
 * Sends an AJAX request with a JSONified form payload.
 * @param url: The URL to send the request to.
 * @returns {jqXHR}: The jQuery request object.
 */
function send_ajax_form_request(url){
    return $.ajax({
        type: "POST",
        url: url,
        contentType: "application/json; charset=utf-8",
        data: get_form_json()
    });
}


/**
 * Adds a text overlay to the given element.
 * @param {string} element_query: The element to query for.
 * @param {string} text: The text to show.
 * @param {boolean} empty: Whether to empty the element's contents.
 */
function add_text_overlay(element_query, text, empty=true){
    let element = $(element_query);
    if(empty) element.empty();
    $(`
        <div class="centerer">
            <h3>${text}</h3>
        </div>
    `).appendTo(element);
}


/**
 * Adds a text overlay to the given elements.
 * @param {string[]} element_queries: The elements to query for.
 * @param {string} text: The text to show.
 * @param {boolean} empty: Whether to empty the element's contents.
 */
function batch_add_text_overlay(element_queries, text, empty=true){
    for(const element_query of element_queries)
        add_text_overlay(element_query, text, empty);
}


/**
 * Adds a loading overlay to the given element.
 * @param {string} element_query: The element to query for.
 * @param {boolean} empty: Whether to empty the element's contents.
 */
function add_loading_overlay(element_query, empty=true){
    let element = $(element_query);
    if(empty) element.empty();
    $(`
        <div class="centerer">
            <h3>Loading</h3>
        </div>
    `).appendTo(element);
}


/**
 * Adds a loading overlay to the given elements.
 * @param {string[]} element_queries: The elements to query for.
 * @param {boolean} empty: Whether to empty the element's contents.
 */
function batch_add_loading_overlay(element_queries, empty=true){
    for(const element_query of element_queries)
        add_loading_overlay(element_query, empty);
}


/**
 * Fades in the given element.
 * @param {string} element_query: The element to query for.
 */
function fade_in(element_query){
    let element = $(element_query);
    element.css("opacity", "0");
    setTimeout(function(){
        element.css({"transition": "opacity .2s", "opacity": "1"});
    }, 100);
}


/**
 * Fades in the given elements.
 * @param {string[]} element_queries: The elements to query for.
 */
function batch_fade_in(element_queries){
    for(const element_query of element_queries)
        fade_in(element_query);
}
