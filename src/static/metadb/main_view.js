/*jslint es6 */
"use strict";

var all_columns_defs = [
    { className: ' dt-center', targets: '_all' }
];

var commonOptions = {
    initComplete: postInit,
    sDom: 'tri',
    orderCellsTop: true,
    paginate: false,
    select: {style: 'multi', selector: 'td:first-child'},
    scrollY: 400,
    scrollX: true,
    scrollCollapse: true,
    order: [[ 2, 'asc' ]],
    autoWidth: false,
    deferRender: true,
    processing: true,
    language: {
        'loadingRecords': '&nbsp',
        'processing': '<div class="spinner"></div>'
    }
};

function make_empty_row(table) {
    // Add an empty row for filters in the table header
    var empty_row = $('<tr></tr>');
    for (var cell of table.table().header().rows[0].cells) {
        let classList = $(cell).attr('class');
        let th = $('<th></th>');
        th.addClass(classList).removeClass('sorting').removeClass('sorting_asc');
        empty_row.append(th);
    };
    return empty_row;
};

function add_filters(that) {
    // Add filters to the table header
    var table = that.api();
    var second_header = make_empty_row(table);
    var table_id = that.attr('id');
    $( table.table().header() ).append(second_header);

    // Loop over columns and add filters to corresponding cells in the second header row
    table.columns().every( function () {
        var column = this;
        var id = column.index();
        var th = $( second_header[0].cells[id] );

        // 'Select all' checkbox is in the first cell always!
/*        if (id == 0) {
            var check_all = $(`<input type="checkbox" id="check-all-${table_id}"></input>`).appendTo(th);
            check_all.on( 'change', function() {
                if ($(this).is(':checked')) {
                    table.rows().select();
                } else {
                    table.rows().deselect();
                };
            } );
        };
*/
        var clearButton = $('<button class="close" type="button"><span class="glyphicon glyphicon-remove"></span></button>');
        var input_group = $('<div class="input-group"></div>');

        // Add filter as a select list field
        if (th.hasClass('head_select')) {
            var select = $(`<select class="form-control" id="select_${table_id}_${id}"></select>`);
            select.append('<option value="">*</option>');
            column.data().unique().sort().each( function( d, j ) {
                select.append( `<option value="${d}">${d}</option>` )
            } );

            select.on( 'change', function() {
                var val = $.fn.dataTable.util.escapeRegex(
                    $(this).val()
                );
                column
                    .search( val ? `^${val}$` : '', true, false )
                    .draw();
            } );

            clearButton.on( 'click', function() {
                select.prop("selectedIndex", 0);
                select.trigger("change");
            } );

            input_group.append(select);
            th.append( input_group.append($('<span class="input-group-btn"></span>').append(clearButton)) );
        };

        // Add filter as an input text field
        if (th.hasClass('head_text')) {
            var text = $(`<input class="form-control" type="text" id="text_${table_id}_${id}">`).appendTo(input_group);
            th.append( input_group.append($('<span class="input-group-btn"></span>').append(clearButton)) );
            text.on('keyup change clear', function() {
                if (column.search() != this.value) {
                    column
                        .search( this.value )
                        .draw();
                };
            } );
            clearButton.on( 'click', function() {
                text.val("");
                text.trigger('clear');
            } );
        };
    } );
}

function postInit() {
    // Called after a data table was initialized. Executed for each table!
    add_filters(this);  // Add add search filters into the table header.
};

function columnsAdjust() {
    // Adjusts columns widths for all tables.
    $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();
    $.fn.dataTable.tables( {visible: true, api: true} ).draw();
};

function set_header(e, settings, json, xhr) {
    // Get headers from JSON data and put them into the table
    var table = $(this).DataTable();

    if (json != null) {
        $.each(json.headers, function(i, v) {
            table.columns().header()[i+2].innerText = v[1];  // Start at the 3rd column
            $(table.columns().header()[i+2]).addClass(v[0]);
        })
    }
}

function renderButtons(row, url, showInfoBtn=false) {
    var infoButton = `&nbsp;<div><button type="button" class="btn btn-info btn-sm js-info"
                      data-url="${url}${row.id}">
                      <span class="glyphicon glyphicon-chevron-down"></span></button></div>`;

    return `<div><button type="button" class="btn btn-warning btn-sm js-update"
            data-url="${url}${row.id}/">
            <span class="glyphicon glyphicon-pencil"></span></button></div>&nbsp;`+
           `<div><button type="button" class="btn btn-danger btn-sm js-delete"
            data-url="${url}${row.id}/">
            <span class="glyphicon glyphicon-trash"></span></button></div>`+
            (showInfoBtn ? infoButton : '');
}

$(document).ready( function () {
    $('a[data-toggle="tab"]').on( 'shown.bs.tab', function() {
        columnsAdjust();
    } );
    $(window).resize(function () {
        columnsAdjust();
    });

} );