/**
 * Initializes the page after it has loaded.
 */
$("document").ready(function(){
    initialize_dropdown_menus();
    initialize_help_section();
    update_active_document_count();

    // Add "scroll to top" button functionality
    $("#scroll-to-top-button").click(function(){
        $("#main-section").animate({scrollTop: 0}, "fast");
    });


    // Fade the page content in
    $("main").css("opacity", "1");
});


/**
 * Initializes the navbar dropdown menus.
 */
function initialize_dropdown_menus(){

    // Prepare
    add_dropdown_menu_callback("prepare", [
        ["Scrub", "scrub"],
        ["Cut", "cut"],
        ["Tokenizer", "tokenizer"]
    ]);

    // Visualize
    add_dropdown_menu_callback("visualize", [
        ["Word Cloud", "wordcloud"],
        ["Multicloud", "multicloud"],
        ["BubbleViz", "viz"],
        ["Rolling Window", "rollingwindow"]
    ]);

    // Analyze
    add_dropdown_menu_callback("analyze", [
        ["Statistics", "statistics"],
        ["Hierarchical Clustering", "dendrogram"],
        ["K-Means Clustering", "kmeans"],
        ["Consensus Tree", "bct_analysis"],
        ["Similarity Query", "similarity"],
        ["Top Words", "topword"],
        ["Content Analysis", "contentanalysis"]
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

        //If the menu did not exist, create it
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
function help_button_callback(){
    let main_grid = $("#main-grid");
    let help_button = $("#help-button");
    let expanded = help_button.text() === "Hide Help";

    // If the help section is expanded, close it
    if(expanded){
        main_grid.css("grid-template-columns", "100%");
        $("#help-section").remove();
        help_button.text("Show Help");
        return;
    }

    // Otherwise, show the help section
    main_grid.css("grid-template-columns", "40rem auto");
    let help_section = $(`<div id="help-section"></div>`).prependTo(main_grid);
    help_button.text("Hide Help");

    let url = "/static/help"+window.location.pathname+"-help.html";
    help_section.load(url);
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
    setTimeout(function(){ popup.remove(); }, 200);
}


/**
 * Creates a dismissable popup element with a text input and "OK" button.
 *
 * @returns {jQuery}: The popup element.
 */
function create_text_input_popup(){
    let popup = create_popup();

    $(`<input id="popup-input" type="text">`+
        `<h3 id="popup-ok-button" class="selectable">OK</h3>`
    ).appendTo("#popup-content");

    return popup;
}
