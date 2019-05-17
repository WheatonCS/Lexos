$("document").ready(function(){
    initialize_dropdown_menus();
    initialize_help_section();
});

/* Dropdown menus */
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
        ["Hierarchical Clustering", "dendogram"],
        ["K-Means Clustering", "kmeans"],
        ["Consensus Tree", "bct_analysis"],
        ["Similarity Query"],
        ["Top Words", "topword"],
        ["Content Analysis"]
    ]);

    // Remove menus if an outside element was clicked
    $(window).click(remove_dropdown_menus);

    // Stop click propagation on navbar menu button clicks
    $(".navbar-button").each(function(){
       $(this).click(function(event){ event.stopPropagation(); });
    });
}

function add_dropdown_menu_callback(element_name, items){
    $(`#${element_name}-button`).click(function(){

        let create = !$(`#${element_name}-menu`).length;

        //If any dropdown menus exist, remove them
        remove_dropdown_menus();

        //If the menu did not exist, create it
        if(create) create_dropdown_menu(element_name, items);
    });
}

function create_dropdown_menu(element_name, menu_items){
    console.log(element_name);

    // Create the dropdown menu grid
    let menu = $(`<div id="${element_name}-menu" class=`+
        `"navbar-menu"></div>`).insertBefore(`#${element_name}-button`);

    // Populate the grid
    for(const menu_item of menu_items){
        let title = menu_item[0];
        let url = menu_item[1];
        $(`<a href="${url}">${title}</a>`).appendTo(menu);
    }

    // Stop click propagation if the menu is clicked
    menu.click(function(event){ event.stopPropagation(); });
}

function remove_dropdown_menus()
{
    let dropdown_menus = $(".navbar-menu");
    if(dropdown_menus.length)
        dropdown_menus.each(function(){ $(this).remove(); });
}

/* Help section */
function initialize_help_section()
{
    // Set the help button callback
    $("#help-button").click(help_button_callback);

    // Allow the help section to scroll horizontally with the page
    $(window).scroll(function(){
        $("#help").css("left", '-'+$(window).scrollLeft()+'px');
    });
}

function help_button_callback(){
    let body = $("body");
    let help_button = $("#help-button");
    let expanded = help_button.text() == "Hide Help";

    if(expanded){
        body.css("margin-left", "0");
        $("#help-section").remove();
        help_button.text("Show Help");
        return;
    }

    body.css("margin-left", "40rem");
    let help_section = $(`<div id="help-section"></div>`).appendTo("#help-container");
    help_button.text("Hide Help");

    let url = "/static/help"+window.location.pathname+".html?ver=3.2.0";
    console.log(url);
    help_section.load(url);
}
