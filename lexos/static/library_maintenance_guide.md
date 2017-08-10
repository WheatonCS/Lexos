# Library File Maintenance Guide

Template files now load external libraries from `static/node_modules`. These libraries are maintained using `npm`. A record of the installation commands used is maintained below.

As long as the `package.json` and `package-lock.json` files are unchanged, the entire sequence can be achieved by running `npm install`.

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
3. The Lato and Junicode fonts are placed in the `static/fonts` folder. Currently, these are not accessed; the fonts are loaded from the web. However, we should really make loading from local files an alternative for local mode. I have not done this because I cannot make the downloaded version of Lato look exactly like the version downloaded from Google fonts.

