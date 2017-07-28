# Library File Maintenance Guide

Template files now load external libraries from `static/node_modules`. These libraries are maintained using `npm`. A record of the installation commands used is maintained below.

As long as the `package.json` file is unchanged, the entire sequence can be achieved by running `npm install`.

## For `base.html`

- npm install jquery@2.2.4
- npm install bootstrap@3
- npm install smartmenus
- npm install font-awesome

## For DataTables

- npm install datatables.net
- npm install datatables.net-bs
- npm install datatables.net-buttons
- npm install datatables.net-buttons-bs
- npm install datatables.net-fixedcolumns
- npm install datatables.net-fixedcolumns-bs
- npm install datatables.net-fixedheader
- npm install datatables.net-fixedheader-bs
- npm install datatables.net-select
- npm install datatables.net-select-bs

### Notes:

- Some DataTables features may need additional installation, but I have not found anything that doesn't work so far.
- The `pdfmake` and `jszip` functions require the external `jszip` and `pdfmake` libraries. When I installed these with `npm`, they placed scores of folders in the `node_modules` folder, making it incredible complex. It may be better to load the main javascripts from the `static/js folder`. That said, as far as I know, we are not currently using these functions, so no action is needed at this time.
- `jquery.dataTables.areaselect.js` and `natural.js` cannot be loaded from `npm`, so they are placed in the `static/js` folder.

## For `manage.html`

- npm install sydcanem/bootstrap-contextmenu

## For `wordcloud.html`, `multicloud.html`, `rwanalysis.html`

- npm install d3@3.5.17
- npm install d3-cloud
- npm install canvg/canvg

## For `multicloud.html`

- npm install bootstrap-switch

## Packages Not Maintained with `npm`

Some packages could not be installed using `npm`. These are listed below with implementation notes:

1. The DataTables extensions `jquery.dataTables.areaselect.js` and `natural.js` are placed in the `static/js` folder.
in the `static/js` folder.
2. The Lato font has been removed from the repo to avoid storing too many font files. Currently, this font is downloaded from Google fonts. Some effort will be required to duplicate the look with a local version, as I have not managed to get the settings to produce the same size and shape as our downloaded Google fonts version (which is version 1.0 of the font). Version 2.015 can be installed using `npm` from `[https://github.com/betsol/lato-font](https://github.com/betsol/lato-font)` using `npm i -D lato-font`. 
3. The Junicode font is placed in the `static/fonts` folder. It is accessed by the `html/pre_defined_rules.html` and `js/scripts_scrub.js`, so it needs to remain in this location.

