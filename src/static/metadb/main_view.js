all_columns_defs = [
    { className: ' dt-center', targets: '_all', }
]

var collection_update_url = $('#tab-collection').attr('update-data-url').split('99999');
var collection_delete_url = $('#tab-collection').attr('delete-data-url').split('99999');

collection_columns = [
    { 'render': function() { return null; } },  // For checkboxes
    { 'render': function (data, type, row, meta) {
        return '<div><button type="button" class="btn btn-warning btn-sm js-update-collection"'
               + `data-url="${collection_update_url[0]}${row.id}${collection_update_url[1]}">`
               + '<span class="glyphicon glyphicon-pencil"></span></button></div>&nbsp;'
               + '<div><button type="button" class="btn btn-danger btn-sm js-delete-collection"'
               + `data-url="${collection_delete_url[0]}${row.id}${collection_delete_url[1]}">`
               + '<span class="glyphicon glyphicon-trash"></span></button></div>';
    } },  // for buttons
    { 'data': 'id' },
    { 'data': 'label' },
    { 'data': 'name' },
    { 'data': 'description' },
    { 'data': 'organization' },
    { 'data': 'organization_url' },
    { 'data': 'url' },
]

collection_columnsDefs = [
    { width: '20px', targets: 0, orderable: false, className: 'select-checkbox' }, // Select checkbox
    { width: '45px', targets: 1, orderable: false, }, // Buttons
    { width: '5%', targets: 2 },  // Id
    { width: '11%', targets: 3 },  // Label
    { width: '14%', targets: 4 },  // Name
    { width: '22%', targets: 5 },  // Description
    { width: '10%', targets: 6 },  // Organiation
    { width: '15%', targets: 7,  // Urganization URL
      render: (data) => `<a href="${data}" target="_blank">${data}</a>`,
    },
    { width: '15%', targets: 8,  // URL
      render: (data) => `<a href="${data}" target="_blank">${data}</a>`,
    },
]

var dataset_update_url = $('#tab-dataset').attr('update-data-url').split('99999');
var dataset_delete_url = $('#tab-dataset').attr('delete-data-url').split('99999');

dataset_columns = [
    { 'render': function() { return null; } }, // For checkboxes
    { 'render': function (data, type, row, meta) {
        return '<div><button type="button" class="btn btn-warning btn-sm js-update-dataset"'
               + `data-url="${dataset_update_url[0]}${row.id}${dataset_update_url[1]}">`
               + '<span class="glyphicon glyphicon-pencil"></span></button></div>&nbsp;'
               + '<div><button type="button" class="btn btn-danger btn-sm js-delete-dataset"'
               + `data-url="${dataset_delete_url[0]}${row.id}${dataset_delete_url[1]}">`
               + '<span class="glyphicon glyphicon-trash"></span></button></div>';
    } },  // for buttons
    { 'data': 'id' },
    { 'data': 'is_visible' },
    { 'data': 'collection_label' },
    { 'data': 'resolution_name' },
    { 'data': 'scenario_name' },
    { 'data': 'data_kind_name' },
    { 'data': 'file_type_name' },
    { 'data': 'time_start' },
    { 'data': 'time_end' },
    { 'data': 'description' },
]

dataset_columnsDefs = [
    { width: '20px', targets: 0, orderable: false, className: 'select-checkbox' },  // Select checkbox
    { width: '45px', targets: 1, orderable: false, },  // Buttons
    { width: '5%', targets: 2 },  // Id
    { width: '45px', targets: 3,   // Is visible
      render: (data) => {
          return data == 0 ? "" : '<span class="glyphicon glyphicon-ok"></span>';
      }, 
    },
    { width: '11%', targets: 4 },  // Collection label
    { width: '10%', targets: 5 },  // Resolution
    { width: '15%', targets: 6 },  // Scenario
    { width: '7%', targets: 7 },   //Data kind
    { width: '7%', targets: 8 },   // File type
    { width: '8%', targets: 9 },  // Time start
    { width: '8%', targets: 10 },  // Time end
    { width: '15%', targets: 11 },  // Description
]

var specpar_update_url = $('#tab-specpar').attr('update-data-url').split('99999');
var specpar_delete_url = $('#tab-specpar').attr('delete-data-url').split('99999');

specpar_columns = [
    { 'render': function() { return null; } }, // For checkboxes
    { 'render': function (data, type, row, meta) {
        return '<div><button type="button" class="btn btn-warning btn-sm js-update-specpar"'
               + `data-url="${specpar_update_url[0]}${row.id}${specpar_update_url[1]}">`
               + '<span class="glyphicon glyphicon-pencil"></span></button></div>&nbsp;'
               + '<div><button type="button" class="btn btn-danger btn-sm js-delete-specpar"'
               + `data-url="${specpar_delete_url[0]}${row.id}${specpar_delete_url[1]}">`
               + '<span class="glyphicon glyphicon-trash"></span></button></div>';
    } },  // for buttons
    { 'data': 'id' },
    { 'data': 'is_visible' },
    { 'data': 'parameter_name' },
    { 'data': 'acc_mode_name' },
    { 'data': 'time_step_name' },
    { 'data': 'time_step_label' },
    { 'data': 'time_step_subpath' },
    { 'data': 'levels_group' },
    { 'data': 'levels_group_desc' },
    { 'data': 'levels' },
]

specpar_columnsDefs = [
    { width: '20px', targets: 0, orderable: false, className: 'select-checkbox' },  // Select checkbox
    { width: '45px', targets: 1, orderable: false, },  // Buttons
    { width: '25px', targets: 2 },  // Id
    { width: '45px', targets: 3,   // Is visible
      render: (data) => {
          return data == 0 ? "" : '<span class="glyphicon glyphicon-ok"></span>';
      }, 
    },
    { width: '95px', targets: 4 },   // Parameter name
    { width: '95px', targets: 5 },   // Accumulation mode
    { width: '95px', targets: 6 },   // Time step name
    { width: '95px', targets: 7 },   // Time step label
    { width: '95px', targets: 8 },   // Time step subpath
    { width: '95px', targets: 9 },   // Levels group
    { width: '95px', targets: 10 },  // Levels group description
    { width: '175px', targets: 11 },  // Levels
]

var data_update_url = $('#tab-data').attr('update-data-url').split('99999');
var data_delete_url = $('#tab-data').attr('delete-data-url').split('99999');

data_columns = [
    { 'render': function() { return null; } }, // For checkboxes
    { 'render': function (data, type, row, meta) {
        return '<div><button type="button" class="btn btn-warning btn-sm js-update-data"'
               + `data-url="${data_update_url[0]}${row.id}${data_update_url[1]}">`
               + '<span class="glyphicon glyphicon-pencil"></span></button></div>&nbsp;'
               + '<div><button type="button" class="btn btn-danger btn-sm js-delete-data"'
               + `data-url="${data_delete_url[0]}${row.id}${data_delete_url[1]}">`
               + '<span class="glyphicon glyphicon-trash"></span></button></div>';
    } },
    { 'data': 'id' },
    { 'data': 'is_visible' },
    { 'data': 'collection_label' },
    { 'data': 'resolution_name' },
    { 'data': 'scenario_name' },
    { 'data': 'parameter_name' },
    { 'data': 'time_step' },
    { 'data': 'levels_group' },
    { 'data': 'levels' },
    { 'data': 'levels_variable' },
    { 'data': 'variable_name' },
    { 'data': 'units_name' },
    { 'data': 'property_label' },
    { 'data': 'property_value' },
    { 'data': 'root_dir' },
    { 'data': 'file_pattern' },
    { 'data': 'scale' },
    { 'data': 'offset' },
]

data_columnsDefs = [
    { width: '20px', targets: 0, orderable: false, className: 'select-checkbox' },  // Select checkbox
    { width: '45px', targets: 1, orderable: false, },  // Buttons
    { width: '25px', targets: 2 },    // Id
    { width: '45px', targets: 3,   // Is visible
      render: (data) => {
          return data == 0 ? "" : '<span class="glyphicon glyphicon-ok"></span>';
      }, 
    },
    { width: '95px', targets: 4, },   // Collection label
    { width: '75px', targets: 5 },    // Resolution
    { width: '95px', targets: 6 },    // Scenario
    { width: '95px', targets: 7 },    // Parameter
    { width: '75px', targets: 8 },    // Time step
    { width: '95px', targets: 9 },   // Levels group
    { width: '175px', targets: 10 },  // Levels names
    { width: '55px', targets: 11 },   // Levels variable
    { width: '95px', targets: 12 },    // Variable name
    { width: '55px', targets: 13 },   // Units
    { width: '85px', targets: 14 },   // Property label
    { width: '85px', targets: 15 },   // Property value
    { width: '165px', targets: 16 },   // Root dir
    { width: '165px', targets: 17 },  // File pattern
    { width: '55px', targets: 18 },   // Scale
    { width: '55px', targets: 19 },   // Offset
]

commonOptions = {
    initComplete: postInit,
    sDom: 'ti',
    orderCellsTop: true,
    paginate: false,
    select: {style: 'multi', selector: 'td:first-child',},
    scrollY: 400,
    scrollX: true,
    scrollCollapse: true,
    order: [[ 2, 'asc' ]],
    autoWidth: false,
};

function make_empty_row(table) {  
    // Add an empty row for filters in the table header
    var n_col = table.columns().header().length; // Number of columns in table
    var empty_row = $('<tr></tr>');
    for (var i = 0; i < n_col; i++) {
        var classList = $(table.table().header().rows[0].cells[i]).attr('class');
        var th = $('<th></th>');
        th.addClass(classList).removeClass('sorting').removeClass('sorting_asc');
        empty_row.append(th);
    };
    return empty_row;
};

function add_filters(that) {
    // Add filters to the table header
    var table = that.api();
    var second_header = make_empty_row(table);
    table_id = that.attr('id');
    $( table.table().header() ).append(second_header);

    // Loop over columns and add filters to corresponding cells in the second header row
    table.columns().every( function () {
        var column = this;
        var id = column.index();
        var th = $( second_header[0].cells[id] );

        // 'Select all' checkbox is in the first cell always!
        if (id == 0) {
            var check_all = $(`<input type="checkbox" id="check-all-${table_id}"></input>`).appendTo(th);
            check_all.on( 'change', function() {
                if ($(this).is(':checked')) {
                    table.rows().select();
                } else {
                    table.rows().deselect();
                };
            } );
        };
        
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

$(document).ready( function () {
    $('a[data-toggle="tab"]').on( 'shown.bs.tab', function() {
        columnsAdjust();
    } );
    $(window).resize(function () { 
        columnsAdjust();
    });

    // Create Collections table
    var collectionOptions = $.extend(true, {}, commonOptions);
    collectionOptions["columnDefs"] = collection_columnsDefs.concat(all_columns_defs);
    collectionOptions["columns"] = collection_columns;
    collectionOptions["ajax"] = { 'url': 'collections/api/', 'type': 'GET', 'dataSrc': '' };
    $('#collection').DataTable( collectionOptions ).on('draw', function() {
        addUpdDelButtonHandlers.call(this, 'collection');
    });

    // Create Datasets table
    var datasetOptions = $.extend(true, {}, commonOptions);
    datasetOptions["columnDefs"] = dataset_columnsDefs.concat(all_columns_defs),
    datasetOptions["columns"] = dataset_columns;
    datasetOptions["ajax"] = { 'url': 'datasets/api/', 'type': 'GET', 'dataSrc': '' };
    $('#dataset').DataTable( datasetOptions ).on('draw', function() {
        addUpdDelButtonHandlers.call(this, 'dataset');
    });

    // Create Specific parameter table
    var specparOptions = $.extend(true, {}, commonOptions);
    specparOptions["columnDefs"] = specpar_columnsDefs.concat(all_columns_defs),
    specparOptions["columns"] = specpar_columns;
    specparOptions["ajax"] = { 'url': 'specpars/api/', 'type': 'GET', 'dataSrc': '' };
    $('#specpar').DataTable( specparOptions ).on('draw', function() {
        addUpdDelButtonHandlers.call(this, 'specpar');
    });

    // Create Data table
    var dataOptions = $.extend(true, {}, commonOptions);
    dataOptions["columnDefs"] = data_columnsDefs.concat(all_columns_defs),
    dataOptions["columns"] = data_columns;
    dataOptions["ajax"] = { 'url': 'data/api/', 'type': 'GET', 'dataSrc': '' };
    $('#data').DataTable( dataOptions ).on('draw', function() {
        addUpdDelButtonHandlers.call(this, 'data');
    });
 
} );