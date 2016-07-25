/*
 * jquery.dataTables.areaselect
 * 2015 - Adrien Cuisinier
 * Released under the MIT license.
 * v1.0.0
 */

(function ($) {
    //* UTILS *//
    $.fn.withinBox = function (left, top, width, height, useOffsetCache) {
        var ret = [];
        this.each(function () {
            var q = $(this);
            if (this === document.documentElement) return ret.push(this);
            var offset = useOffsetCache ? $.data(this, "offset") || $.data(this, "offset", q.offset()) : q.offset();
            var ew = q.width(),
                eh = q.height(),
                res = !((offset.top > top + height) || (offset.top + eh < top) || (offset.left > left + width) || (offset.left + ew < left));

            if (res) ret.push(this);
            return true;
        });
        return this.pushStack($.unique(ret), "withinBox", $.makeArray(arguments).join(","));
    };

    //* PRIVATES *//

    // Extension cache
    window.dtCtx = {
        initialized: false,
        current: null,
        selection: [],
        multiSelection: false,
        dragFirstFrame: false,
        mouseSartTarget: null,
        mouseDragStart: false,
        mouseDragStartPos: {
            x: 0,
            y: 0
        },
        area: {
            top: 0,
            left: 0,
            width: 0,
            height: 0
        }
    };
    
    function dtSetArea(top, left, width, height) {
        dtCtx.area.top = top;
        dtCtx.area.left = left;
        dtCtx.area.width = width;
        dtCtx.area.height = height;
    }

    // Changes backgrounds of selected items
    function dtSelectRows() {
        var selection = $(dtCtx.current + " tbody > tr")
                        .withinBox(dtCtx.area.left,
                                   dtCtx.area.top,
                                   dtCtx.area.width,
                                   dtCtx.area.height);

        var table = $(dtCtx.current).DataTable();

        if (dtCtx.selection.length === selection.length) return;

        var lst = [];
        if (dtCtx.selection.length < selection.length) {
            $.grep(selection, function (e) {
                if ($.inArray(e, dtCtx.selection) === -1) lst.push(e);
            });

            $.each(lst, function (i, tr) {
                if (!$(tr).hasClass("selected"))
                    table.row(tr).select();
            });
        } else {
            $.grep(dtCtx.selection, function (e) {
                if ($.inArray(e, selection) === -1) lst.push(e);
            });

            $.each(lst, function (i, tr) {
                table.row(tr).deselect();
            });
        }

        dtCtx.selection = selection;
    }

    // Updates selection square
    function dtMouseMove(event) {
        if (dtCtx.dragFirstFrame && !dtCtx.multiSelection) {
            var table = $(dtCtx.current).DataTable();
            table.rows({ selected: true }).deselect();
            dtCtx.dragFirstFrame = false;
        }

        var top, left, width, height;
        if (event.pageX > dtCtx.mouseDragStartPos.x &&
            event.pageY > dtCtx.mouseDragStartPos.y) {
            top = dtCtx.mouseDragStartPos.y;
            left = dtCtx.mouseDragStartPos.x;
            width = event.pageX - dtCtx.mouseDragStartPos.x;
            height = event.pageY - dtCtx.mouseDragStartPos.y;
        } else if (event.pageX < dtCtx.mouseDragStartPos.x &&
                   event.pageY < dtCtx.mouseDragStartPos.y) {
            top = event.pageY;
            left = event.pageX;
            width = dtCtx.mouseDragStartPos.x - event.pageX;
            height = dtCtx.mouseDragStartPos.y - event.pageY;
        } else if (event.pageY < dtCtx.mouseDragStartPos.y) {
            top = event.pageY;
            left = dtCtx.mouseDragStartPos.x;
            width = event.pageX - dtCtx.mouseDragStartPos.x;
            height = dtCtx.mouseDragStartPos.y - event.pageY;
        } else {
            top = dtCtx.mouseDragStartPos.y;
            left = event.pageX;
            width = dtCtx.mouseDragStartPos.x - event.pageX;
            height = event.pageY - dtCtx.mouseDragStartPos.y;
        }

        dtSetArea(top, left, width, height);

        dtSelectRows();
    }

    function dtInitPersitancy() {
        if (!dtCtx.initialized) {
            dtCtx.initialized = true;

            $(window).on("mouseup", function () {
                if (!dtCtx.mouseDragStart) return;

                $(window).off("mousemove");

                dtCtx.mouseDragStart = false;
                dtCtx.current = null;
                dtCtx.selection.length = 0;
            });

            $(document)
                .on("keydown", function (e) {
                    if (e.keyCode !== 17 || dtCtx.multiSelection) return;
                    dtCtx.multiSelection = true;

                })
                .on("keyup", function (e) {
                    if (e.keyCode !== 17 || !dtCtx.multiSelection) return;
                    dtCtx.multiSelection = false;
                });
        }
    }

    function dtAreaSelection(table) {
        $(table)
            .on("mousedown", "tbody > tr > td:not(.dataTables_empty):not(.dataTables_noselect)", function (event) {
                var table = $(this).closest("table");
                if (table.attr("disabled")) return;

                // set context
                dtCtx.current = "#" + table.attr("id");
                dtCtx.dragFirstFrame = true;
                dtCtx.mouseSartTarget = event.target;
                dtCtx.mouseDragStart = true;
                dtCtx.mouseDragStartPos.x = event.pageX;
                dtCtx.mouseDragStartPos.y = event.pageY;
                dtCtx.selection.length = 0;
                dtCtx.selection.push(this);
                
                dtSetArea(event.pageY, event.pageX, 1, 1);

                // fallow mouse moves
                $(window).on("mousemove", dtMouseMove);
            });
    }

    //* MAIN *//

    $.fn.AreaSelect = function () {
        if (!$(this).is("table")) {
            console.error("Table element expected");
            return;
        }
        dtInitPersitancy();
        dtAreaSelection(this);
    };

    return $;
})(jQuery);