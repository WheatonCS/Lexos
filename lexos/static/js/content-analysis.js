$(function(){

    // If the "Upload" button was clicked...
    $("#dictionaries-section #upload-button").click(function(){

        // Click the file input element
        let file_input_element = $("#file-input");
        file_input_element.click();
    });

    // If files were selected for upload, upload the files
    $("#file-input").change(upload_files);

    // Initialize the formula section button callbacks
    initialize_button_callbacks();

    // If the "Analyze" button is pressed...
    $("#formula-section #analyze-button").click(function(){

        // Display the loading overlays and disable the "Upload" and "Analyze"
        // buttons
        start_loading("#overview-body, #corpus-body, #documents-body",
            `#formula-section #analyze-button, #dictionaries-section
            #upload-button, #overview-download-button,
            #corpus-download-button`);

        // Remove any existing error messages
        remove_errors();

        // Send a request to analyze the files
        send_ajax_form_request("/content-analysis/analyze",
            {formula: $("#formula-textarea").val()})

            // If the request was successful, display the results
            .done(display_results)

            // If the request failed, display an error message and remove the
            // loading overlay
            .fail(function(){
                error("Failed to perform the analysis.");
                finish_loading("#results-container", "", `#formula-section
                    #analyze-button, #dictionaries-section #upload-button`);
            });
    });

    // Initialize the tooltips
    initialize_tooltips();
});


/**
 * Initialize the formula section button callbacks.
 */
function initialize_button_callbacks(){

    let formula_element = $("#formula-textarea");

    // If a number pad or operations pad button is clicked, add the
    // appropriate text
    $("#number-pad h3, #operations-pad h3").each(function(){

        $(this).click(function(){

            let text = $(this).text();
            let formula = formula_element.val();

            // If the "DEL" button was pressed...
            if(text === "DEL"){

                // If the deleted character is the end of a document label,
                // delete the entire document label
                let last_character = formula.slice(-1);
                if(last_character === ']')
                    formula = formula.slice(0, formula.lastIndexOf('['));

                // Otherwise, delete a single character
                else formula = formula.slice(0, -1);
            }

            // If the "CLR" button was pressed, clear the formula
            else if(text === "CLR") formula = '';

            // If the "X" or "^" button was pressed, append the appropriate
            // text
            else if(text === 'X') formula += '*';
            else if(text === '^') formula += "^(";

            // Otherwise, append the text shown on the button
            else formula += text;

            formula_element.val(formula);
        });
    });
}


/**
 * Upload files.
 * @param {event} event: The event that triggered the callback.
 */
let files = [];
function upload_files(){

    // Remove any existing error messages
    remove_errors();

    // Display the loading overlay
    start_loading(".dictionaries-wrapper",
        "#dictionaries-section #upload-button");

    // Send a request to upload the files
    send_ajax_request("/content-analysis/upload-dictionaries")

        // If the request is successful, create the upload previews
        .done(create_upload_previews)

        // If the request failed, display an error
        .fail(function(){ error("Upload failed."); });
}


/**
 * Create the upload previews.
 * @param {string} response: The response from the
 *      "/content-analysis/upload-dictionaries" request.
 */
function create_upload_previews(response)
{
    // Create the upload previews
    let uploads = JSON.parse(response);
    $(`<div class="hidden dictionaries"></div>`)
        .appendTo(".dictionaries-wrapper");

    for(const upload of uploads)
        $(`<h3>${upload}</h3>`).appendTo(".dictionaries");

    // Create the callbacks for the formula section document buttons
    let formula_element = $("#formula-textarea");
    $("#documents-pad h3:not(.centerer)").each(function(){

        $(this).click(function(){
            formula_element.val(formula_element.val()+`[${$(this).text()}]`);
        });
    });

    // Remove the loading overlay, show the dictionary buttons, and
    // enable the "Upload" button
    finish_loading(".dictionaries-wrapper", ".dictionaries",
        "#dictionaries-section #upload-button");
}


/**
 * Displays the results.
 * @param {string} response: The response from the
 *      "/content-analysis/analyze" request.
 */
function display_results(response){
    response = JSON.parse(response);

    // Check for errors
    let error_message = response["error"];
    if(error_message){
        error(error_message);
        finish_loading("#results-container", '', `#formula-section
            #analyze-button, #dictionaries-section #upload-button`);
        return;
    }

    // Create the overview table
    let overview = response["overview"];
    let head = overview[0];
    let data = overview.splice(1);
    console.log(head, data);
    create_table("#overview-body", data, head);

    // Create the corpus table
    create_table("#corpus-body", response["corpus"],
        ["Dictionary", "Phrase", "Count"]);

    // Create the document tables
    $(`<div id="document-tables-grid""></div>`).appendTo("#documents-body");

    for(const document of response["documents"])
        create_table("#document-tables-grid", document["table"],
            ["Dictionary", "Phrase", "Count"], document["name"]);

    // Initialize the download buttons
    $("#overview-download-button").click(function(){
        download(response["overview-csv"], "analysis-overview.csv");
    });

    $("#corpus-download-button").click(function(){
        download(response["corpus-csv"], "analysis-corpus.csv");
    });

    // Remove the loading overlay and enable the
    // "Upload", "Analyze", and "Download" buttons
    finish_loading("#overview-body, #corpus-body, #documents-body",
        `#overview-body .lexos-table, #corpus-body .lexos-table,
        #document-tables-grid .lexos-table`, `#formula-section
        #analyze-button, #dictionaries-section #upload-button,
        #overview-download-button, #corpus-download-button`);
}


/**
 * Sends an AJAX request containing the file inputs.
 * @param {string} url: The URL to send the request to.
 * @returns {jqXHR}: The jQuery AJAX request.
 */
function send_ajax_request(url){

    return $.ajax({
        type: "POST",
        url: url,
        processData: false,
        contentType: false,
        data: new FormData($("form")[0])
    })
}


/**
 * Initialize the tooltips.
 */
function initialize_tooltips(){
    create_tooltip("#dictionaries-tooltip-button", `Upload a text file
        containing a comma-separated list of key words and phrases associated
        with the characteristic to test. For example, if one is analyzing
        sentiment, a positive file might include: "happy, very happy, great,
        good".`);
    create_tooltip("#formula-tooltip-button", `Create a formula that uses the
        dictionaries to compute a final score. For example: "[happy] –
        [sad]".`, true);
    create_tooltip("#corpus-tooltip-button", `The top 100 words are displayed.
        For a list of all of the words, click the "Download" button.`, true);
    create_tooltip("#documents-tooltip-button", `The top 100 words are
        displayed for each document.`, true);
}
