/**
 * Creates a popup.
 * @param {string} title: The title to display on the popup.
 * @returns {jQuery}: The popup element.
 */
function create_popup(title){
    let popup_container_element = $(`
        <div id="popup-container">
            <div id="popup">
                <div class="vertical-splitter">
                    <h3 class="title">${title}</h3>
                    <h3 id="popup-close-button" class="right-justified selectable">X</h3>
                </div>
                <div id="popup-content"></div>
            </div>
       </div>
    `).appendTo("body");

    // Fade in the popup
    fade_in("#popup-container");

    // Close the popup when the close button or the background is clicked
    $("#popup-close-button").click(close_popup);
    popup_container_element.click(close_popup);

    // Prevent click events from propagating to the popup container and thus
    // closing the popup undesirably
    return $("#popup").click(function(event){ event.stopPropagation(); });
}


/**
 * Fades out and removes the given popup.
 */
function close_popup(){
    let popup = $("#popup-container").css("opacity", "0");
    setTimeout(function(){ popup.remove(); });
}


/**
 * Creates a popup with an "OK" button.
 * @param {string} title: The title to display on the popup.
 * @returns {jQuery}: The popup element.
 */
function create_ok_popup(title){
   let popup_element = $(`<h3 id="popup-ok-button" class="button">OK</h3>`);
    popup_element.appendTo(create_popup(title));
    return popup_element;
}


/**
 * Creates a popup with a text input and "OK" button.
 * @param {string} title: The popup element.
 * @returns {jQuery}: The popup element.
 */
function create_text_input_popup(title){
    let popup_element = create_ok_popup(title);
    $(`<input id="popup-input" type="text" spellcheck="false" autocomplete="off">`)
        .appendTo("#popup-content");
    return popup_element;
}


/**
 * Creates a popup containing radio button options.
 * @param {string} title: The title to display on the popup.
 * @param {string} radio_buttons_name: The name of the radio buttons.
 * @param {string} display_element_query: The query for the element to display
 *      the  selected option's text on.
 * @param {string} input_element_query: The query for the input element whose
 *      value  will be set to the selected option.
 * @param {string[][]} options: The value and text of each radio button.
 */
function create_radio_options_popup(title, radio_buttons_name,
    display_element_query, input_element_query, options){

    // Get the currently set option from the input element
    let input_element = $(input_element_query);
    let set_option = input_element.val();

    // Create the popup
    let popup = create_popup(title).addClass("radio-button-popup");
    let popup_content = $("#popup-content")
        .addClass("radio-button-options-popup");

    // For each option...
    for(const option of options) {

        // Create the radio button
        let element = $(`
            <div>
                <label class="circle-label">
                    <input type="radio" name="${radio_buttons_name}" value="${option[0]}">
                    <span>${option[1]}</span>
                </label>
            </div>
        `).appendTo(popup_content);

        // Check the currently set option's radio button
        if(set_option === option[0])
            element.find("input").prop("checked", true);
    }

    $(`<h3 id="ok-button" class="button">OK</h3>`).appendTo("#popup");

    // If the "OK" button is pressed, set the input element's value, the
    // display element's text, and close the popup
    $("#ok-button").click(function(){
        let selected_element = $(`input[name="${radio_buttons_name}"]:checked`);
        input_element.val(selected_element.val());
        $(display_element_query).text(selected_element
            .closest("div").find("span").html());
        close_popup();
    });

    return popup;
}
