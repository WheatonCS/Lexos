/**
 * Initializes the page after it has loaded.
 */
$("document").ready(function(){
    highlight_navbar_button();
    initialize_dropdown_menus();
    initialize_help_section();
    update_active_document_count();

    // Fade the page content in
    $("main").css("opacity", "1");
});


/**
 * Highlights the appropriate navbar button for the current page.
 */
function highlight_navbar_button(){

    switch(window.location.pathname.substring(1)){

        // Upload
        case "upload": highlight_element($("#upload-button")); break;

        // Manage
        case "manage": highlight_element($("#manage-button")); break;

        // Prepare
        case "scrub": case "cut": case "tokenize":
            highlight_element($("#prepare-button")); break;

        // Visualize
        case "word-cloud": case "multicloud": case "bubbleviz": case "rolling-window":
            highlight_element($("#visualize-button")); break;

        // Analyze
        case "statistics": case "dendrogram": case "k-means": case "consensus-tree":
        case "similarity": case "top-words": case "content-analysis":
            highlight_element($("#analyze-button"));
    }
}


/**
 * Highlights the given element.
 *
 * @param {jQuery} element: The element to highlight.
 */
function highlight_element(element){
    element.css("color", "#47BCFF");
}


/**
 * Initializes the navbar dropdown menus.
 */
function initialize_dropdown_menus(){

    // Prepare
    add_dropdown_menu_callback("prepare", [
        ["Scrub", "scrub"],
        ["Cut", "cut"],
        ["Tokenize", "tokenize"]
    ]);

    // Visualize
    add_dropdown_menu_callback("visualize", [
        ["Word Cloud", "word-cloud"],
        ["Multicloud", "multicloud"],
        ["BubbleViz", "bubbleviz"],
        ["Rolling Window", "rolling-window"]
    ]);

    // Analyze
    add_dropdown_menu_callback("analyze", [
        ["Statistics", "statistics"],
        ["Dendrogram", "dendrogram"],
        ["K-Means Clustering", "k-means"],
        ["Consensus Tree", "consensus-tree"],
        ["Similarity Query", "similarity-query"],
        ["Top Words", "top-words"],
        ["Content Analysis", "content-analysis"]
    ]);

    // Remove menus if an outside element was clicked
    $(window).click(remove_dropdown_menus);

    // Stop click propagation on navbar menu button clicks
    $(".navbar-button").each(function(){
       $(this).click(function(event){ event.stopPropagation(); });
    });
}


/**
 * Adds a click callback to toggle the dropdown menu.
 *
 * @param {String} element_name: The name of the navbar elements.
 * @param {List} items: The names and links of the dropdown rows.
 */
function add_dropdown_menu_callback(element_name, items){
    $(`#${element_name}-button`).click(function(){

        let create = !$(`#${element_name}-menu`).length;

        //If any dropdown menus exist, remove them
        remove_dropdown_menus();

        //If the menu does not exist, create it
        if(create){

            // Create the dropdown menu grid
            let menu = $(`<div id="${element_name}-menu" class=`+
                `"navbar-menu"></div>`).insertBefore(
                `#${element_name}-button`);

            // Populate the grid
            for(const item of items){
                let title = item[0];
                let url = item[1];
                $(`<a href="${url}">${title}</a>`).appendTo(menu);
            }

            // Stop click propagation if the menu is clicked
            menu.click(function(event){ event.stopPropagation(); });
        }
    });
}


/**
 * Removes any dropdown menus.
 */
function remove_dropdown_menus(){
    let dropdown_menus = $(".navbar-menu");
    if(dropdown_menus.length)
        dropdown_menus.each(function(){ $(this).remove(); });
}


/**
 * Initializes the help section.
 */
function initialize_help_section(){
    // Set the help button callback
    $("#help-button").click(help_button_callback);

    // Allow the help section to scroll horizontally with the page
    $(window).scroll(function(){
        $("#help").css("right", $(window).scrollLeft()+'px');
    });
}


/**
 * Adds a click callback to show toggle the help menu.
 */
let help_visible = false;
function help_button_callback(){
    let main_grid = $("#main-grid");
    let help_button = $("#help-button");

    // If the help section is visible, close it
    if(help_visible){
        main_grid.css("grid-template-columns", "100%");
        $("#help-section").remove();
        help_button.removeClass("highlight");
        help_visible = false;
        return;
    }

    // Otherwise, show the help section
    main_grid.css("grid-template-columns", "40rem auto");
    let help_section = $(`<div id="help-section"></div>`).prependTo(main_grid);
    help_button.addClass("highlight");

    let url = "/static/help"+window.location.pathname+"-help.html";
    help_section.load(url);
    help_visible = true;
}


/**
 * Updates the active document count element.
 */
function update_active_document_count(){
    request_active_document_count().done(function(response){
        $("#active-document-count").text(response);
    });
}


/**
 * Request the number of active documents
 *
 * @returns {jqXHR}: The response.
 */
function request_active_document_count(){
    return $.ajax({type: "GET", url: "active-documents"});
}


/**
 * Creates a dismissable popup element.
 *
 * @returns {jQuery}: The popup element.
 */
function create_popup(){
    let popup = $(
        `<div id="popup-container">`+
            `<div id="popup">`+
                `<h3 id="popup-close-button" class="selectable">X</h3>`+
                `<div id="popup-content" class="centerer"></div>`+
            `</div>`+
       `</div>`
    ).appendTo("body");

    setTimeout(function(){ popup.css("opacity", "1"); }); // Fade in the popup

    // Close the popup when the close button or the background is clicked
    $("#popup-close-button").click(function(){ close_popup(popup); });
    $("#popup-container").click(function(){ close_popup(popup); });
    $("#popup").click(function(event){ event.stopPropagation(); });

    return popup;
}


/**
 * Removes the given popup.
 */
function close_popup(){
    let popup = $("#popup-container").css("opacity", "0");  // Fade out the popup
    setTimeout(function(){ popup.remove(); });
}


/**
 * Creates a dismissible popup element with a text input and "OK" button.
 *
 * @returns {jQuery}: The popup element.
 */
function create_text_input_popup(){
    let popup = create_popup();

    $(`<input id="popup-input" type="text" spellcheck="false" autocomplete="off">`+
        `<h3 id="popup-ok-button" class="selectable">OK</h3>`
    ).appendTo("#popup-content");

    return popup;
}
