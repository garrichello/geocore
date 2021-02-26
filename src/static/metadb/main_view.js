all_columns_defs = [
    { className: ' dt-center', targets: '_all', }
]

var collection_api_url = $('#tab-collection').attr('api-data-url')

collection_columns = [
    { 'render': function() { return null; } },  // For checkboxes
    { 'render': function (data, type, row, meta) {
        return '<div><button type="button" class="btn btn-warning btn-sm js-update-collection"'
               + `data-url="${collection_api_url}${row.id}/">`
               + '<span class="glyphicon glyphicon-pencil"></span></button></div>&nbsp;'
               + '<div><button type="button" class="btn btn-danger btn-sm js-delete-collection"'
               + `data-url="${collection_api_url}${row.id}/">`
               + '<span class="glyphicon glyphicon-trash"></span></button></div>';
    } },  // for buttons
    { 'data': 'id' },
    { 'data': 'label' },
    { 'data': 'collectioni18n.name' },
    { 'data': 'collectioni18n.description' },
    { 'data': 'organization.organizationi18n.name' },
    { 'data': 'organization.url' },
    { 'data': 'url' },
]

collection_columnsDefs = [
    { width: '20px', targets: 0, orderable: false, className: 'select-checkbox' }, // Select checkbox
    { width: '45px', targets: 1, orderable: false, }, // Buttons
    { width: '5%', targets: 2 },  // Id
    { width: '11%', targets: 3 },  // Label
    { width: '14%', targets: 4 },  // Name
    { width: '20%', targets: 5 },  // Description
    { width: '12%', targets: 6 },  // Organization
    { width: '15%', targets: 7,  // Urganization URL
      render: (data) => `<a href="${data}" target="_blank">${data}</a>`,
    },
    { width: '15%', targets: 8,  // URL
      render: (data) => `<a href="${data}" target="_blank">${data}</a>`,
    },
]

var dataset_api_url = $('#tab-dataset').attr('api-data-url');

dataset_columns = [
    { 'render': function() { return null; } }, // For checkboxes
    { 'render': function (data, type, row, meta) {
        return '<div><button type="button" class="btn btn-warning btn-sm js-update-dataset"'
               + `data-url="${dataset_api_url}${row.id}/">`
               + '<span class="glyphicon glyphicon-pencil"></span></button></div>&nbsp;'
               + '<div><button type="button" class="btn btn-danger btn-sm js-delete-dataset"'
               + `data-url="${dataset_api_url}${row.id}/">`
               + '<span class="glyphicon glyphicon-trash"></span></button></div>';
    } },  // for buttons
    { 'data': 'id' },
    { 'data': 'is_visible' },
    { 'data': 'collection_label' },
    { 'data': 'resolution.name' },
    { 'data': 'scenario.name' },
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

var specpar_api_url = $('#tab-specpar').attr('api-data-url');

specpar_columns = [
    { 'render': function() { return null; } }, // For checkboxes
    { 'render': function (data, type, row, meta) {
        return '<div><button type="button" class="btn btn-warning btn-sm js-update-specpar"'
               + `data-url="${specpar_api_url}${row.id}">`
               + '<span class="glyphicon glyphicon-pencil"></span></button></div>&nbsp;'
               + '<div><button type="button" class="btn btn-danger btn-sm js-delete-specpar"'
               + `data-url="${specpar_api_url}${row.id}">`
               + '<span class="glyphicon glyphicon-trash"></span></button></div>';
    } },  // for buttons
    { 'data': 'id' },
    { 'data': 'parameter.is_visible' },
    { 'data': 'parameter.parameteri18n.name' },
    { 'data': 'parameter.accumulation_mode' },
    { 'data': 'time_step.timestepi18n.name' },
    { 'data': 'time_step.label' },
    { 'data': 'time_step.subpath2' },
    { 'data': 'levels_group.units.unitsi18n.name' },
    { 'data': 'levels_group.description' },
    { 'data': function(data, type, row, meta) {
        levels = Array();
        data.levels_group.levels.forEach(element => {
            levels.push(element.leveli18n.name);
        });
        return levels.join();
    } },
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

var data_api_url = $('#tab-data').attr('api-data-url');

data_columns = [
    { 'render': function() { return null; } }, // For checkboxes
    { 'render': function (data, type, row, meta) {
        return '<div><button type="button" class="btn btn-warning btn-sm js-update-data"'
               + `data-url="${data_api_url}${row.id}">`
               + '<span class="glyphicon glyphicon-pencil"></span></button></div>&nbsp;'
               + '<div><button type="button" class="btn btn-danger btn-sm js-delete-data"'
               + `data-url="${data_api_url}${row.id}">`
               + '<span class="glyphicon glyphicon-trash"></span></button></div>';
    } },
    { 'data': 'id' },
    { 'data': 'dataset.is_visible' },
    { 'data': 'dataset.collection_label' },
    { 'data': 'dataset.resolution.name' },
    { 'data': 'dataset.scenario.name' },
    { 'data': 'parameter.is_visible' },
    { 'data': 'parameter.parameteri18n.name' },
    { 'data': 'time_step.timestepi18n.name' },
    { 'data': 'levels_group.description' },
    { 'data': function(data, type, row, meta) {
        levels = Array();
        data.levels_group.levels.forEach(element => {
            levels.push(element.leveli18n.name);
        });
        return levels.join();
    } },
    { 'data': 'levels_variable.name' },
    { 'data': 'variable.name' },
    { 'data': 'units.unitsi18n.name' },
    { 'data': 'property.label' },
    { 'data': 'property_value.label' },
    { 'data': 'root_dir.name' },
    { 'data': 'dataset.scenario.subpath0' },
    { 'data': 'dataset.resolution.subpath1' },
    { 'data': 'time_step.subpath2' },
    { 'data': 'file.name_pattern' },
    { 'data': 'scale' },
    { 'data': 'offset' },
]

data_columnsDefs = [
    { width: '20px', targets: 0, orderable: false, className: 'select-checkbox' },  // Select checkbox
    { width: '45px', targets: 1, orderable: false, },  // Buttons
    { width: '25px', targets: 2 },    // Id
    { width: '55px', targets: 3,   // Is dataset visible
      render: (data) => {
          return data == 0 ? "" : '<span class="glyphicon glyphicon-ok"></span>';
      }, 
    },
    { width: '95px', targets: 4, },   // Collection label
    { width: '75px', targets: 5 },    // Resolution
    { width: '95px', targets: 6 },    // Scenario
    { width: '65px', targets: 7,   // Is parameter visible
      render: (data) => {
          return data == 0 ? "" : '<span class="glyphicon glyphicon-ok"></span>';
      }, 
    },
    { width: '95px', targets: 8 },    // Parameter
    { width: '75px', targets: 9 },    // Time step
    { width: '95px', targets: 10 },   // Levels group
    { width: '175px', targets: 11 },  // Levels names
    { width: '55px', targets: 12 },   // Levels variable
    { width: '95px', targets: 13 },    // Variable name
    { width: '55px', targets: 14 },   // Units
    { width: '85px', targets: 15 },   // Property label
    { width: '85px', targets: 16 },   // Property value
    { width: '165px', targets: 17 },   // Root dir
    { width: '75px', targets: 18 },   // Subpath0
    { width: '75px', targets: 19 },   // Subpath1
    { width: '75px', targets: 20 },   // Subpath2
    { width: '165px', targets: 21 },  // File pattern
    { width: '55px', targets: 22 },   // Scale
    { width: '55px', targets: 23 },   // Offset
]

var edge_api_url = $('#tab-edge').attr('api-data-url')

edge_columns = [
    { 'render': function() { return null; } },  // For checkboxes
    { 'render': function (data, type, row, meta) {
        return '<div><button type="button" class="btn btn-warning btn-sm js-update-edge"'
               + `data-url="${edge_api_url}${row.id}">`
               + '<span class="glyphicon glyphicon-pencil"></span></button></div>&nbsp;'
               + '<div><button type="button" class="btn btn-danger btn-sm js-delete-edge"'
               + `data-url="${edge_api_url}${row.id}">`
               + '<span class="glyphicon glyphicon-trash"></span></button></div>';
    } },  // for buttons
    { 'data': 'conveyor.id' },
    { 'data': 'id' },
    { 'data': 'from_vertex.id' },
    { 'data': 'from_vertex.computing_module.name' },
    { 'data': 'from_vertex.condition_option.label' },
    { 'data': 'from_vertex.condition_value.label' },
    { 'data': 'from_output' },
    { 'data': 'to_vertex.id' },
    { 'data': 'to_vertex.computing_module.name' },
    { 'data': 'to_vertex.condition_option.label' },
    { 'data': 'to_vertex.condition_value.label' },
    { 'data': 'to_input' },
    { 'data': 'data_variable.label' },
    { 'data': 'data_variable.description' },
    { 'data': 'data_variable.units.unitsi18n.name' },
]

edge_columnsDefs = [
    { width: '20px', targets: 0, orderable: false, className: 'select-checkbox' }, // Select checkbox
    { width: '45px', targets: 1, orderable: false, }, // Buttons
    { width: '65px', targets: 2, },   // edge id
    { width: '55px', targets: 3 },    // Edge id
    { width: '55px', targets: 4 },    // From vertex id
    { width: '115px', targets: 5 },   // From module
    { width: '75px', targets: 6 },    // From option
    { width: '75px', targets: 7 },    // From option value
    { width: '55px', targets: 8 },    // From output
    { width: '55px', targets: 9 },    // To vertex id
    { width: '115px', targets: 10 },  // To module
    { width: '75px', targets: 11 },   // To option
    { width: '75px', targets: 12 },   // To option value
    { width: '55px', targets: 13 },   // To input
    { width: '135px', targets: 14 },   // Data label
    { width: '135px', targets: 15 },   // Data description
    { width: '75px', targets: 16 },   // Units
]

commonOptions = {
    initComplete: postInit,
    sDom: 'tri',
    orderCellsTop: true,
    paginate: false,
    select: {style: 'multi', selector: 'td:first-child',},
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
    collectionOptions["ajax"] = { 'url': collection_api_url, 'type': 'GET', 'dataSrc': 'data' };
    $('#collection').DataTable( collectionOptions ).on('draw', function() {
        addUpdDelButtonHandlers.call(this, 'collection');
    });
    $('#collection').DataTable().on('xhr.dt', set_header);

    // Create Datasets table
    var datasetOptions = $.extend(true, {}, commonOptions);
    datasetOptions["columnDefs"] = dataset_columnsDefs.concat(all_columns_defs),
    datasetOptions["columns"] = dataset_columns;
    datasetOptions["ajax"] = { 'url': dataset_api_url, 'type': 'GET', 'dataSrc': 'data' };
    $('#main-tabs a[href="#tab-dataset"]').on('click', function() {
        if (!$.fn.DataTable.isDataTable('#dataset')) {
            $('#dataset').DataTable( datasetOptions ).on('draw', function() {
                addUpdDelButtonHandlers.call(this, 'dataset');
            });
            $('#dataset').DataTable().on('xhr.dt', set_header);
        }
    });

    // Create Specific parameter table
    var specparOptions = $.extend(true, {}, commonOptions);
    specparOptions["columnDefs"] = specpar_columnsDefs.concat(all_columns_defs),
    specparOptions["columns"] = specpar_columns;
    specparOptions["ajax"] = { 'url': specpar_api_url, 'type': 'GET', 'dataSrc': 'data' };
    $('#main-tabs a[href="#tab-specpar"]').on('click', function() {
        if (!$.fn.DataTable.isDataTable('#specpar')) {
            $('#specpar').DataTable( specparOptions ).on('draw', function() {
                addUpdDelButtonHandlers.call(this, 'specpar');
            });
            $('#specpar').DataTable().on('xhr.dt', set_header);
        }
    });

    // Create Data table
    var dataOptions = $.extend(true, {}, commonOptions);  
    dataOptions["columnDefs"] = data_columnsDefs.concat(all_columns_defs),
    dataOptions["columns"] = data_columns;
    dataOptions["ajax"] = { 'url': data_api_url, 'type': 'GET', 'dataSrc': 'data' };
    $('#main-tabs a[href="#tab-data"]').on('click', function() {
        if (!$.fn.DataTable.isDataTable('#data')) {
            $('#data').DataTable( dataOptions ).on('draw', function() {
                addUpdDelButtonHandlers.call(this, 'data');
            });
            $('#data').DataTable().on('xhr.dt', set_header);
        }
    });

    // Create Edge table
    var edgeOptions = $.extend(true, {}, commonOptions);
    edgeOptions["columnDefs"] = edge_columnsDefs.concat(all_columns_defs);
    edgeOptions["columns"] = edge_columns;
    edgeOptions["ajax"] = { 'url': edge_api_url, 'type': 'GET', 'dataSrc': 'data' };
    $('#main-tabs a[href="#tab-edge"]').on('click', function() {
        if (!$.fn.DataTable.isDataTable('#edge')) {
            $('#edge').DataTable( edgeOptions ).on('draw', function() {
                addUpdDelButtonHandlers.call(this, 'edge');
            });
            $('#edge').DataTable().on('xhr.dt', set_header);
        }
    });

    // Create Other tables
    function prePostInit() {
        var table = $(this).DataTable();
        for (var i = 3; i < table.columns().header().length; i++) {
            $(table.columns(i).header()).addClass('head_text');
        }
        postInit.call(this);
    }

    var otherOptions = {
        initComplete: prePostInit,
        sDom: 'tri',
        orderCellsTop: true,
        paginate: false,
        select: {style: 'multi', selector: 'td:first-child',},
        scrollY: 400,
        scrollX: true,
        scrollCollapse: true,
        order: [[ 2, 'asc' ]],
        processing: true,
        language: {
            'loadingRecords': '&nbsp',
            'processing': '<div class="spinner"></div>'
        } 
    };
    var other_api_url;

    var dwell = function(dict, path) {
        var val = dict;
        chunks = path.split('.');
        $.each(chunks, (i, chunk) => {
            val = val[chunk];
        });
        return val;
    }

    var delister = function(data, field_idx) {
        // Here we extract items from an Array of dictionaries came from the server as a JSON.
        // In rare cases a field contains a list of structures (dictionaries) with items.
        // Items can be borrowed deep in the nested dictionary structure.
        // subfield field in the JSON helps to reach for these items.
        $.each(data.data, (i, e) => {  // loop over rows
            $.each(e, (v, k) => {  // loop over columns
                if (Array.isArray(k)) {  // if a cell contains an Array
                    var items = Array();  // here we will store the Array items
                    $.each(data.data[i][v], (l, m) => {  // loop over items
                        items.push(dwell(m, data.headers[field_idx[v]].subfield));  // group
                    })
                    data.data[i][v] = items; // replace original dict with the array
                };
            })
        });
    }

    var create_dt = function(data, data_url) {
        if ($.fn.DataTable.isDataTable('#other')) {
            $('#other').DataTable().destroy();
            $('#other').empty();
            $('#other').off();
        }
        var columns = [
            { 'render': function() { return null; } },  // For checkboxes
            { 'render': function (data, type, row, meta) {
                return '<div><button type="button" class="btn btn-warning btn-sm js-update-other"'
                       + `data-url="${other_api_url}${row.id}">`
                       + '<span class="glyphicon glyphicon-pencil"></span></button></div>&nbsp;'
                       + '<div><button type="button" class="btn btn-danger btn-sm js-delete-other"'
                       + `data-url="${other_api_url}${row.id}">`
                       + '<span class="glyphicon glyphicon-trash"></span></button></div>';
            } },  // for buttons
        ];
        var field_idx = [];
        $.each(data.headers, function (i, v) {
            columns.push({data: v.field, title: v.caption}); // describe columns headers
            field_idx[v.field] = i;  // map field name to its column position
        });
        delister(data, field_idx);
        otherOptions['data'] = data.data;
        otherOptions['columns'] = columns;
        otherOptions['columnDefs'] = [
            { width: 20, targets: 0, orderable: false, className: 'select-checkbox' }, // Select checkbox
            { width: 45, targets: 1, orderable: false, }, // Buttons
        ]
        var odt = $('#other').DataTable( otherOptions );
        odt.on('draw', function() {
            addUpdDelButtonHandlers.call(this, 'other');
        });
        odt.on('processing', function(e, settings, procesing) {
            if (typeof processing !== 'undefined') {
                $('#other_processing').css( 'display', processing ? 'block' : 'none' );
            };
        })
        odt.on('xhr', (e, settings, json, xhr) => {
            delister(json, field_idx);
        })
        addUpdDelButtonHandlers('other');
        odt.ajax.url(data_url);
    }

    var get_data = function(data_url) {
        $.ajax({
            url: data_url,
            dataType: 'json',
            beforeSend: function() {
                $('#other_processing').show();
            },
            success: function(data) {
                create_dt(data, data_url);
                $('#other_processing').hide();
            }
        });
    }

    // Add button
    $('.js-data-choice').click(function() {
        other_api_url = $(this).attr('api-data-url');
        get_data.call(this, other_api_url);
        $('#create-other-btn').attr('disabled', false);
        $('#create-other-btn').attr('data-url', $(this).attr('create-data-url'));
    });

} );