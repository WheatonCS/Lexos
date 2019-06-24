let table;
$(function(){

    // Initialize the table
    table = new Table("tokenizer", "tokenize/table", "#table-section", "",
        validate_analyze_inputs, null, true, true, false, true, true, true,
        true);

    // Initialize the legacy form inputs and create the table
    get_active_file_ids(initialize, "#tokenizer-table-body");

    //Initialize the "Orientation" tooltip
    create_tooltip("#orientation-tooltip-button", `This option will not be
        represented in the table below, but will be applied to the file sent
        when the "Download" button is clicked.`);

    // Initialize the tooltips
    initialize_analyze_tooltips();

    // Initialize the walkthrough
    initialize_walkthrough(walkthrough);
})


/**
 * Initializes the legacy inputs and creates the token table.
 * @param {string} response: The response from the "active-file-ids" request.
 */
function initialize(response){

    // Initialize the legacy inputs
    if(!initialize_legacy_inputs(response)){

        // If there are no active documents, display "No Active Documents"
        // text and return
        add_text_overlay(".lexos-table-body", "No Active Documents");
        return;
    }

    // Create the token table
    table.create();
}


/**
 * Initializes the walkthrough.
 */
function walkthrough(){

    let intro = introJs();
    intro.setOptions({steps: [
        {
            intro: `Welcome to Tokenize!`,
            position: "top",
        },
        {
            element: "#orientation-section",
            intro: `Here you can select how your
                documents are oriented. Note that "Documents as Rows, Terms as
                Columns" only applies to the downloaded CSV file.`,
            position: "top",
        },
        {
            element: "#tokenize-section",
            intro: `Tokenize determines how terms are counted when generating
                data.`,
            position: "top",
        },
        {
            element: "#normalize-section",
            intro: `Normalize determines if and how term totals are weighted.`,
            position: "top",
        },
        {
            element: "#cull-section",
            intro: `Cull limits the number of terms used to generate data and
                is optional.`,
            position: "top",
        },
        {
            element: "#table-section",
            intro: `Here is your generated data table from the options
                selected above.`,
            position: "top",
        },
        {
            element: "#sort-buttons",
            intro: `You can sort your data table with these options, and by
                clicking column headers on the data table.`,
            position: "top",
        },
        {
            element: "#tokenize-buttons",
            intro: `Here you can generate a data table. You can also choose to
                download the data table as a CSV file.`,
            position: "top",
        },
        {
            intro: `This concludes the Tokenize walkthrough!`,
            position: "top",
        }
    ]});

    intro.start();
}
