/**
 * Gets the sum of two point-like objects.
 *
 * @param {{x, y}} a: The first addend.
 * @param {{x, y}} b: The second addend.
 * @returns {{x: number, y: number}}: The product of a and b.
 */
function point_add(a, b){
    return {x: a.x+b.x, y: a.y+b.y};
}


/**
 * Gets the difference of two point-like objects.
 *
 * @param {{x, y}} a: The minuend.
 * @param {{x, y}} b: The subtrahend.
 * @returns {{x: number, y: number}}: The difference of a and b.
 */
function point_subtract(a, b){
    return {x: a.x-b.x, y: a.y-b.y};
}


/**
 * Gets the minimum of two point-like objects.
 *
 * @param {{x, y}} a: The first point.
 * @param {{x, y}} b: The second point.
 * @returns {{x: number, y: number}}: The minimum of a and b.
 */
function point_minimum(a, b){
    return {x: Math.min(a.x, b.x), y: Math.min(a.y, b.y)};
}


/**
 * Gets the maximum of two point-like objects.
 *
 * @param {{x, y}} a: The first point.
 * @param {{x, y}} b: The second point.
 * @returns {{x: number, y: number}}: The maximum of a and b.
 */
function point_maximum(a, b){
    return {x: Math.max(a.x, b.x), y: Math.max(a.y, b.y)};
}


/**
 * Gets the scroll offset of the main section.
 *
 * @returns {{x, y}}: The scroll offset.
 */
function get_main_section_scroll_offset(){
    let main_section = $("#main-section");
    return {x: main_section.scrollLeft(), y: main_section.scrollTop()};
}


/**
 * Gets the scroll offset of the window.
 *
 * @returns {{x, y}}: The scroll offset.
 */
function get_window_scroll_offset(){
    let window_element = $(window);
    return {x: window_element.scrollLeft(), y: window_element.scrollTop()};
}


/**
 * Gets the mouse position relative to the main section.
 *
 * @returns {{x, y}}: The mouse position.
 */
function get_relative_mouse_position(event){
    let main_section = $("#main-section");
    return {x: event.pageX+main_section.scrollLeft(),
        y: event.pageY+main_section.scrollTop()};
}


/**
 * Gets the mouse position relative to the window.
 *
 * @returns {{x, y}}: The mouse position.
 */
function get_mouse_position(event){
    return {x: event.pageX, y: event.pageY};
}


/**
 * Gets the size of the window in pixels.
 *
 * @returns {{x, y}}: The size of the window.
 */
function get_window_size(){
    let window_element = $(window);
    return {x: window_element.width(), y: window_element.height()};
}
