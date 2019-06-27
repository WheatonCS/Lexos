$("document").ready(function(){

    // Highlight the navbar button of the current page
    highlight_navbar_button();

    // Initialize the theme popup
    initialize_theme_popup();

    // If the "Help" button is pressed, toggle the help section visibility
    $("#help-button").click(function(){
        toggle_help_section()
        update_graph_size()
    });

    // If the navbar walkthrough button is pressed, begin the walkthrough
    $("#navbar-walkthrough-button").click(start_walkthrough);

    // Initialize the navbar dropdown menus
    initialize_dropdown_menus();

    // Fade in the page
    $("body").css({transition: '', opacity: '1'});
});


/**
 * Initializes the theme.
 */
function initialize_theme_popup(){

    // If the Lexos logo is clicked...
    $("#lexos-dragon, #lexos-text").click(function(){

        // Create a theme popup
        display_radio_options_popup("Theme", "theme", theme,
            [
                ["default", "Default"],
                ["grey", "Grey"],
                ["grey-dark", "Grey Dark"],
                ["mint", "Mint"],
                ["mint-dark", "Mint Dark"],
                ["solarized-light", "Solarized Light"],
                ["solarized-dark", "Solarized Dark"]
            ], set_theme);
    });
}


/**
 * Sets the theme.
 * @param {string} selected_theme: The theme to set.
 */
function set_theme(selected_theme){

    // Send a request to set the theme
    send_ajax_request("/set-theme", {theme: selected_theme})

        // If the request was successful, update the theme and
        // reload the page
        .done(function(){
            theme = selected_theme;
            location.reload();
        })

        // If the request failed, display an error message
        .fail(function(){ error("Failed to set the theme."); });
}


/**
 * Highlights the appropriate navbar button for the current page.
 */
function highlight_navbar_button(){

    switch(window.location.pathname.substring(1)){

        // "Upload"
        case "upload": highlight($("#upload-button")); break;

        // "Manage"
        case "manage": highlight($("#manage-button")); break;

        // "Prepare"
        case "scrub": case "cut": case "tokenize":
            highlight($("#prepare-button")); break;

        // "Visualize"
        case "word-cloud": case "multicloud": case "bubbleviz": case "rolling-window":
            highlight($("#visualize-button")); break;

        // "Analyze"
        case "statistics": case "dendrogram": case "k-means": case "consensus-tree":
        case "similarity": case "top-words": case "content-analysis":
            highlight($("#analyze-button"));
    }
}


/**
 * Highlights the given element.
 * @param {jQuery} element: The element to highlight.
 */
function highlight(element){
    element.addClass("highlight");
}


/**
 * Initializes the navbar dropdown menus.
 */
function initialize_dropdown_menus(){

    // "Prepare"
    add_dropdown_menu_callback("prepare", [
        ["Scrub", "scrub"],
        ["Cut", "cut"],
        ["Tokenize", "tokenize"]
    ]);

    // "Visualize"
    add_dropdown_menu_callback("visualize", [
        ["Word Cloud", "word-cloud"],
        ["Multicloud", "multicloud"],
        ["BubbleViz", "bubbleviz"],
        ["Rolling Window", "rolling-window"]
    ]);

    // "Analyze"
    add_dropdown_menu_callback("analyze", [
        ["Statistics", "statistics"],
        ["Dendrogram", "dendrogram"],
        ["K-Means", "k-means"],
        ["Consensus Tree", "consensus-tree"],
        ["Similarity Query", "similarity-query"],
        ["Top Words", "top-words"],
        ["Content Analysis", "content-analysis"]
    ]);

    // Remove the menu if an outside element was clicked
    $(window).click(remove_dropdown_menus);

    // Stop click propagation on navbar menu button clicks so that the menu
    // is not removed undesirably
    $(".navbar-button").each(function(){
       $(this).click(function(event){ event.stopPropagation(); });
    });
}


/**
 * Adds a click callback to toggle the dropdown menu.
 * @param {string} element_name: The name of the navbar elements.
 * @param {list} items: The names and links of the dropdown rows.
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
 * Toggles the visibility of the help section.
 */
let help_visible = false;
let walkthrough_callback = null;
function toggle_help_section(){

    // If the help section is visible, close it and return
    if(help_visible){
        close_help_section();
        return;
    }

    // Otherwise, create the help section
    let main_grid = $("#main-grid").css("grid-template-columns", "40rem auto");

    $(`
        <div id="help-section" class="invisible">
            <div id="help-section-navbar">
                <span id="walkthrough-button" class="left-justified help-button">Page Walkthrough</span>
                <span id="page-help-button" class="right-justified help-button">Page Help</span>
                <span id="glossary-button" class="left-justified help-button">Help Glossary</span>
                <span id="about-button" class="right-justified help-button">About Lexos</span>
            </div>
            <div id="help-section-content"></div>
        </div>
    `).prependTo(main_grid);

    $("#help-button").addClass("highlight");

    help_visible = true;
    let help_content_element = $("#help-section-content");
    help_content_element.load(
        "/static/help"+window.location.pathname+"-help.html");

    // Initialize the help section's buttons
    $("#glossary-button").click(function(){
        help_content_element.load("/static/help/glossary-help.html");
    });

    $("#about-button").click(function(){
        help_content_element.load("/static/help/about-help.html");
    });

    $("#page-help-button").click(function(){
        help_content_element.load(
            "/static/help"+window.location.pathname+"-help.html");
    });

    $("#walkthrough-button").click(function(){
        close_help_section();
        start_walkthrough();
    });

    // Fade in the help section
    fade_in("#help-section", ".5s");
}


/**
 * Closes the help section.
 */
function close_help_section(){
    $("#main-grid").css("grid-template-columns", "100%");
    $("#help-section").remove();
    $("#help-button").removeClass("highlight");
    help_visible = false;
}


/**
 * Starts the walkthough.
 */
function start_walkthrough(){
    walkthrough_callback();
    $(".introjs-prevbutton").text("Back");
    $(".introjs-nextbutton").text("Next");
    $(".introjs-tooltip").css("opacity", "1");
}


/**
 * Binds the walkthrough callback.
 * @param {function} walkthrough: The walkthrough callback to bind.
 */
function initialize_walkthrough(walkthrough){
    walkthrough_callback = walkthrough;
}


/**
 * Update the number of active documents displayed after the "Active
 * Documents" text in the footer
 */
function update_active_document_count(){

    return $.ajax({type: "GET", url: "active-documents"})
        .done(function(response){
            active_document_count = parseInt(response);
            $("#active-document-count").text(response);
        })

    .fail(function(){ error("Failed to update the active document count."); });
}
